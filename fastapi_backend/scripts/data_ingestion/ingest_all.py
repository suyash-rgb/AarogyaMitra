# scripts/data_ingestion/ingest_all.py
import json
import uuid
import os
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
QDRANT_STORAGE = BASE_DIR / "data" / "qdrant_storage"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

def run_ingestion():
    print(f"[1/4] Loading FastEmbed model ({EMBEDDING_MODEL})...")
    embed_model = TextEmbedding(model_name=EMBEDDING_MODEL)

    print(f"[2/4] Initializing local Qdrant at {QDRANT_STORAGE}...")
    QDRANT_STORAGE.mkdir(parents=True, exist_ok=True)
    client = QdrantClient(path=str(QDRANT_STORAGE))

    collections = ["schemes_kb", "clinical_triage_kb", "medicines_kb"]
    
    # 1. Initialize Collections and Payload Indexes
    for coll in collections:
        if not client.collection_exists(coll):
            client.create_collection(
                collection_name=coll,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
            )
            print(f"Created collection: {coll}")
        else:
            print(f"Collection already exists: {coll}")

        # State-Aware Backdoor Payload Indexes
        for field in ["jurisdiction_level", "state_code", "scheme_name", "doc_type"]:
            try:
                client.create_payload_index(
                    collection_name=coll,
                    field_name=f"metadata.{field}",
                    field_schema=models.PayloadSchemaType.KEYWORD
                )
            except Exception:
                pass

    # 2. Iterate through generated JSONL files
    for coll in collections:
        coll_folder = PROCESSED_DIR / coll
        if not coll_folder.exists():
            print(f"Folder not found: {coll_folder}")
            continue

        jsonl_files = list(coll_folder.glob("*.jsonl"))
        print(f"\n[3/4] Ingesting {len(jsonl_files)} files into '{coll}'...")

        for jf in jsonl_files:
            texts, ids, metadatas = [], [], []
            with open(jf, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    item = json.loads(line)
                    texts.append(item["text"])
                    ids.append(item.get("id", str(uuid.uuid4())))
                    metadatas.append(item["metadata"])

            if not texts:
                continue

            # Compute embeddings
            embeddings = list(embed_model.embed(texts))

            # Batch upsert into Qdrant using deterministic UUIDs
            points = [
                models.PointStruct(
                    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{coll}_{item_id}")),
                    vector=emb.tolist(),
                    payload={"text": t, "metadata": m}
                )
                for item_id, t, m, emb in zip(ids, texts, metadatas, embeddings)
            ]

            batch_size = 128
            for i in range(0, len(points), batch_size):
                client.upsert(collection_name=coll, points=points[i:i + batch_size])

            print(f"  -> Ingested {len(points)} records from {jf.name}")

    print("\n[4/4] Ingestion successfully completed.")

if __name__ == "__main__":
    run_ingestion()
