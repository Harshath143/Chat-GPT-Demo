from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import faiss
import numpy as np
import ollama
from sentence_transformers import SentenceTransformer

# Initialize FastAPI app
app = FastAPI()

# Load sentence transformer model for embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Dictionary to store FAISS memory per session
session_memory = {}

# FAISS settings
dimension = 384  # Embedding size of MiniLM
index = faiss.IndexFlatL2(dimension)  # L2 distance index

# BaseModel for API requests
class ChatRequest(BaseModel):
    session_id: str
    prompt: str

class EndSessionRequest(BaseModel):
    session_id: str

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI is working!"}

# Chat endpoint
@app.post("/chat/")
async def chat_with_llama(request: ChatRequest):
    session_id = request.session_id
    prompt = request.prompt

    # Generate embedding for the prompt
    embedding = embedding_model.encode([prompt]).astype(np.float32)

    # Store session-based memory
    if session_id not in session_memory:
        session_memory[session_id] = faiss.IndexFlatL2(dimension)

    memory_index = session_memory[session_id]

    # Retrieve past context (if available)
    retrieved_text = "New session. No past context found."
    if memory_index.ntotal > 0:
        _, I = memory_index.search(embedding, 1)  # Retrieve closest memory
        retrieved_text = "Previous context found. Answering based on past chats."

    # Store the new embedding
    memory_index.add(embedding)

    # Use Ollama's local Llama 3 model
    try:
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        ai_response = response.get("response", {}).get("content", "Sorry, I couldn't generate a response.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

    return {
        "session_id": session_id,
        "retrieved_context": retrieved_text,
        "response": ai_response
    }

# Endpoint to clear session memory
@app.post("/end_session/")
async def end_session(request: EndSessionRequest):
    session_id = request.session_id
    if session_id in session_memory:
        del session_memory[session_id]
        return {"message": f"Session {session_id} memory cleared."}
    else:
        return {"message": "Session not found."}
