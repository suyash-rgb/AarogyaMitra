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
    src_file = os.path.join(base_dir, "datasets", "rag vector-db", "Beneficiary Identification System Guidelines.pdf")
    tgt_file = os.path.join(base_dir, "data", "processed", "schemes_kb", "bis_guidelines.jsonl")
    os.makedirs(os.path.dirname(tgt_file), exist_ok=True)

    print(f"Processing: {src_file}")
    reader = pypdf.PdfReader(src_file)
    full_text = ""
    for page_idx, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        # Strip recurring headers and footers
        t = re.sub(r'(?i)National\s+Health\s+Agency\s+Guidelines.*', '', t)
        t = re.sub(r'(?i)Pradhan\s+Mantri\s+Jan\s+Arogya\s+Yojana.*', '', t)
        t = re.sub(r'\bPage\s+\d+\s+of\s+\d+\b', '', t)
        t = re.sub(r'\b\d+\b\s*$', '', t)
        full_text += "\n" + t

    chunks = recursive_chunk(full_text, chunk_size=800, overlap=150)
    records = []
    for idx, chunk in enumerate(chunks, start=1):
        record = {
            "id": f"bis_guidelines_{idx:04d}",
            "text": chunk,
            "metadata": {
                "source_file": "Beneficiary Identification System Guidelines.pdf",
                "target_collection": "schemes_kb",
                "jurisdiction_level": "CENTRAL",
                "state_code": "ALL",
                "scheme_name": "PM-JAY",
                "doc_type": "eligibility_guidelines",
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
