"""
ArogyaMitra Data Preprocessing Script: ChatDoctor Dataset
---------------------------------------------------------
Dataset Source: archive-ChatDoctor (HealthCareMagic-100k.json, iCliniq.json)
Target Output: 750 ChatML pairs stored in datasets/fine-tuning/chatdoctor-clean.json

Sampling Criteria:
- Filter for common primary care complaints: fatigue, mild fever, back pain, headache, acid reflux.
- Strictly exclude cases involving oncology, psychiatric crises, or complex inpatient procedures.

Cleaning & Preprocessing:
- Strip external doctor signatures, physician names, hospital advertising, phone numbers, disclaimers.
- Restructure doctor turns to consistently ask 1 or 2 targeted diagnostic follow-up questions before offering general advice.
- Truncate verbose clinical essays to concise responses strictly under 130 words.
"""

import os
import json
import re
import random
import unicodedata
from collections import defaultdict

# Fixed random seed for reproducibility
random.seed(42)

INPUT_DIR = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\archive-ChatDoctor"
OUTPUT_FILE = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\chatdoctor-clean.json"
TARGET_SIZE = 750

SYSTEM_PROMPT = "You are AarogyaMitra Health Advisor, an empathetic AI clinical assistant for Indian primary care healthcare contexts."

# Primary Care Categories & Keyword Patterns
CATEGORIES = {
    "fatigue": [r"\bfatigue\b", r"\btired\w*", r"\bexhaust\w*", r"\bletharg\w*", r"\blow energy\b", r"\bweakness\b"],
    "mild_fever": [r"\bfever\b", r"\bmild fever\b", r"\blow grade fever\b", r"\btemperature\b", r"\bchills\b"],
    "back_pain": [r"\bback pain\b", r"\blower back\b", r"\bupper back\b", r"\blumbar\b", r"\bback ache\b", r"\bspine pain\b"],
    "headache": [r"\bheadache\b", r"\bmigraine\b", r"\bhead pain\b", r"\btension headache\b", r"\bsinus headache\b"],
    "acid_reflux": [r"\bacid reflux\b", r"\bheartburn\b", r"\bgerd\b", r"\bacidity\b", r"\bacid indigestion\b", r"\bsour burp\w*", r"\bchest burn\w*"]
}

# Strict Exclusion Patterns (Oncology, Psychiatric Crises, Complex Inpatient Procedures)
EXCLUSIONS = [
    # Oncology
    r"\bcancer\b", r"\btumor\b", r"\btumour\b", r"\bchemo\w*", r"\bmalignan\w*", r"\bradiation\b", r"\bmetasta\w*", r"\blymphoma\b", r"\bleukemia\b", r"\bcarcinoma\b", r"\bsarcoma\b", r"\bbiopsy\b",
    # Psychiatric Crisis
    r"\bsuicid\w*", r"\bself harm\b", r"\bpsychosis\b", r"\bhallucinat\w*", r"\bschizophrenia\b", r"\bpsychiatric crisis\b", r"\bmania\b", r"\bbipolar\b",
    # Complex Inpatient Procedures
    r"\bsurger\w*", r"\bsurgical\b", r"\bicu\b", r"\bintubat\w*", r"\bventilat\w*", r"\bbypass\b", r"\bdialysis\b", r"\btransplant\b", r"\bcatheter\b", r"\bpost op\w*"
]

