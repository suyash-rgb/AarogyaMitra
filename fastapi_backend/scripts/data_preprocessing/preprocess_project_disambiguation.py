import os
import re
import json

def preprocess():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_file = os.path.join(base_dir, "datasets", "rag vector-db", "aarogyamitra_project_faq_and_entity_disambiguation_master.md")
    tgt_file = os.path.join(base_dir, "data", "processed", "schemes_kb", "project_disambiguation.jsonl")
    os.makedirs(os.path.dirname(tgt_file), exist_ok=True)

    print(f"Processing: {src_file}")
    with open(src_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into sections based on H3 (### Q) or H2 (##)
    sections = re.split(r'(?=\n###?\s+)', content)
    records = []
    chunk_counter = 1

    for sec in sections:
        sec_str = sec.strip()
        if not sec_str:
            continue
        
        # If very large section, chunk it further
        if len(sec_str) > 1000:
            lines = sec_str.split("\n")
            buf = ""
            for line in lines:
                buf += line + "\n"
                if len(buf) >= 800:
                    records.append({
                        "id": f"project_disambiguation_{chunk_counter:04d}",
                        "text": buf.strip(),
                        "metadata": {
                            "source_file": "aarogyamitra_project_faq_and_entity_disambiguation_master.md",
                            "target_collection": "schemes_kb",
                            "jurisdiction_level": "CENTRAL",
                            "state_code": "ALL",
                            "scheme_name": "AAROGYAMITRA_PROJECT",
                            "doc_type": "entity_disambiguation_faq",
                            "chunk_id": chunk_counter
                        }
                    })
                    chunk_counter += 1
                    buf = ""
            if buf.strip():
                records.append({
                    "id": f"project_disambiguation_{chunk_counter:04d}",
                    "text": buf.strip(),
                    "metadata": {
                        "source_file": "aarogyamitra_project_faq_and_entity_disambiguation_master.md",
                        "target_collection": "schemes_kb",
                        "jurisdiction_level": "CENTRAL",
                        "state_code": "ALL",
                        "scheme_name": "AAROGYAMITRA_PROJECT",
                        "doc_type": "entity_disambiguation_faq",
                        "chunk_id": chunk_counter
                    }
                })
                chunk_counter += 1
        else:
            records.append({
                "id": f"project_disambiguation_{chunk_counter:04d}",
                "text": sec_str,
                "metadata": {
                    "source_file": "aarogyamitra_project_faq_and_entity_disambiguation_master.md",
                    "target_collection": "schemes_kb",
                    "jurisdiction_level": "CENTRAL",
                    "state_code": "ALL",
                    "scheme_name": "AAROGYAMITRA_PROJECT",
                    "doc_type": "entity_disambiguation_faq",
                    "chunk_id": chunk_counter
                }
            })
            chunk_counter += 1

    with open(tgt_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Generated {len(records)} chunks -> {tgt_file}")

if __name__ == "__main__":
    preprocess()
