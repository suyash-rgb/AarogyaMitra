import os
import re
import json
import pypdf


def recursive_chunk(text: str, chunk_size: int = 800, overlap: int = 150):
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunk = text[start:].strip()
            if chunk:
                chunks.append(chunk)
            break
        
        # Look for sentence boundary
        boundary = max(text.rfind('. ', start, end), text.rfind('?\n', start, end), text.rfind('; ', start, end))
        if boundary != -1 and boundary > start + chunk_size // 2:
            end = boundary + 1
        else:
            # Look for space
            space_boundary = text.rfind(' ', start, end)
            if space_boundary != -1 and space_boundary > start + chunk_size // 2:
                end = space_boundary
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap if end - overlap > start else end
    return chunks


def preprocess():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_file = os.path.join(base_dir, "datasets", "rag vector-db", "PM-JAY Process Flow at Empanelled Hospitals.pdf")
    tgt_file = os.path.join(base_dir, "data", "processed", "schemes_kb", "pmjay_process_flow.jsonl")
    os.makedirs(os.path.dirname(tgt_file), exist_ok=True)

    print(f"Processing: {src_file}")
    reader = pypdf.PdfReader(src_file)
    full_text = ""
    for page in reader.pages:
        t = page.extract_text() or ""
        t = re.sub(r'\bPage\s+\d+\b', '', t)
        full_text += "\n" + t

    chunks = recursive_chunk(full_text, chunk_size=700, overlap=100)
    records = []
    for idx, chunk in enumerate(chunks, start=1):
        record = {
            "id": f"pmjay_process_flow_{idx:04d}",
            "text": chunk,
            "metadata": {
                "source_file": "PM-JAY Process Flow at Empanelled Hospitals.pdf",
                "target_collection": "schemes_kb",
                "jurisdiction_level": "CENTRAL",
                "state_code": "ALL",
                "scheme_name": "PM-JAY",
                "doc_type": "hospital_workflow",
                "chunk_id": idx
            }
        }
        records.append(record)

    with open(tgt_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Generated {len(records)} chunks -> {tgt_file}")

if __name__ == "__main__":
    preprocess()
