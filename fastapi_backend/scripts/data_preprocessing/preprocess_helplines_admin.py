import os
import re
import json

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
        
        boundary = max(text.rfind('. ', start, end), text.rfind('| ', start, end), text.rfind('\n', start, end))
        if boundary != -1 and boundary > start + chunk_size // 2:
            end = boundary + 1
        else:
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
    src_file = os.path.join(base_dir, "datasets", "rag vector-db", "indian_public_health_helplines_and_administration_master.md")
    tgt_file = os.path.join(base_dir, "data", "processed", "clinical_triage_kb", "helplines_admin.jsonl")
    os.makedirs(os.path.dirname(tgt_file), exist_ok=True)

    print(f"Processing: {src_file}")
    with open(src_file, "r", encoding="utf-8") as f:
        full_text = f.read()

    chunks = recursive_chunk(full_text, chunk_size=850, overlap=150)
    records = []
    for idx, chunk in enumerate(chunks, start=1):
        record = {
            "id": f"helplines_admin_{idx:04d}",
            "text": chunk,
            "metadata": {
                "source_file": "indian_public_health_helplines_and_administration_master.md",
                "target_collection": "clinical_triage_kb",
                "jurisdiction_level": "CENTRAL",
                "state_code": "ALL",
                "scheme_name": "PUBLIC_HEALTH_HELPLINES",
                "doc_type": "helplines_administration",
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
