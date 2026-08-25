from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

transcript_folder = Path(__file__).parent.parent / "transcripts"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

all_chunks = []

for file in transcript_folder.glob("*.txt"):

    text = file.read_text(encoding="utf-8")

    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "lecture": file.stem,
            "chunk_id": i,
            "text": chunk
        })

output_file = Path(__file__).parent.parent / "data" / "chunks.json"

output_file.parent.mkdir(exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4, ensure_ascii=False)

print(f"✅ Total Chunks Created: {len(all_chunks)}")
print(f"✅ Saved to: {output_file}")