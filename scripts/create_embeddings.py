from pathlib import Path
import json
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

CHUNKS_PATH = BASE_DIR / "data" / "chunks.json"
INDEX_PATH = BASE_DIR / "data" / "faiss_index.index"
METADATA_PATH = BASE_DIR / "data" / "metadata.pkl"

# -----------------------------
# Load chunks
# -----------------------------
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [chunk["text"] for chunk in chunks]

print(f"Loaded {len(texts)} chunks")

# -----------------------------
# Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embeddings created!")

# -----------------------------
# Create FAISS index
# -----------------------------
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# -----------------------------
# Save index
# -----------------------------
faiss.write_index(index, str(INDEX_PATH))

with open(METADATA_PATH, "wb") as f:
    pickle.dump(chunks, f)

print("FAISS index saved!")
print(f"Total vectors: {index.ntotal}")