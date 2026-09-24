import csv
import random
from pathlib import Path
import sys

backend_dir = Path(r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend")
output_file = backend_dir / "datasets" / "fine-tuning" / "laya_intent_classification_synthetic_dataset.csv"

# ---------------------------------------------------------
# Dynamic Components for Human-like Synthetic Generation
# Laya AI receives English inputs ONLY (post translation).
# ---------------------------------------------------------

OPENERS = [
    "", "", "", "", "", # 50% chance of no opener
    "Please tell me ", "I want to know ", "Doctor ", "Help me ", 
    "Can you say ", "My ", "Listen ", "Urgently need to know "
]

# --- CLASS 1: EMERGENCY_CRITICAL ---
C1_SYMPTOMS = [
    "severe chest pain", "heart attack", "crushing pain in chest", 
    "left arm going numb", "snake bite", "snake bit my leg", 
    "profuse bleeding", "heavy blood loss", "major accident", 
    "unconscious", "fainted and not waking up", "pesticide poisoning", 
    "drank poison", "choking", "cannot breathe", "severe electric shock", 
    "head injury", "bleeding from ear", "sudden extreme stomach pain in pregnancy"
]
C1_ACTIONS = [
    "need ambulance", "call 108", "send help", "urgent help needed", 
    "what to do right now", "save him", "emergency", "send ambulance fast"
]

def gen_c1():
    s = random.choice(C1_SYMPTOMS)
    a = random.choice(C1_ACTIONS)
    style = random.choice(["short", "urgent", "descriptive", "broken"])
    if style == "short":
        return f"{s} {a}"
    elif style == "urgent":
        return f"{a}! {s}!"
    elif style == "descriptive":
        return f"My grandfather has {s}. We {a}."
    else: 
        return f"{s} happening. {a} please."

# --- CLASS 2: FACILITY_LOCATOR ---
C2_FACILITIES = [
    "Jan Aushadhi Kendra", "PMBJP store", "government hospital", 
    "PHC", "Primary Health Center", "CHC", "Community Health Center", 
    "blood bank", "free lab", "diagnostic center", "trauma center", "ICU bed"
]
C2_LOCATIONS = [
    "near me", "in Wardha", "near civil lines", "in Bhopal", 
    "near PIN 440003", "in Gwalior", "in Shivpuri", "in my village"
]
C2_INTENTS = [
    "Where is the nearest", "Find", "Location of", "Contact number for", 
    "Is there any", "Show me", "I am looking for"
]

def gen_c2():
    f = random.choice(C2_FACILITIES)
    l = random.choice(C2_LOCATIONS)
    i = random.choice(C2_INTENTS)
    style = random.choice(["question", "command", "short", "broken"])
    if style == "question":
        return f"{i} {f} {l}?"
    elif style == "command":
        return f"Give me the address of a {f} {l}."
    elif style == "short":
        return f"nearest {f} {l}"
    else:
        return f"{f} {l} where is it"

# --- CLASS 3: GOVT_SCHEME_ELIGIBILITY ---
C3_SCHEMES = [
    "Ayushman Bharat", "PM-JAY", "ABHA health ID", 
    "Janani Suraksha Yojana", "State health scheme", "BPL medical scheme"
]
C3_TOPICS = [
    "eligibility", "documents required", "free treatment", 
    "5 lakh coverage", "apply online", "benefits", "hospital list"
]

def gen_c3():
    s = random.choice(C3_SCHEMES)
    t = random.choice(C3_TOPICS)
    style = random.choice(["question", "scenario", "short", "broken"])
    if style == "question":
        return f"Am I eligible for {s} if I have a BPL card?"
    elif style == "scenario":
        return f"I need to know the {t} for {s}."
    elif style == "short":
        return f"{s} {t}"
    else:
        return f"how to get {t} in {s}"

# --- CLASS 4: MEDICINE_GENERIC_SEARCH ---
C4_DRUGS = [
    "Paracetamol 650", "Dolo 650", "Telmisartan 40", "Clavam 625", 
    "Metformin 500", "Atorvastatin 10mg", "Azithromycin 500", "Pantoprazole 40", 
    "Cetirizine"
]
C4_TOPICS = [
    "generic substitute", "cheap alternative", "Jan Aushadhi price", 
    "side effects", "dosage", "when to take", "after food or empty stomach", 
    "safe during pregnancy"
]

def gen_c4():
    d = random.choice(C4_DRUGS)
    t = random.choice(C4_TOPICS)
    style = random.choice(["prescription", "question", "short", "broken"])
    if style == "prescription":
        return f"Doctor prescribed {d}. What is its {t}?"
    elif style == "question":
        return f"What is the {t} for {d}?"
    elif style == "short":
        return f"{d} {t}"
    else:
        return f"{t} of {d} tell me"

# --- CLASS 5: SYMPTOM_TRIAGE_REMEDY ---
C5_SYMPTOMS = [
    "mild fever", "102F fever", "dry cough", "sore throat", 
    "joint pain", "morning stiffness", "stomach ache", "loose motion", 
    "headache", "eye strain", "chest burning after food", "red rash"
]
C5_CONTEXTS = [
    "in my 5-year-old child", "since yesterday", "for the last two days", 
    "after eating outside food", "in the morning", "with chills"
]
C5_REQUESTS = [
    "home remedy", "what should I do", "which medicine to take", 
    "do I need a doctor", "natural cure", "diet advice"
]

def gen_c5():
    s = random.choice(C5_SYMPTOMS)
    c = random.choice(C5_CONTEXTS)
    r = random.choice(C5_REQUESTS)
    style = random.choice(["descriptive", "question", "short", "broken"])
    if style == "descriptive":
        return f"I have {s} {c}. Please suggest a {r}."
    elif style == "question":
        return f"What is the best {r} for {s}?"
    elif style == "short":
        return f"{s} {r}"
    else:
        return f"{s} {c} {r} please"

# --- CLASS 6: OUT_OF_SCOPE_GENERAL ---
C6_GREETINGS = ["Hello", "Hi", "Namaste", "Good morning", "Thank you"]
C6_QUESTIONS = [
    "who are you", "what can you do", "how to change language", 
    "are you a doctor", "how does this app work"
]
C6_OFF_TOPIC = [
    "what is the weather today", "who won the cricket match", 
    "tell me a joke", "what is the capital of India", "how to cook biryani"
]

def gen_c6():
    style = random.choice(["greeting", "app_question", "off_topic", "mixed"])
    if style == "greeting":
        return random.choice(C6_GREETINGS)
    elif style == "app_question":
        return f"{random.choice(C6_GREETINGS)}, {random.choice(C6_QUESTIONS)}?"
    elif style == "off_topic":
        return random.choice(C6_OFF_TOPIC)
    else:
        return f"{random.choice(C6_QUESTIONS)}?"

def apply_opener(text):
    op = random.choice(OPENERS)
    if op and not text.lower().startswith(("what", "where", "how", "is", "can", "am", "do")):
        if random.random() > 0.3 and text[0].isupper():
            text = text[0].lower() + text[1:]
        return op + text
    return text

def generate_dataset():
    dataset = []
    classes = {
        "EMERGENCY_CRITICAL": gen_c1,
        "FACILITY_LOCATOR": gen_c2,
        "GOVT_SCHEME_ELIGIBILITY": gen_c3,
        "MEDICINE_GENERIC_SEARCH": gen_c4,
        "SYMPTOM_TRIAGE_REMEDY": gen_c5,
        "OUT_OF_SCOPE_GENERAL": gen_c6
    }
    
    for cls, gen_func in classes.items():
        seen = set()
        attempts = 0
        while len(seen) < 200 and attempts < 10000:
            text = gen_func()
            text = apply_opener(text)
            
            # Simulate speech-to-text / translation errors (lowercase, missing punctuation)
            if random.random() > 0.6:
                text = text.replace("?", "").replace(".", "")
            if random.random() > 0.8:
                text = text.lower()
                
            text = text.strip()
            if text and text.lower() not in [x.lower() for x in seen]:
                seen.add(text)
            attempts += 1
            
        for text in list(seen)[:200]:
            dataset.append({"text": text, "label": cls})
            
    return dataset

def main():
    print("Generating pure English natural dataset...", flush=True)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    dataset = generate_dataset()
    random.shuffle(dataset)
    
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(dataset)
        
    counts = {}
    for row in dataset:
        counts[row["label"]] = counts.get(row["label"], 0) + 1
        
    print("\nDataset Generation Complete!", flush=True)
    print(f"Total Rows: {len(dataset)}", flush=True)
    for k, v in counts.items():
        print(f"  {k}: {v}", flush=True)
        
if __name__ == "__main__":
    main()
