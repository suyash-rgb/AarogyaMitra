"""
Refined EkaCare Datasets Preprocessing & ChatML Conversion Script
Author: AarogyaMitra Team
Target Output: datasets/fine-tuning/ekacare-clean.json (750 Indian Phrasing & OTC ChatML Pairs)
"""

import os
import re
import json
import random
import pandas as pd
from datasets import load_dataset
from huggingface_hub import hf_hub_download

random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "fine-tuning")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ekacare-clean.json")
UNCLEAN_JSON = os.path.join(OUTPUT_DIR, "unclean_ekacare_clinical_notes.json")
UNCLEAN_MD = os.path.join(OUTPUT_DIR, "unclean_ekacare_clinical_notes.md")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(s: str) -> str:
    if not s or str(s).strip().lower() in ["nan", "none", "null"]:
        return ""
    return re.sub(r'\s+', ' ', str(s)).strip()

DRUG_USER_TEMPLATES = [
    "What is {brand_name} and what active ingredient does it have?",
    "I was prescribed {brand_name}. What is its active salt composition and main therapeutic use?",
    "Can you tell me the generic active salt in {brand_name} and its medical category?",
    "What kind of medicine is {brand_name} and what active component does it contain?",
    "I bought {brand_name} over the counter. What active component does it have and what safety cautions should I follow?"
]

def convert_drug_mcqa_row(row) -> dict:
    brand = clean_text(row.get("medication_name"))
    salt = clean_text(row.get("generic_name"))
    category = clean_text(row.get("therapeutic_class")) or "General Medication"
    
    tpl = random.choice(DRUG_USER_TEMPLATES)
    u_msg = tpl.format(brand_name=brand)
    
    ast_msg = (
        f"{brand} contains {salt}. It belongs to the {category} class. "
        f"Always use it as advised by your doctor or pharmacist, and ensure you do not combine it "
        f"with other medicines containing {salt} to prevent accidental overdose."
    )
    
    return {
        "messages": [
            {
                "role": "system",
                "content": "You are AarogyaMitra Health Advisor. Provide accurate Indian medicine guidance and mention safety cautions."
            },
            {
                "role": "user",
                "content": u_msg
            },
            {
                "role": "assistant",
                "content": ast_msg
            }
        ]
    }

CHATTER_PATTERNS = [
    r'काय काय झालेलं', r'काय त्रास आहे', r'केव्हांपासून', r'मला सांग', r'संगितलं का',
    r'batao', r'kya ho raha hai', r'tell me', r'how are you', r'hann'
]

def is_chatter(line: str) -> bool:
    line_lower = line.lower()
    for pat in CHATTER_PATTERNS:
        if re.search(pat, line_lower):
            return True
    return False

def process_clinical_note(row) -> list:
    text = clean_text(row.get("text"))
    if not text or len(text) < 15:
        return []
    
    raw_lines = [clean_text(l) for l in re.split(r'[.\n\?]+', text) if clean_text(l)]
    
    symptom_items = []
    rx_items = []
    
    for l in raw_lines:
        if is_chatter(l):
            continue
        l_lower = l.lower()
        if any(kw in l_lower for kw in ["tab", "tablet", "syr", "inj", "capsule", "advice", "advices", "after food", "before food", "tds", "bd", "sos", "mg"]):
            rx_items.append(l)
        else:
            if len(l.split()) >= 2:
                symptom_items.append(l)
                
    sys_msg = "You are AarogyaMitra Health Advisor, an empathetic AI clinical assistant for Indian healthcare contexts."
    pairs = []
    
    if symptom_items:
        clean_symptoms = ". ".join(symptom_items[:3])
        if re.search(r'[\u0900-\u097F]', clean_symptoms):
            u_msg = f"Doctor, I am having these symptoms: {clean_symptoms}. What advice should I follow?"
        else:
            u_msg = f"Doctor, I am experiencing: {clean_symptoms}. What could be the issue and what advice should I follow?"
            
        if rx_items:
            clean_rx = ". ".join(rx_items[:3])
            ast_msg = (
                f"Based on your symptoms ({symptom_items[0]}), clinical evaluation suggests monitoring your condition closely. "
                f"Your prescribed treatment/advice includes: {clean_rx}. "
                f"Please take any medications strictly as prescribed, stay hydrated, and consult a doctor if severe symptoms persist."
            )
        else:
            ast_msg = (
                f"Thank you for sharing your symptoms ({symptom_items[0]}). "
                f"It is recommended to rest, stay well hydrated, and visit a nearby primary health center or clinic for a physical examination."
            )
            
        pairs.append({
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": u_msg},
                {"role": "assistant", "content": ast_msg}
            ]
        })

    if rx_items:
        clean_rx = ". ".join(rx_items[:4])
        u_msg = f"Doctor, how should I take these prescribed medications: {clean_rx}?"
        ast_msg = (
            f"Here is your medication guidance: {clean_rx}. "
            f"Be sure to follow instructions carefully (e.g., taking tablets before or after food as indicated), "
            f"do not skip doses, and consult your physician or pharmacist if you experience any adverse effects."
        )
        pairs.append({
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": u_msg},
                {"role": "assistant", "content": ast_msg}
            ]
        })
        
    return pairs

