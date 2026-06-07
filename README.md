# 🌐 LinguaFlow — Language Translation Tool

**CodeAlpha AI Internship — Task 1**

A sleek, AI-powered language translation web app built with **Python** and **Streamlit**. Translate text between 100+ languages with just a few clicks. Features built-in **text-to-speech** so you can hear your translations too.

---

## ✨ Features

- **Translate between 100+ languages** using Google Translate API (no API key needed)
- **Smart language selection** — pick source and target from a clean dropdown
- **Text-to-Speech** — hear the translated text spoken aloud (works for 50+ languages)
- **Real-time feedback** with loading spinners and clear error handling
- **Clean, modern UI** — responsive design that works on desktop & mobile
- **One-click Clear** — reset the form instantly

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Core language |
| Streamlit | Web UI framework |
| googletrans 4.0 | Google Translate API wrapper (free, no key) |
| gTTS | Google Text-to-Speech |

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.8 or higher installed
- Git installed (for version control)

### Step-by-step

```bash
# 1. Navigate to the project folder
cd CodeAlpha/Task1_LanguageTranslationTool

# 2. (Recommended) Create a virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`.

---

## 📖 Example Usage

| Source Language | Target Language | Input | Output |
|----------------|----------------|-------|--------|
| English | Hindi | "Good morning, how are you?" | "शुभ प्रभात, आप कैसे हैं?" |
| English | French | "Welcome to my internship project" | "Bienvenue sur mon projet de stage" |
| English | Spanish | "Artificial Intelligence is the future" | "La inteligencia artificial es el futuro" |

---

## ⚠️ Limitations

- `googletrans` is a free, unofficial API — rate limits may apply for very heavy usage
- Text-to-Speech quality depends on the target language's gTTS support
- Internet connection required (both translation and TTS are cloud-based)

---

## 📄 License

This project is submitted as part of the **CodeAlpha AI Internship**.
