from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Allow Python to find scripts/rag.py
sys.path.append(str(BASE_DIR / "scripts"))

# ============================================================
# IMPORT RAG
# ============================================================

from rag import ask_question


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="MIT AI Teaching Assistant",
    description="RAG-powered MIT 6.0002 AI Teaching Assistant",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class QuestionRequest(BaseModel):
    question: str


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MIT AI Teaching Assistant API is running!"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ============================================================
# ASK QUESTION
# ============================================================

@app.post("/ask")
def ask(request: QuestionRequest):

    answer, sources = ask_question(request.question)

    return {
        "answer": answer,
        "sources": sources
    }