def main():
    print("=== Processing & Cleaning EkaCare Datasets ===")
    
    # 1. Indian Drug MCQA
    print("[1/3] Loading ekacare/indian_drug_mcqa...")
    drug_file = hf_hub_download(repo_id="ekacare/indian_drug_mcqa", filename="data/test-00000-of-00001.parquet", repo_type="dataset")
    df_drug = pd.read_parquet(drug_file, engine="fastparquet")
    
    drug_pairs = []
    for _, row in df_drug.iterrows():
        brand = clean_text(row.get("medication_name"))
        salt = clean_text(row.get("generic_name"))
        if brand and salt:
            drug_pairs.append(convert_drug_mcqa_row(row))
            
    print(f"      Converted {len(drug_pairs)} clean Drug ChatML pairs.")

    # 2. Clinical Notes Dataset
    print("[2/3] Loading ekacare/clinical_note_generation_dataset...")
    f0 = hf_hub_download("ekacare/clinical_note_generation_dataset", "test-00000.parquet", repo_type="dataset")
    f1 = hf_hub_download("ekacare/clinical_note_generation_dataset", "test-00001.parquet", repo_type="dataset")
    df_clin = pd.concat([pd.read_parquet(f0), pd.read_parquet(f1)], ignore_index=True)
    
    # Export raw unclean datasets for inspection
    raw_notes = []
    for idx, row in df_clin.iterrows():
        raw_notes.append({
            "index": idx + 1,
            "session_id": str(row.get("session_id")),
            "raw_text": str(row.get("text")).strip()
        })
        
    with open(UNCLEAN_JSON, "w", encoding="utf-8") as f:
        json.dump(raw_notes, f, ensure_ascii=False, indent=2)
        
    with open(UNCLEAN_MD, "w", encoding="utf-8") as f:
        f.write("# Raw Unclean EkaCare Clinical Notes Dataset\n\n")
        f.write("This file contains the 156 raw, unedited transcribed clinical notes from `ekacare/clinical_note_generation_dataset`.\n\n")
        for item in raw_notes:
            f.write(f"### Note #{item['index']} (Session ID: `{item['session_id']}`)\n")
            f.write(f"```text\n{item['raw_text']}\n```\n\n")
            
    print(f"      Exported raw dataset to {UNCLEAN_JSON} and {UNCLEAN_MD}")

    clinical_pairs = []
    for _, row in df_clin.iterrows():
        clinical_pairs.extend(process_clinical_note(row))
        
    print(f"      Converted {len(clinical_pairs)} clean Clinical ChatML pairs.")

    # 3. Assemble target 750 dataset
    TARGET_TOTAL = 750
    random.shuffle(drug_pairs)
    random.shuffle(clinical_pairs)
    
    num_clin = min(214, len(clinical_pairs))
    num_drug = TARGET_TOTAL - num_clin
    
    final_pairs = drug_pairs[:num_drug] + clinical_pairs[:num_clin]
    random.shuffle(final_pairs)
    
    print(f"[3/3] Exporting {len(final_pairs)} ChatML pairs (Drug: {num_drug}, Clinical: {num_clin})...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_pairs, f, ensure_ascii=False, indent=2)
        
    print(f"SUCCESS: Exported clean dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