# Targeted Diagnostic Follow-Up Questions per Category
DIAGNOSTIC_QUESTIONS = {
    "fatigue": [
        "How long have you been experiencing this fatigue, and do you have accompanying symptoms like fever or unexplained weight loss?",
        "Do you have a history of anemia or thyroid imbalance, and how is your daily sleep quality?"
    ],
    "mild_fever": [
        "How many days has the fever lasted, and what is your current temperature reading?",
        "Are you experiencing any accompanying symptoms such as cough, sore throat, or body pain?"
    ],
    "back_pain": [
        "Did this back pain begin after heavy lifting or physical strain, and does it radiate down either of your legs?",
        "Do you feel any numbness, weakness in your lower limbs, or difficulty with posture?"
    ],
    "headache": [
        "How long have you had this headache, and is it accompanied by nausea, dizziness, or light sensitivity?",
        "Have you noticed any neck stiffness or visual changes along with the pain?"
    ],
    "acid_reflux": [
        "How frequently do you experience this acid reflux, and does the burning worsen after specific meals or when lying down?",
        "Are you experiencing any difficulty swallowing, persistent burping, or stomach pain?"
    ]
}

# Signature & Advertisement Stripping Patterns
STRIP_PATTERNS = [
    r"Dr\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*.*",
    r"Doctor\s+[A-Z][a-z]+.*",
    r"Regards,?\s*.*",
    r"Best regards,?\s*.*",
    r"Sincerely,?\s*.*",
    r"Thanks for asking,?\s*.*",
    r"Welcome to Chat Doctor forum\.?",
    r"Welcome to ChatDoctor\.?",
    r"ChatDoctor Team\.?",
    r"iCliniq Team\.?",
    r"HealthCareMagic Physician\.?",
    r"For more information consult.*",
    r"Visit our website.*",
    r"Call 911.*",
    r"Call 999.*",
    r"Contact us at.*",
    r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
    r"\b1-800-\d+\b",
    r"Disclaimer:.*",
    r"This advice does not constitute a doctor-patient relationship.*",
    r"Hope I have answered your query.*",
    r"Hope this helps.*",
    r"Wish you a speedy recovery.*",
    r"Take care\..*"
]

STRIP_USER_PREFIXES = [
    r"^(hello|hi|hey|greetings)(\s+doctor)?,?\s*",
    r"^dear\s+doctor,?\s*",
    r"^doctor,?\s*"
]

def clean_unicode(text):
    if not text:
        return ""
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u02bc", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2014", " - ").replace("\u2013", " - ").replace("\u2212", " - ")
    text = text.replace("\u00a0", " ").replace("\ufffd", "'").replace("\u00b0", " degrees ")
    text = text.replace("â€™", "'").replace("â€”", " - ").replace("â€œ", '"').replace("â€", '"')
    
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'[\u2018\u2019\u201a\u201b\u2032\u2035]', "'", text)
    text = re.sub(r'[\u201c\u201d\u201e\u201f\u2033\u2036]', '"', text)
    text = re.sub(r'[\u2010\u2011\u2012\u2013\u2014\u2015]', '-', text)
    
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def clean_user_input(text):
    c = clean_unicode(text)
    for p in STRIP_USER_PREFIXES:
        c = re.sub(p, "", c, flags=re.IGNORECASE).strip()
    if c:
        c = c[0].upper() + c[1:]
    return c

def clean_doctor_output(text):
    c = clean_unicode(text)
    # Strip numbering artifacts (1., 2), etc.)
    c = re.sub(r'\b\d+[\.\)]\s*', '', c)
    
    for p in STRIP_PATTERNS:
        c = re.sub(p, "", c, flags=re.IGNORECASE).strip()
        
    c = re.sub(r'\s+', ' ', c).strip()
    return c

def is_excluded(text):
    t_lower = text.lower()
    for exc in EXCLUSIONS:
        if re.search(exc, t_lower):
            return True
    return False

def get_category(text):
    t_lower = text.lower()
    for cat, patterns in CATEGORIES.items():
        if any(re.search(pat, t_lower) for pat in patterns):
            return cat
    return None

