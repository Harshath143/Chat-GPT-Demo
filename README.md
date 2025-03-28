# ChatGPT Demo - Web RAG System

## Overview
This project is an AI-powered chatbot system that integrates **FastAPI** as the backend and a **ChatGPT-style UI** as the frontend. The system uses **Ollama with LLaMA 3**, **FAISS for vector search**, and **Vosk for speech-to-text processing**. It supports **document uploads**, **web scraping**, and **multilingual queries**.

![Project Screenshot](assets/screenshot.png)

---

## 🚀 Features
✅ **Chat with AI**: Uses Ollama's LLaMA 3 model for intelligent responses.  
✅ **Memory Storage**: Stores session-based memory using FAISS.  
✅ **Web Scraping**: Retrieves context from URLs for improved responses.  
✅ **Document Processing**: Extracts text from PDFs, DOCX, and transcribes WAV files.  
✅ **Speech Recognition**: Converts speech to text using Vosk.  
✅ **Multilingual Support**: Translates queries to English before processing.  
✅ **FastAPI Backend**: Provides API endpoints for interaction.  
✅ **Modern UI**: A ChatGPT-like frontend with a clean and user-friendly interface.  

---

## 🛠️ Tech Stack
**Frontend:**  
- HTML, CSS, JavaScript  
- Fetch API for backend communication  

**Backend:**  
- FastAPI (Python)  
- Ollama (LLaMA 3)  
- FAISS for vector search  
- Vosk for speech-to-text  
- BeautifulSoup for web scraping  
- Google Translate API for multilingual support  
- PyMuPDF & python-docx for document parsing  

---

## 📌 Setup Guide
### 🔧 1. Install Ollama & LLaMA 3
Make sure **Ollama** is installed and the **LLaMA 3** model is available:
```sh
ollama pull llama3
```

### 🔧 2. Clone the Repository
```sh
git clone https://github.com/Harshath143/Chat-GPT-Demo.git
cd Chat-GPT-Demo
```

### 🔧 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 🔧 4. Run FastAPI Backend
```sh
uvicorn main:app --reload
```

### 🔧 5. Start Frontend
Simply open `index.html` in a browser or serve with Live Server.

---

## 📡 API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/upload/` | POST | Uploads and processes files |
| `/chat/` | POST | Chat with AI using LLaMA 3 |

---

---

## 🔗 Live Demo
🚀 **Coming Soon!**

---

## 🤝 Contributing
Feel free to submit issues and pull requests!

---

## 📝 License
This project is licensed under MIT License.

