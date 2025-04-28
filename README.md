# 🏥 Health Insurance Assistant (United States)

An intelligent, voice-enabled chatbot that helps users **learn about health insurance terms** and **find healthcare plans across U.S. states**.  
Built with **FastAPI** backend and **React.js** frontend, featuring smart memory, voice input, and direct insurer links.

---

## 🚀 Project Overview

- **Glossary Mode**: Explain insurance terms like deductible, copay, premium.
- **Plan Recommendation Mode**: Suggest top real insurance plans based on user's state.
- **Voice Input & Output**: Speak instead of typing!
- **Memory Sidebar**: See and reuse previous conversations.
- **Clickable Insurance Links**: Navigate directly to insurer sites.
- **US-Only Focus**: All plans are from the United States market.

---

## 💡 Tech Stack

| Technology | Usage |
|------------|-------|
| FastAPI    | Backend server (Python) |
| React.js   | Frontend chatbot UI |
| FAISS      | Search similar glossary/questions |
| Sentence Transformers | Smart semantic text understanding |
| HTML/CSS   | Responsive design |
| pyttsx3    | Voice output engine (optional) |

---

## 📂 Project Structure

```bash
backend/
  ├── main.py                # FastAPI API logic
  ├── glossary_cleaned.json    # Healthcare glossary dataset
  ├── plans_data_cleaned.jsonl  # US healthcare plans data
  └── company_links_smart_filled.json # Insurer websites

frontend/
  ├── src/
  │    ├── insurance_bot.jsx  # React chatbot component
  │    └── insurance_bot.css  # Frontend styles
  └── public/
       └── index.html
```

---

## 🔧 Local Development Setup

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit backend at: **http://127.0.0.1:8000**

### Frontend (React.js)

```bash
cd frontend
npm install
npm start
```

Visit frontend at: **http://localhost:3000**

---

## 🚀 Features Coming Soon

- Voice-only handsfree mode
- Plan filters: by age, income, or needs
- Mobile-friendly version
- Docker containerization for production

---

## 👩‍💼 Author

Developed with passion by **Aswin Ganesh Venkatramanan**  
[GitHub Profile 🔍](https://github.com/AswinGaneshVenkat)


---

# ✨ Your Personalized Healthcare Buddy Awaits!

