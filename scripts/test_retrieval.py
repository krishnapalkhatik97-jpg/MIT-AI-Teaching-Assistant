import pickle
import faiss
from sentence_transformers import SentenceTransformer


model_path = r"C:\Users\Krishna Pal\.cache\huggingface\hub\models--sentence-transformers--all-MiniLM-L6-v2\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"

print("Loading model...")

model = SentenceTransformer(model_path)

print("Loading FAISS...")

index = faiss.read_index("data/faiss_index.index")

with open("data/metadata.pkl", "rb") as f:
    chunks = pickle.load(f)


query = "What is gradient descent?"

query_embedding = model.encode(
    [query],
    convert_to_numpy=True
)

distances, indices = index.search(
    query_embedding,
    10
)


print("\nTOP 10 RESULTS")
print("=" * 80)

for rank, (idx, distance) in enumerate(
    zip(indices[0], distances[0]),
    start=1
):

    chunk = chunks[idx]

    print(f"\n{rank}. Distance: {distance:.4f}")
    print(f"Lecture: {chunk['lecture']}")
    print(f"Chunk ID: {chunk['chunk_id']}")
    print("-" * 80)

    print(
        chunk["text"][:300]
        .replace("\n", " ")
    )

print("\nDone.")