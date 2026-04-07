# 🚀 Smart Talent Selection Engine

An AI-powered recruitment system that intelligently analyzes resumes and ranks candidates based on **semantic understanding**, not just keyword matching.

---

## 📌 Overview

In modern hiring, recruiters face:

* 1000+ resumes per job
* Poor keyword-based filtering
* Missed high-quality candidates

This system solves it using:

* Resume parsing
* Skill mapping
* AI-based ranking
* Justification engine

📄 Based on real hiring problems described in the system requirements.

---

## 🎯 Core Features

### 📄 1. Resume Upload System

* Supports: **PDF, DOCX, JPG, PNG**
* Bulk upload support
* Automatic storage in database

---

### 🧠 2. Resume Parsing & Profile Extraction

Extracts structured data:

* Skills
* Education
* Projects
* Experience

Handles messy real-world resumes.

---

### 🧩 3. Skill Mapper (Semantic Layer)

* Converts raw skills into meaningful categories
* Example:

  * "React" → Frontend Development
  * "PyTorch" → Machine Learning

---

### 📊 4. Job Description Matching

* Upload a job description
* System compares with all candidates

---

### 🏆 5. Candidate Ranking Engine

* Generates score (0–100%)
* Considers:

  * Skill match
  * Experience depth
  * Project relevance

---

### 🤖 6. AI Justification Engine

Multi-layer fallback system:

1. Gemini API (Primary)
2. Ollama (Local LLM)
3. Rule-based fallback

Example output:

> "Strong match for backend role with Python and database experience"

---

## 🏗️ System Architecture

```
[ Resume Upload ]
        ↓
[ Parsing Engine ]
        ↓
[ Skill Mapper ]
        ↓
[ Database (PostgreSQL) ]
        ↓
[ JD Upload ]
        ↓
[ Ranking Engine ]
        ↓
[ AI Justifier ]
        ↓
[ Frontend Dashboard ]
```

---

## 🛠️ Tech Stack

### 🔹 Backend

* FastAPI (Python)
* PostgreSQL
* Uvicorn

### 🔹 Frontend

* React (Vite)

### 🔹 AI Layer

* Gemini API
* Ollama (Local LLM)

---

## 📂 Project Structure

```
smart-talent/
│
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── models/
│   │   ├── db/
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   └── package.json
│
└── README.md
```

---

# ⚙️ COMPLETE SETUP GUIDE

## 🔹 1. Prerequisites

Make sure you have:

* Python (>= 3.9)
* Node.js (>= 18)
* PostgreSQL
* Git

---

## 🔹 2. Clone Repository

```bash
git clone https://github.com/RUK692004/Smart_talent.git
cd smart-talent
```

---

# 🧠 BACKEND SETUP (FastAPI)

## 🔹 Step 1: Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

---

## 🔹 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔹 Step 3: Setup PostgreSQL Database

### Create Database

```sql
CREATE DATABASE resume_db;
```

---

### Update Database Config

Go to:

```
backend/app/db/database.py
```

Update:

```python
DB_NAME = "resume_db"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

---

## 🔹 Step 4: Run Backend Server

```bash
uvicorn app.main:app --reload --port 8001
```

Open:

```
http://127.0.0.1:8001/docs
```

---

# 💻 FRONTEND SETUP (React)

## 🔹 Step 1: Install Dependencies

```bash
cd frontend
npm install
```

---

## 🔹 Step 2: Start Frontend

```bash
npm run dev
```

Open:

```
http://localhost:5173
```

---

# 🤖 AI SETUP (IMPORTANT)

## 🔹 Option 1: Gemini API (Cloud)

1. Get API key from Google AI Studio
2. Create `.env` file in backend:

```
GEMINI_API_KEY=your_api_key_here
```

---

## 🔹 Option 2: Ollama (Local LLM)

Install Ollama:

👉 https://ollama.com

Run model:

```bash
ollama run gemma:2b
```

---

## 🔁 AI FALLBACK FLOW

```
Gemini → Ollama → Rule-Based
```

---

# 🧪 HOW TO USE

### 1. Upload Resumes

* Go to upload section
* Upload multiple resumes

### 2. Upload Job Description

* Enter JD details

### 3. View Ranking

* Candidates sorted by score

### 4. Click Candidate

* View AI justification

---

# 📊 SAMPLE OUTPUT

| Rank | Candidate | Score | Skills        | Justification             |
| ---- | --------- | ----- | ------------- | ------------------------- |
| 1    | Rohith    | 92%   | Python, Flask | Strong backend experience |

---

# 🚧 KNOWN LIMITATIONS

* Resume parsing may fail for complex layouts
* Gemini API has rate limits
* Ollama requires local setup

---

# 🚀 FUTURE IMPROVEMENTS

* pgvector semantic embeddings
* Advanced filtering
* Dashboard analytics
* Cloud deployment

---

# 👨‍💻 TEAM / AUTHOR

* Add your team members here

---

# ⭐ Final Note

This project demonstrates how AI can **transform recruitment from keyword filtering → intelligent talent selection**.

---

## 🙌 If you like this project

Give it a ⭐ on GitHub!
