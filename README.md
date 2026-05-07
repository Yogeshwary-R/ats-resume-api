![Python](https://img.shields.io/badge/Python-3.10+-3572A5?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=black)
![JWT](https://img.shields.io/badge/JWT-Auth-f59e0b?style=for-the-badge&logo=jsonwebtokens&logoColor=black)
![AI Powered](https://img.shields.io/badge/AI--Powered-Ollama-7c3aed?style=for-the-badge)

# 🎯 ATS Resume Scorer API

> A backend REST API that scores resumes against job descriptions and gives **AI-powered improvement suggestions** — built transparent. You see *exactly* why you scored 72%.

 
---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Resume Scoring** | Upload a PDF → get a % match score against any job description |
| 🤖 **AI Suggestions** | Ollama (gemma:2b) generates actionable improvement tips |
| 🔐 **JWT Auth** | Secure user accounts with bcrypt password hashing |
| 👁️ **Explainable** | See matched skills & missing skills — not a black box |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI + Uvicorn |
| Database | PostgreSQL (hosted on Supabase) |
| ORM | SQLAlchemy |
| Auth | JWT + bcrypt |
| AI Model | Ollama (gemma:2b) |
| PDF Parsing | pdfplumber + NLTK |
| Rate Limiting | slowapi |

---

## ⚙️ Concepts Implemented

`REST API` `JWT Authentication` `AI Integration` `File Upload (PDF)` `ORM` `Password Hashing` `Rate Limiting` `Input Validation` `Environment Variables` `NLP (NLTK)`

---

## 🔄 Request Flow

```
POST /resume/scan → JWT check → pdfplumber → NLTK scorer → Ollama AI → JSON result
```

---

## 📁 Project Structure

```
project/
├── main.py              # App entry point
├── config.py            # Settings & env config
├── .env                 # Secrets (never committed)
└── app/
    ├── routes/          # API routes
    ├── services/        # Business logic
    ├── models/          # Database schemas
    └── core/            # Security & database config
        
``` 
 
---

## 🚀 Run Locally

```bash
git clone  https://github.com/Yogeshwary-R/ats-resume-api.git 
cd ats-resume-api

pip install -r requirements.txt

cp .env.example .env    # Add your DB credentials & secrets

uvicorn main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) — FastAPI auto-generates interactive API docs.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new account |
| `POST` | `/auth/login` | Get JWT access token |
| `POST` | `/resume/scan` | Upload PDF + get score + AI tips |
| `GET` | `/resume/history` | View past scan results |

---

---

*Built with FastAPI · PostgreSQL · Ollama · Supabase · JWT authentication*
