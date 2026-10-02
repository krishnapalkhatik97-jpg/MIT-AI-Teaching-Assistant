from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scripts.rag import ask_question


app = FastAPI(title="MIT AI Teaching Assistant")


# Allow Vite frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "MIT AI Teaching Assistant API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/ask")
def ask(data: dict):
    question = data.get("question", "").strip()

    if not question:
        return {
            "error": "Question is required"
        }

    answer, sources = ask_question(question)

    return {
        "answer": answer,
        "sources": [
            {
                "lecture": source["lecture"],
                "chunk_id": source["chunk_id"],
                "distance": source["distance"],
            }
            for source in sources
        ],
    }