def restructure_doctor_turn(output_text, category):
    cleaned = clean_doctor_output(output_text)
    
    # Pick targeted diagnostic follow-up question
    q_pair = DIAGNOSTIC_QUESTIONS.get(category, DIAGNOSTIC_QUESTIONS["fatigue"])
    followup_q = f"Before recommending a self-care plan: {q_pair[0]}"
    
    # Truncate advice body under 130 words total
    words = cleaned.split()
    max_advice_words = 85
    if len(words) > max_advice_words:
        advice_body = " ".join(words[:max_advice_words]).rstrip(".,;:") + "."
    else:
        advice_body = cleaned
        
    if not advice_body.endswith("."):
        advice_body += "."
        
    full_response = f"{followup_q}\n\n{advice_body}"
    
    # Enforce strict < 130 words cap
    res_words = full_response.split()
    if len(res_words) > 125:
        full_response = " ".join(res_words[:125]).rstrip(".,;:") + "."
        
    return full_response

def process_dataset():
    cat_pools = defaultdict(list)
    seen_inputs = set()
    
    files_to_load = [
        ("iCliniq.json", "answer_chatdoctor", "answer_icliniq"),
        ("HealthCareMagic-100k.json", "output", "output")
    ]
    
    for fname, primary_key, sec_key in files_to_load:
        fpath = os.path.join(INPUT_DIR, fname)
        if not os.path.exists(fpath):
            print(f"Warning: File {fname} not found.")
            continue
            
        print(f"Loading {fname}...")
        with open(fpath, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
            
        print(f"Processing {len(data)} items from {fname}...")
        
        for item in data:
            inp = item.get("input", "")
            out = item.get(primary_key, "") or item.get(sec_key, "")
            
            if not inp or not out:
                continue
                
            full_text = inp + " " + out
            if is_excluded(full_text):
                continue
                
            cat = get_category(full_text)
            if not cat:
                continue
                
            u_clean = clean_user_input(inp)
            u_key = u_clean.lower().strip()
            
            if not u_clean or u_key in seen_inputs or len(u_clean.split()) < 8:
                continue
                
            cat_pools[cat].append((u_clean, out, cat))
            seen_inputs.add(u_key)

    print("\nPrimary Care Category Pool Counts:")
    for cat, pool in cat_pools.items():
        print(f"  - {cat}: {len(pool)} available")
        
    # Sample 750 pairs across 5 categories (~150 each)
    selected_items = []
    per_cat_target = TARGET_SIZE // len(CATEGORIES)  # 150 each
    
    for cat, pool in cat_pools.items():
        random.shuffle(pool)
        take = min(len(pool), per_cat_target)
        selected_items.extend(pool[:take])
        
    if len(selected_items) < TARGET_SIZE:
        remaining_pool = []
        selected_set = set(id(item) for item in selected_items)
        for cat, pool in cat_pools.items():
            for item in pool:
                if id(item) not in selected_set:
                    remaining_pool.append(item)
                    
        random.shuffle(remaining_pool)
        needed = TARGET_SIZE - len(selected_items)
        selected_items.extend(remaining_pool[:needed])
        
    selected_items = selected_items[:TARGET_SIZE]
    random.shuffle(selected_items)
    
    print(f"\nTotal sampled ChatDoctor primary care pairs: {len(selected_items)}")
    
    chatml_pairs = []
    category_counts = defaultdict(int)
    
    for user_inp, doc_out, cat in selected_items:
        category_counts[cat] += 1
        a_restructured = restructure_doctor_turn(doc_out, cat)
        
        turn = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_inp},
                {"role": "assistant", "content": a_restructured}
            ]
        }
        chatml_pairs.append(turn)

    # Save to fine-tuning directory
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(chatml_pairs, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully exported {len(chatml_pairs)} ChatML pairs to:")
    print(f"  {OUTPUT_FILE}")
    
    print("\nFinal Category Distribution in Exported Dataset:")
    for cat, cnt in category_counts.items():
        print(f"  - {cat}: {cnt}")

    # Validate first item
    print("\nValidation check on first pair:")
    print(json.dumps(chatml_pairs[0], indent=2))

if __name__ == "__main__":
    process_dataset()
