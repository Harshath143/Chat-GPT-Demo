# ChatGPT UI Clone - Web RAG System

## Introduction
This project is a **ChatGPT UI Clone** that integrates with a **FastAPI backend** to provide **Retrieval-Augmented Generation (RAG)** capabilities. It allows users to interact with an **AI-powered chatbot** that can process text, extract information from documents, transcribe audio, and retrieve relevant content from the web. The system leverages **FAISS for vector search**, **Ollama for Llama 3-based AI responses**, and supports **multiple data sources** for contextual augmentation.

## Features
- **FastAPI Backend** with endpoints for chat, file uploads, and web scraping.
- **Frontend (HTML, CSS, JavaScript)** for an interactive ChatGPT-like UI.
- **Vector Database (FAISS)** for efficient retrieval of past conversation context.
- **LLM Integration** using Ollama and Llama 3 model for response generation.
- **Document Processing** for PDFs, DOCX files, and WAV audio transcription.
- **Web Scraping** to fetch relevant content from a given URL.
- **Multilingual Support** via Google Translator API.

---

## System Requirements
Ensure you have the following installed:

- **Python 3.8+**
- **FastAPI**
- **FAISS**
- **Ollama** (with Llama 3 model installed)
- **Vosk (for speech-to-text)**
- **Sentence Transformers**
- **Node.js & npm** (for frontend development)

### Install Ollama and Llama 3
Ensure Ollama is installed on your system:
```sh
curl -fsSL https://ollama.ai/install.sh | sh
```
Download the **Llama 3 model**:
```sh
ollama pull llama3
```

---

## Backend Setup (FastAPI)

### 1. Install Dependencies
```sh
pip install fastapi uvicorn faiss-cpu numpy ollama vosk requests beautifulsoup4 fitz googletrans newspaper3k sentence-transformers python-docx
```

### 2. Run the FastAPI Server
```sh
uvicorn main:app --reload
```
The server will start at: `http://127.0.0.1:8000`

### 3. Backend Endpoints

| Method | Endpoint | Description |
|--------|------------|-------------|
| **GET** | `/` | Returns a welcome message |
| **POST** | `/chat/` | Generates AI responses with RAG support |
| **POST** | `/upload/` | Uploads and processes files for retrieval |

Example request to `/chat/`:
```json
{
    "session_id": "user123",
    "prompt": "What is AI?",
    "language": "en"
}
```

---

## Frontend Setup

### 1. Project Structure
```
Chat-GPT-Demo/
│── backend/
│── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│── README.md
│── Web_RAG.py (FastAPI backend)
```

### 2. Frontend (HTML, CSS, JavaScript)
Ensure the frontend interacts with FastAPI via `fetch` requests.

#### **HTML (index.html)**
```html
<input type="text" id="user-input" placeholder="Ask anything...">
<button id="send-btn"><i class="fa-solid fa-paper-plane"></i></button>
<div id="chat-output"></div>
```

#### **JavaScript (script.js)**
```js
document.getElementById("send-btn").addEventListener("click", async () => {
    const input = document.getElementById("user-input").value;
    const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: "user123",
            prompt: input,
            language: "en"
        })
    });
    const data = await response.json();
    document.getElementById("chat-output").innerHTML = data.response;
});
```

### 3. Start a Local Server
```sh
cd frontend
python -m http.server 5500  # Serves index.html
```
Then open `http://127.0.0.1:5500` in your browser.

---

## Deployment
### Deploy Backend with FastAPI on Render/Heroku
```sh
git init
git add .
git commit -m "Deploy Chat-GPT-Demo"
git push origin main
```

### Deploy Frontend on GitHub Pages / Vercel
- Host `index.html`, `styles.css`, `script.js` on GitHub.
- Use **GitHub Pages** or **Vercel** for hosting.

---

## Troubleshooting
- **CORS Errors?** Add CORS middleware in `main.py`:
  ```python
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
  ```
- **No AI Response?** Ensure `ollama` and `llama3` model are correctly installed.
  ```sh
  ollama run llama3 "Hello!"
  ```
- **FAISS Errors?** Ensure FAISS is installed:
  ```sh
  pip install faiss-cpu
  ```

---

## Conclusion
This project integrates **FastAPI, Ollama, FAISS, and a simple frontend** to create an interactive AI-powered chatbot. It supports **file uploads, web scraping, multilingual responses**, and **local memory storage** using FAISS.

🚀 Feel free to contribute and improve the project! Happy coding! 🎉

