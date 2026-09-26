import os
import json
import pandas as pd

def preprocess():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    src_file = os.path.join(base_dir, "datasets", "rag vector-db", "AyurGenixAI_Dataset.csv")
    tgt_file = os.path.join(base_dir, "data", "processed", "clinical_triage_kb", "ayurgenix_dataset.jsonl")
    os.makedirs(os.path.dirname(tgt_file), exist_ok=True)

    print(f"Processing: {src_file}")
    df = pd.read_csv(src_file)
    records = []
    for idx, row in df.iterrows():
        disease = str(row.get("Disease", "")).strip()
        symptoms = str(row.get("Symptoms", "")).strip()
        disease_symptom = f"{disease} ({symptoms})" if symptoms else disease
        formulation = str(row.get("Formulation", "")).strip()
        herbs = str(row.get("Ayurvedic Herbs", "") or row.get("Herbal/Alternative Remedies", "")).strip()
        dosage_prep = str(row.get("Diet and Lifestyle Recommendations", "") or row.get("Duration of Treatment", "")).strip()
        precautions = str(row.get("Risk Factors", "") or row.get("Complications", "") or row.get("Allergies (Food/Env)", "")).strip()

        line_text = f"Disease / Symptom: {disease_symptom} | Formulation: {formulation} | Active Botanical Ingredients: {herbs} | Dosage / Preparation: {dosage_prep} | Precautions: {precautions}"

        record = {
            "id": f"ayurgenix_{idx+1:04d}",
            "text": line_text,
            "metadata": {
                "source_file": "AyurGenixAI_Dataset.csv",
                "target_collection": "clinical_triage_kb",
                "jurisdiction_level": "CENTRAL",
                "state_code": "ALL",
                "scheme_name": "AYUSH",
                "doc_type": "herbal_formulation",
                "chunk_id": idx + 1
            }
        }
        records.append(record)

    with open(tgt_file, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Generated {len(records)} atomic records -> {tgt_file}")

if __name__ == "__main__":
    preprocess()
