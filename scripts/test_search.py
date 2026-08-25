from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "data" / "faiss_index.index"
METADATA_PATH = BASE_DIR / "data" / "metadata.pkl"

# -----------------------------
# Load model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Load FAISS
# -----------------------------
index = faiss.read_index(str(INDEX_PATH))

with open(METADATA_PATH, "rb") as f:
    chunks = pickle.load(f)

# -----------------------------
# Ask a question
# -----------------------------
query = input("Ask a question: ")

query_embedding = model.encode([query])

distances, indices = index.search(query_embedding, k=3)

print("\nTop Results:\n")

for i, idx in enumerate(indices[0], start=1):
    print("=" * 80)
    print(f"Result {i}")
    print(chunks[idx]["text"])
    print()