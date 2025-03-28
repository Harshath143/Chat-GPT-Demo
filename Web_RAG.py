from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import faiss
import numpy as np
import ollama
import vosk
import wave
import json
import requests
from bs4 import BeautifulSoup
import fitz  # pymupdf for PDF text extraction
import docx  # python-docx for DOCX file handling
from sentence_transformers import SentenceTransformer
from googletrans import Translator
import tempfile
from newspaper import Article  # Corrected import from newspaper3k

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Web RAG API"}

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Vosk Model for Speech-to-Text
try:
    vosk_model = vosk.Model(model_name="vosk-model-small-en-us-0.15")
except Exception as e:
    raise RuntimeError("Error loading Vosk model: " + str(e))

# Initialize Google Translator
translator = Translator()

# Dictionary to store FAISS memory & chat history per session
session_memory = {}
chat_history = {}
file_embeddings = {}
web_embeddings = {}

# FAISS settings
dimension = 384
index = faiss.IndexFlatL2(dimension)

# Max memory per session
MAX_MEMORY = 5  

# Request models
class ChatRequest(BaseModel):
    session_id: str
    prompt: str
    language: str = "en"
    url: str = None  # Optional URL for web RAG

# Function to scrape web page
def scrape_website(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        text = " ".join([p.text for p in soup.find_all("p")])
        return text if len(text) > 100 else "No useful content found."
    except Exception as e:
        return f"Error retrieving website: {str(e)}"

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to transcribe audio using Vosk
def transcribe_audio(audio_path):
    try:
        wf = wave.open(audio_path, "rb")
        rec = vosk.KaldiRecognizer(vosk_model, wf.getframerate())

        text = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text += result.get("text", "") + " "

        final_result = json.loads(rec.FinalResult())
        text += final_result.get("text", "")
        return text.strip()
    except Exception as e:
        return f"Error in audio transcription: {str(e)}"

# File Upload & Embedding
@app.post("/upload/")
async def upload_file(session_id: str, file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(await file.read())
    temp_file.close()

    # Extract text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(temp_file.name)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(temp_file.name)
    elif file.filename.endswith(".wav"):
        text = transcribe_audio(temp_file.name)  # Transcribe audio
    else:
        return {"error": "Only PDF, DOCX, and WAV files are supported."}

    # Generate embeddings
    embeddings = embedding_model.encode([text]).astype(np.float32)

    # Store embeddings in FAISS
    if session_id not in file_embeddings:
        file_embeddings[session_id] = faiss.IndexFlatL2(dimension)
    
    file_embeddings[session_id].add(embeddings)

    return {"message": "File uploaded and indexed for retrieval."}

# Chat endpoint with Web RAG
@app.post("/chat/")
async def chat_with_llama(request: ChatRequest):
    session_id = request.session_id
    prompt = request.prompt
    language = request.language
    url = request.url

    # Translate prompt if needed
    if language != "en":
        prompt = translator.translate(prompt, src=language, dest="en").text

    # Generate embedding
    embedding = embedding_model.encode([prompt]).astype(np.float32)

    # Initialize session memory
    if session_id not in session_memory:
        session_memory[session_id] = faiss.IndexFlatL2(dimension)
        chat_history[session_id] = []

    memory_index = session_memory[session_id]

    # Retrieve past chat context
    retrieved_text = "New session. No past context found."
    if memory_index.ntotal > 0:
        _, I = memory_index.search(embedding, 1)
        retrieved_idx = int(I[0][0])
        if retrieved_idx < len(chat_history[session_id]):
            retrieved_text = chat_history[session_id][retrieved_idx]

    # Retrieve relevant context from uploaded files
    if session_id in file_embeddings and file_embeddings[session_id].ntotal > 0:
        _, file_I = file_embeddings[session_id].search(embedding, 1)
        retrieved_text += f"\nRelevant document content: {file_I}"

    # Retrieve data from website
    if url:
        web_text = scrape_website(url)
        if web_text != "No useful content found.":
            web_embedding = embedding_model.encode([web_text]).astype(np.float32)
            if session_id not in web_embeddings:
                web_embeddings[session_id] = faiss.IndexFlatL2(dimension)
            web_embeddings[session_id].add(web_embedding)
            retrieved_text += f"\nWeb context: {web_text[:500]}..."  # Limit to 500 chars

    # Store embedding and history
    memory_index.add(embedding)
    if len(chat_history[session_id]) >= MAX_MEMORY:
        chat_history[session_id].pop(0)
    chat_history[session_id].append(prompt)

    # Generate response using Ollama
    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        ai_response = response.get("message", "Sorry, I couldn't generate a response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

    return {"session_id": session_id, "retrieved_context": retrieved_text, "response": ai_response}
