# 🤖 Emora AI – Emotion Aware AI Chatbot

Emora AI is an **Emotion-Aware Conversational AI Chatbot** that detects user emotions from text or voice and generates empathetic responses using AI.

The system analyzes emotional context over multiple messages to provide supportive and emotionally intelligent conversations.

---

## 🚀 Features

### 💬 Smart Chat System
- Real-time chatbot conversation
- AI-generated empathetic responses
- Typing animation
- Chat history storage

### 🧠 Emotion Detection
- Emotion detection using **RoBERTa (GoEmotions model)**
- Emotion confidence score
- Emotion context tracking across messages

### 📊 Emotion Analytics
- Emotion distribution chart
- Emotion timeline chart
- Total messages analytics

### 🎙 Voice Interaction
- Microphone speech input
- Audio file upload transcription
- Speech-to-text using **AssemblyAI**

### 🧾 Chat History
- SQLite-based chat storage
- Session-based chat history
- Load previous conversations
- Clear history option

---

# 🧠 System Architecture
User Input (Text / Voice)
↓
Speech-to-Text (Browser API / AssemblyAI)
↓
Emotion Detection (RoBERTa GoEmotions)
↓
Emotion Context Analysis
↓
Groq LLM Response Generation
↓
Chat UI Rendering
↓
SQLite Storage
↓
Emotion Analytics Dashboard


---

# 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLite

### AI Models
- RoBERTa (GoEmotions)
- Groq LLM (Llama 3)

### Frontend
- HTML
- CSS
- JavaScript
- AdminLTE Dashboard

### APIs
- Groq API
- AssemblyAI Speech API

---

# 📂 Project Structure


project/
│
├── app.py
├── response_generator.py
├── emotion_detector.py
├── emotion_context.py
├── memory_manager.py
├── database.py
│
├── templates/
│ └── index.html
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
│
├── chat_history.db
├── .env
├── .gitignore
└── README.md


---

# ⚙️ Installation

## 1️⃣ Clone the Repository


git clone https://github.com/An-andd/emora-ai-chatbot.git

cd emora-ai-chatbot


---

## 2️⃣ Install Dependencies


pip install -r requirements.txt


---

## 3️⃣ Add API Keys

Create a `.env` file:


ASSEMBLY_API_KEY=your_assembly_key
GROQ_API_KEY=your_groq_key


---

## 4️⃣ Run the Application


python app.py


Open:


http://127.0.0.1:5000


---

# 📊 Example Dashboard

The dashboard includes:

- Emotion distribution chart
- Emotion timeline chart
- Message analytics

---

# 🔐 Security

API keys are stored securely using **environment variables (.env)** and are not exposed in the repository.

---

# 🌟 Future Improvements

- Real-time facial emotion detection
- Multi-language emotion analysis
- Mental health support mode
- Mobile application integration
- Advanced conversation memory

---

# 👨‍💻 Author

**Anand Suresh**

Computer Science Engineering Student  
AI & Intelligent Systems Enthusiast

GitHub:  
https://github.com/An-andd

---

# 📜 License

This project is for **educational and research purposes**.