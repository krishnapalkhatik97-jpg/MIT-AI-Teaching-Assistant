from pathlib import Path
import pickle
import requests
import faiss
from sentence_transformers import SentenceTransformer


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "data" / "faiss_index.index"
METADATA_PATH = BASE_DIR / "data" / "metadata.pkl"


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print("Loading embedding model...")

model_path = (
    r"C:\Users\Krishna Pal\.cache\huggingface\hub"
    r"\models--sentence-transformers--all-MiniLM-L6-v2"
    r"\snapshots\1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
)

model = SentenceTransformer(model_path)


# ============================================================
# LOAD FAISS INDEX + METADATA
# ============================================================

print("Loading FAISS index...")

index = faiss.read_index(str(INDEX_PATH))

with open(METADATA_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Loaded {index.ntotal} vectors")


# ============================================================
# CONVERSATION MEMORY
# ============================================================

conversation_history = []


# ============================================================
# ASK QUESTION
# ============================================================

def ask_question(query):

    # --------------------------------------------------------
    # 1. Convert question into embedding
    # --------------------------------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )


    # --------------------------------------------------------
    # 2. Retrieve relevant chunks from FAISS
    # --------------------------------------------------------

    k = 5

    distances, indices = index.search(
        query_embedding,
        k
    )

    retrieved_chunks = []

    # Smaller distance = more similar
    DISTANCE_THRESHOLD = 1.35

    for idx, distance in zip(indices[0], distances[0]):

        if idx != -1 and distance <= DISTANCE_THRESHOLD:

            retrieved_chunks.append({
                "lecture": chunks[idx]["lecture"],
                "chunk_id": chunks[idx]["chunk_id"],
                "text": chunks[idx]["text"],
                "distance": float(distance)
            })


    # --------------------------------------------------------
    # 3. Build lecture context
    # --------------------------------------------------------

    context_parts = []

    for item in retrieved_chunks:

        context_parts.append(
            f"Lecture: {item['lecture']}\n"
            f"Chunk ID: {item['chunk_id']}\n"
            f"Content:\n{item['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)


    # --------------------------------------------------------
    # 4. Build conversation history
    # --------------------------------------------------------

    history_text = ""

    if conversation_history:

        history_parts = []

        # Only keep the last 6 exchanges
        for message in conversation_history[-6:]:

            history_parts.append(
                f"{message['role'].upper()}: {message['content']}"
            )

        history_text = "\n".join(history_parts)


    # --------------------------------------------------------
    # 5. Teaching Prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI Teaching Assistant for MIT 6.0002.

Your job is to teach the student, not just give a short answer.

IMPORTANT RULES:

1. Use ONLY the lecture context provided below for factual information.

2. Do NOT use outside knowledge.

3. Do NOT invent facts, examples, formulas, numerical examples,
   or explanations that are not supported by the lecture context.

4. If the context does not contain enough information to answer
   the question, say:

"I couldn't find enough information in the provided MIT lectures."

5. Explain concepts in a beginner-friendly way.

6. You may use an analogy ONLY if the lecture context contains
   or supports that analogy.

7. If the question involves a process or algorithm, explain it
   step-by-step using information from the lectures.

8. If the lecture gives an example, use that example.

9. Ignore retrieved chunks that are not directly relevant to
   the student's question.

10. Every factual claim should be supported by the retrieved
    lecture context.

11. Keep the answer focused on the student's question.

12. Use the conversation history only to understand references
    such as "it", "this", "that", or follow-up questions.

13. Do not treat information from the conversation history as
    lecture evidence. Lecture context is the source of truth.

ANSWER FORMAT:

### Explanation

Give a clear and beginner-friendly explanation.

### Intuition

Give an intuitive explanation or analogy ONLY when supported
by the lecture context.

### Example

Give an example ONLY if the lecture context contains one.

If there is no suitable example, say:

"No specific example was provided in the retrieved lecture context."

### Key Takeaway

Give 1-3 important points the student should remember.

### Sources

List the lecture names and chunk IDs actually used.

------------------------------------------------------------

CONVERSATION HISTORY:

{history_text}

------------------------------------------------------------

LECTURE CONTEXT:

{context}

------------------------------------------------------------

STUDENT QUESTION:

{query}

"""


    # --------------------------------------------------------
    # 6. Send request to local Ollama
    # --------------------------------------------------------

    try:

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "qwen3:1.7b",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=120
        )

    except requests.exceptions.ConnectionError:

        return (
            "Error: Ollama is not running. "
            "Please start Ollama and try again.",
            retrieved_chunks
        )

    except requests.exceptions.Timeout:

        return (
            "Error: Ollama took too long to respond.",
            retrieved_chunks
        )


    # --------------------------------------------------------
    # 7. Handle Ollama errors
    # --------------------------------------------------------

    if response.status_code != 200:

        return (
            f"Error communicating with Ollama: {response.text}",
            retrieved_chunks
        )


    # --------------------------------------------------------
    # 8. Get generated answer
    # --------------------------------------------------------

    result = response.json()

    answer = result["message"]["content"]


    # --------------------------------------------------------
    # 9. Save conversation memory
    # --------------------------------------------------------

    conversation_history.append({
        "role": "student",
        "content": query
    })

    conversation_history.append({
        "role": "assistant",
        "content": answer
    })


    return answer, retrieved_chunks


# ============================================================
# CHAT LOOP
# ============================================================

print("\nMIT AI Teaching Assistant")
print("Type 'exit' to quit.\n")


while True:

    query = input("You: ").strip()


    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    if query.lower() == "exit":

        print("Goodbye!")

        break


    # --------------------------------------------------------
    # Empty question
    # --------------------------------------------------------

    if not query:

        print("Please enter a question.\n")

        continue


    # --------------------------------------------------------
    # Clear conversation
    # --------------------------------------------------------

    if query.lower() == "clear":

        conversation_history.clear()

        print("\nConversation memory cleared.\n")

        continue


    print("\nThinking...\n")


    # --------------------------------------------------------
    # Ask RAG system
    # --------------------------------------------------------

    answer, sources = ask_question(query)


    # --------------------------------------------------------
    # Display answer
    # --------------------------------------------------------

    print("=" * 80)
    print("ANSWER")
    print("=" * 80)

    print(answer)


    # --------------------------------------------------------
    # Display retrieved sources
    # --------------------------------------------------------

    print("\n" + "=" * 80)
    print("RETRIEVED SOURCES")
    print("=" * 80)


    for i, source in enumerate(sources, start=1):

        print(f"\n--- Source {i} ---")

        print(f"Lecture: {source['lecture']}")

        print(f"Chunk ID: {source['chunk_id']}")

        print(f"Distance: {source['distance']:.4f}")

        print(source["text"][:400])


    print()