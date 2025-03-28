# ChatGPT Demo - AI-Powered Web RAG System

This project is a **ChatGPT-like AI-powered web application** that integrates **FastAPI** as the backend and **JavaScript (React/Vanilla JS)** as the frontend. It supports **web scraping, document processing (PDF/DOCX), audio transcription (Vosk), FAISS-based memory, and AI-powered chatbot responses** using **Ollama's Llama 3 model**.

## 🔥 Features
- **AI Chatbot** powered by **Llama 3** via **Ollama**
- **Web Scraping** for retrieving information from URLs
- **Document Processing** (PDF, DOCX) using PyMuPDF and python-docx
- **Speech-to-Text** using Vosk (for `.wav` files)
- **Memory-based Retrieval** using FAISS
- **Multilingual Support** via Google Translate API
- **User Session Management**
- **Interactive UI** similar to ChatGPT
- **Robust API Endpoints** for seamless integration
- **Optimized Performance** for handling multiple user queries
- **Scalable Backend** to support large datasets and AI processing

---
## 🚀 Installation and Setup

### 1️⃣ Prerequisites
Ensure you have the following installed:
- **Python 3.9+**
- **Node.js (for frontend - optional)**
- **FastAPI** (`pip install fastapi`)
- **Uvicorn** (`pip install uvicorn`)
- **FAISS** (`pip install faiss-cpu`)
- **Ollama** ([Install Ollama](https://ollama.ai/download))
- **Llama 3 Model** (`ollama pull llama3`)
- **Vosk Model** (download `vosk-model-small-en-us-0.15` from [Vosk](https://alphacephei.com/vosk/models))

---
### 2️⃣ Backend Setup
Clone the repository:
```bash
$ git clone https://github.com/Harshath143/Chat-GPT-Demo.git
$ cd Chat-GPT-Demo/backend
```

Create a virtual environment and install dependencies:
```bash
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
$ pip install -r requirements.txt
```

Run FastAPI server:
```bash
$ uvicorn main:app --reload
```
Backend will be available at `http://127.0.0.1:8000`.

---
### 3️⃣ Frontend Setup
Navigate to the frontend folder:
```bash
$ cd ../frontend
```
For **Vanilla JavaScript** setup:
- Just open `index.html` in a browser.

For **React** setup:
```bash
$ npm install
$ npm start
```
Frontend will be available at `http://localhost:3000`.

---
## 🔗 API Endpoints

### 1️⃣ Root Endpoint
```
GET /
```
Response:
```json
{ "message": "Welcome to Web RAG API" }
```

### 2️⃣ Upload a File
```
POST /upload/
```
**Request Parameters:**
- `session_id`: Unique session ID
- `file`: PDF/DOCX/WAV file

**Response:**
```json
{ "message": "File uploaded and indexed for retrieval." }
```

### 3️⃣ Chat Endpoint (AI-powered response)
```
POST /chat/
```
**Request Body:**
```json
{
  "session_id": "user123",
  "prompt": "What is AI?",
  "language": "en",
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "session_id": "user123",
  "retrieved_context": "Relevant document content...",
  "response": "AI is..."
}
```

---
## 📡 Backend & Frontend Integration

1️⃣ The **frontend** sends user queries via JavaScript `fetch` requests to the FastAPI backend.

2️⃣ The **backend** processes:
   - **Retrieves previous chat memory** using FAISS.
   - **Fetches document/web-based context** if available.
   - **Generates an AI response** using the **Ollama Llama 3 model**.

3️⃣ The **response is returned** to the frontend and displayed in the chat UI.

### Example JavaScript Fetch Request
```js
async function sendMessage(prompt) {
    const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            session_id: "user123",
            prompt: prompt,
            language: "en",
        })
    });
    const data = await response.json();
    console.log(data.response);
}
```

---
## 💡 Future Enhancements
- **Session Persistence** (Store history in a database)
- **Advanced File Processing** (Support more formats)
- **Improved UI/UX**
- **Customizable AI Models** for different applications
- **Cloud Deployment** for scalable infrastructure
- **Enhanced Logging & Monitoring** for AI performance analysis

---
## 🛠️ Contributing
1. **Fork the repo**
2. **Create a new branch** (`feature-branch`)
3. **Commit changes** (`git commit -m "Added new feature"`)
4. **Push to GitHub** (`git push origin feature-branch`)
5. **Create a pull request**

---
## 📜 License
This project is open-source and available under the **MIT License**.

🚀 **Happy Coding!** 🚀

