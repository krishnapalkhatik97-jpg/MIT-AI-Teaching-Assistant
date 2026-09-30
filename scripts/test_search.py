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
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Load FAISS
# -----------------------------
print("Loading FAISS index...")
index = faiss.read_index(str(INDEX_PATH))

with open(METADATA_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {index.ntotal} vectors")


# -----------------------------
# Ask question
# -----------------------------
query = input("\nAsk a question: ").strip()

if not query:
    print("Please enter a question.")
    exit()


# -----------------------------
# Create query embedding
# -----------------------------
query_embedding = model.encode(
    [query],
    convert_to_numpy=True
)


# -----------------------------
# Search
# -----------------------------
k = 10

distances, indices = index.search(query_embedding, k)


# -----------------------------
# Display results
# -----------------------------
print("\nTop Results:\n")

for i, idx in enumerate(indices[0], start=1):

    print("=" * 80)
    print(f"Result {i}")
    print(f"Distance: {distances[0][i-1]:.4f}")

    print(f"Lecture: {chunks[idx]['lecture']}")
    print(f"Chunk ID: {chunks[idx]['chunk_id']}")

    print("\nText:")
    print(chunks[idx]["text"])

    print()