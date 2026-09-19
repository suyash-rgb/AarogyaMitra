"""
ArogyaMitra Data Preprocessing Script: FirstAidQA Dataset
---------------------------------------------------------
Dataset: FirstAidQA (firstaidqa_v1.json)
Target Output: 1,000 ChatML pairs stored in datasets/fine-tuning/firstaidqa-clean.json

Sampling Criteria:
- Filter exclusively for high-acuity physical emergencies: cardiac arrest, airway obstruction/choking,
  arterial bleeding, electrical shock, chemical/thermal burns, fractures, venomous bites.
- Filter ONLY for detailed, multi-sentence answers (word count >= 30) to ensure rich procedural quality.
- Exclude minor dermatological or non-urgent queries.

Cleaning & Preprocessing:
- Strip all conversational fillers ("Hello", "Thank you for your question", "I am sorry to hear that").
- Sanitize and normalize all broken unicode characters (\u2019, \u2014, \u2013, \u201c, \u201d, \ufffd).
- Reformat answers strictly into 4 to 5 numbered steps starting with active imperative verbs.
- Append standard emergency dispatch trigger: "Call 108/112 immediately if patient is unresponsive."
"""

import os
import json
import re
import random
import unicodedata
from collections import defaultdict

# Fixed random seed for reproducibility
random.seed(42)

INPUT_FILE = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\firstaidqa_v1.json"
OUTPUT_FILE = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend\datasets\fine-tuning\firstaidqa-clean.json"
TARGET_SIZE = 1000
MIN_ANSWER_WORDS = 30  # Strictly enforce detailed, long procedural answers

SYSTEM_PROMPT = "You are AarogyaMitra Health Advisor, an empathetic AI clinical assistant for Indian emergency healthcare contexts."

# High-acuity categories and keyword patterns
CATEGORIES = {
    "cardiac_arrest": [
        r"\bcardiac\b", r"\bcpr\b", r"\bheart attack\b", r"\bdefibrillat\w*", r"\baed\b",
        r"\bchest compression\w*", r"\bcardiopulmonary\b", r"\bcardiac arrest\b", r"\bunresponsive\b",
        r"\bresuscitat\w*", r"\bheart failure\b", r"\bcardiac emergency\b"
    ],
    "choking_airway": [
        r"\bchok\w*", r"\bairway\b", r"\bheimlich\b", r"\bsuffocat\w*", r"\bstrangulat\w*",
        r"\blocked airway\b", r"\basphyxiat\w*", r"\bforeign object\b", r"\bgasping\b", r"\bstopped breathing\b"
    ],
    "arterial_bleeding": [
        r"\barterial\b", r"\bsevere bleed\w*", r"\bheavy bleed\w*", r"\btourniquet\b",
        r"\bhemorrhag\w*", r"\bspurting blood\b", r"\bprofuse bleed\w*", r"\buncontrolled bleed\w*",
        r"\bbleeding wound\b", r"\bblood loss\b", r"\bdeep laceration\w*", r"\bbleed\w*"
    ],
    "electrical_shock": [
        r"\belectric\w*", r"\belectrocut\w*", r"\bhigh voltage\b", r"\bpower line\b",
        r"\belectrical burn\w*", r"\belectric current\b", r"\blive wire\b", r"\bshock\b"
    ],
    "burns": [
        r"\bburn\w*", r"\bscald\w*", r"\bfire\b", r"\bthermal\b", r"\bchemical burn\w*",
        r"\bacid burn\w*", r"\bsecond degree burn\w*", r"\bthird degree burn\w*", r"\bsevere burn\w*",
        r"\bblister\w*"
    ],
    "fractures": [
        r"\bfracture\w*", r"\bbroken bone\w*", r"\bdislocat\w*", r"\bsplint\w*",
        r"\bcompound fracture\w*", r"\bopen fracture\w*", r"\bbroken arm\b", r"\bbroken leg\b",
        r"\bspinal injury\b", r"\bback injury\b", r"\bneck injury\b"
    ],
    "venomous_bites": [
        r"\bsnake\w*", r"\bvenom\w*", r"\bscorpion\w*", r"\bspider\w*",
        r"\brabid\w*", r"\bdog bite\w*", r"\bwasp\w*", r"\bbee\w*", r"\banimal bite\w*",
        r"\bviper\b", r"\bcobra\b", r"\bpoisonous bite\w*", r"\bsting\w*"
    ]
}

EXCLUSION_PATTERNS = [
    r"\bacne\b", r"\bminor rash\b", r"\bitch\w*", r"\bminor scrape\w*", r"\bminor cut\w*",
    r"\bsunburn\b", r"\bdry skin\b", r"\bdermatitis\b", r"\bhives\b", r"\bwrinkle\w*",
    r"\btheory test\b", r"\bdriving test\b", r"\bquiz\b"
]

IMPERATIVE_VERBS = [
    "Apply", "Elevate", "Do not", "Place", "Position", "Check", "Call", "Clear",
    "Cool", "Cover", "Ensure", "Monitor", "Maintain", "Keep", "Tilt", "Loosen",
    "Support", "Immobilize", "Wash", "Remove", "Avoid", "Press", "Perform",
    "Administer", "Seek", "Secure", "Assess", "Stop", "Turn", "Open", "Lie", "Lay",
    "Shield", "Flush", "Wrap", "Hold", "Protect", "Disconnect", "Isolate",
    "Reassure", "Observe", "Examine", "Comfort", "Rest", "Bandage", "Control",
    "Stay", "Help", "Pinch", "Immerse", "Straighten", "Align", "Rinse",
    "Dress", "Splint", "Stabilize", "Lower", "Raise", "Grip", "Drag", "Use",
    "Lift", "Look", "Listen", "Feel", "Begin", "Start", "Push", "Compress",
    "Give", "Provide", "Contact", "Clean", "Inspect", "Stand", "Wait", "Do", "Don't",
    "Leave", "Crouch", "Seat", "Assist", "Remain"
]

IMPERATIVE_SET = set(v.lower() for v in IMPERATIVE_VERBS)

FILLER_PREFIXES = [
    r"^(hello|hi|hey|greetings)[!.,\s]*",
    r"^thank you for your question[!.,\s]*",
    r"^i am sorry to hear that[!.,\s]*",
    r"^as a first aider,?[\s]*",
    r"^in an emergency,?[\s]*",
    r"^it is important to remember that,?[\s]*",
    r"^please note that,?[\s]*",
    r"^firstly,?[\s]*",
    r"^secondly,?[\s]*",
    r"^thirdly,?[\s]*",
    r"^finally,?[\s]*",
    r"^in case of emergency,?[\s]*",
    r"^you should\s+",
    r"^you must\s+",
    r"^you need to\s+",
    r"^it is recommended to\s+",
    r"^it's best to\s+",
    r"^it is best to\s+",
    r"^make sure to\s+",
    r"^be sure to\s+",
    r"^always\s+",
    r"^if possible,?\s*",
    r"^the first aider should\s+",
    r"^the responder should\s+",
    r"^the patient should\s+",
    r"^the victim should\s+",
    r"^no,?\s+",
    r"^yes,?\s+",
    r"^otherwise,?\s*"
]

CATEGORY_DEFAULTS = {
    "cardiac_arrest": [
        "Check for responsiveness and normal breathing immediately.",
        "Position the victim flat on their back on a firm surface.",
        "Perform uninterrupted chest compressions at a rate of 100-120 per minute.",
        "Monitor for signs of circulation and prepare to use an AED if available."
    ],
    "choking_airway": [
        "Assess whether the person can cough or speak clearly.",
        "Position yourself behind the victim and lean them slightly forward.",
        "Deliver 5 sharp back blows between the shoulder blades.",
        "Perform 5 quick abdominal thrusts if the airway remains obstructed."
    ],
    "arterial_bleeding": [
        "Apply direct, firm pressure over the bleeding wound immediately.",
        "Elevate the injured limb above heart level if no fracture is suspected.",
        "Apply a sterile pressure bandage tightly over the wound site.",
        "Monitor for signs of severe shock and maintain body warmth."
    ],
    "electrical_shock": [
        "Disconnect the power source safely before touching the casualty.",
        "Assess the victim's breathing and responsiveness from a safe distance.",
        "Cool electrical burn sites with clean water once safe.",
        "Keep the patient lying down and still until medical care arrives."
    ],
    "burns": [
        "Cool the burn with running cool water for at least 10 to 20 minutes.",
        "Remove restrictive clothing or jewelry near the burn before swelling occurs.",
        "Cover the burn loosely with a sterile, non-stick dressing.",
        "Do not apply ice, butter, or ointments directly to the burn."
    ],
    "fractures": [
        "Immobilize the injured limb in the position it was found.",
        "Apply a cold pack wrapped in a cloth to reduce swelling.",
        "Support the fracture using a splint or sling if trained.",
        "Do not attempt to realign broken bones yourself."
    ],
    "venomous_bites": [
        "Keep the bitten limb immobilized and below heart level.",
        "Wash the bite area gently with clean water and mild soap.",
        "Apply a clean, dry dressing over the bite site.",
        "Do not attempt to cut the wound or suck out venom."
    ]
}

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

def clean_clause(clause):
    c = clean_unicode(clause)
    for p in FILLER_PREFIXES:
        c = re.sub(p, "", c, flags=re.IGNORECASE).strip()
    return c

def convert_to_imperative_step(sentence):
    c = clean_clause(sentence)
    if not c:
        return ""
    
    c = re.sub(r"^(when|if)\s+[^,]{5,50},\s*", "", c, flags=re.IGNORECASE).strip()
    c = clean_clause(c)
    
    words = c.split()
    if not words:
        return ""
    
    first = words[0].strip(".,;:\"'")
    first_lower = first.lower()
    
    if first_lower in IMPERATIVE_SET or first_lower in ["do", "don't", "dont"]:
        words[0] = first.capitalize()
        res = " ".join(words)
        res = res.rstrip(".!?,;") + "."
        return res

    c_lower = c.lower()
    
    # Handle negative imperatives cleanly
    if any(w in c_lower for w in ["should not", "must not", "do not", "don't", "never", "avoid", "not be used"]):
        if "human crutch" in c_lower:
            return "Do not use a human crutch if an arm, hand, or shoulder is injured."
        elif "drag" in c_lower or "clothing" in c_lower:
            return "Do not drag a casualty by their clothing to prevent worsening injuries."
        elif "realign" in c_lower or "bone" in c_lower:
            return "Do not attempt to realign broken bones or dislocated joints."
        elif "cut" in c_lower or "suck" in c_lower or "venom" in c_lower:
            return "Do not cut the wound or attempt to suck out venom."
        elif "ice" in c_lower or "ointment" in c_lower or "butter" in c_lower:
            return "Do not apply ice, butter, or ointments directly to burns."
        elif "pop" in c_lower or "blister" in c_lower:
            return "Do not break or pop burn blisters."
        elif "touch" in c_lower or "wire" in c_lower or "cable" in c_lower:
            return "Do not touch live electrical cables or electrical shock victims directly."
        else:
            action = re.sub(r"^[^.]*?\b(should not|must not|do not|don't|never|avoid|not be used)\b\s*", "", c, flags=re.IGNORECASE).strip()
            if action.lower().startswith("be used"):
                action = re.sub(r"^be used\s*", "", action, flags=re.IGNORECASE).strip()
                return f"Do not use {action[0].lower() + action[1:]}."
            elif action:
                action_clean = action.rstrip(".!?,;")
                return f"Avoid {action_clean[0].lower() + action_clean[1:]}."
            return "Avoid any actions that could worsen the patient's condition."

    action_verbs = [
        ("apply", "Apply"), ("elevate", "Elevate"), ("place", "Place"), ("position", "Position"),
        ("check", "Check"), ("call", "Contact"), ("clear", "Clear"), ("cool", "Cool"),
        ("cover", "Cover"), ("monitor", "Monitor"), ("keep", "Keep"), ("tilt", "Tilt"),
        ("loosen", "Loosen"), ("support", "Support"), ("immobilize", "Immobilize"),
        ("wash", "Wash"), ("remove", "Remove"), ("avoid", "Avoid"), ("press", "Press"),
        ("perform", "Perform"), ("administer", "Administer"), ("flush", "Flush"),
        ("clean", "Clean"), ("splint", "Splint"), ("stay", "Remain"), ("remain", "Remain"),
        ("lay", "Position"), ("lie", "Position"), ("use", "Use")
    ]
    
    for v_pattern, v_cap in action_verbs:
        m = re.search(r'\b' + v_pattern + r'\b\s+(.*)', c, flags=re.IGNORECASE)
        if m:
            rest = m.group(1).strip()
            if len(rest) > 5:
                res = f"{v_cap} {rest}".rstrip(".!?,;") + "."
                return res

    # Intent-based sentence rewrites
    if "cpr" in c_lower or "compression" in c_lower or "resuscitat" in c_lower:
        return "Perform uninterrupted CPR chest compressions immediately."
    elif "water" in c_lower or "flush" in c_lower or "rinse" in c_lower:
        return "Flush the affected area continuously with cool clean water."
    elif "wash" in c_lower or "soap" in c_lower:
        return "Wash the area gently with soap and clean water."
    elif "dressing" in c_lower or "bandage" in c_lower or "gauze" in c_lower or "pressure" in c_lower or "bleed" in c_lower:
        return "Apply firm direct pressure using a clean dressing or bandage."
    elif "monitor" in c_lower or "observe" in c_lower or "breath" in c_lower:
        return "Monitor breathing, pulse, and level of consciousness continuously."
    elif "calm" in c_lower or "panic" in c_lower or "still" in c_lower or "quiet" in c_lower:
        return "Remain calm and keep the casualty quiet and still."
    elif "call" in c_lower or "help" in c_lower or "emergency" in c_lower or "medical" in c_lower:
        return "Contact local emergency medical services for immediate assistance."
    elif "move" in c_lower or "position" in c_lower or "drag" in c_lower:
        return "Position the casualty safely without bending or twisting injured limbs."
    elif "check" in c_lower or "assess" in c_lower or "pulse" in c_lower:
        return "Assess vital signs including responsiveness, breathing, and pulse."
    elif "cover" in c_lower or "cloth" in c_lower or "blanket" in c_lower:
        return "Cover the wound or burn loosely with a clean non-stick sterile sheet."
    elif "elevate" in c_lower or "raise" in c_lower:
        return "Elevate the injured area above heart level if no fracture is suspected."
    elif "splint" in c_lower or "immobiliz" in c_lower or "fracture" in c_lower:
        return "Immobilize the fractured limb in the position found."
    else:
        return "Ensure the patient remains supported and monitored until help arrives."

def format_answer_into_imperative_steps(answer, category):
    text = clean_clause(answer)
    sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 8]
    
    steps = []
    for s in sentences:
        imp = convert_to_imperative_step(s)
        if imp and imp not in steps:
            steps.append(imp)
            
    defaults = CATEGORY_DEFAULTS.get(category, CATEGORY_DEFAULTS["cardiac_arrest"])
    
    idx = 0
    while len(steps) < 4 and idx < len(defaults):
        d_imp = convert_to_imperative_step(defaults[idx])
        if d_imp not in steps:
            steps.append(d_imp)
        idx += 1
        
    if len(steps) > 5:
        steps = steps[:5]
        
    numbered = [f"{i}. {st}" for i, st in enumerate(steps, 1)]
    
    # Append mandatory emergency dispatch trigger line
    numbered.append("")
    numbered.append("Call 108/112 immediately if patient is unresponsive.")
    return "\n".join(numbered)

def process_dataset():
    print(f"Reading input dataset from: {INPUT_FILE}")
    with open(INPUT_FILE, "r", encoding="utf-8", errors="replace") as f:
        raw_data = json.load(f)
        
    print(f"Total raw items loaded: {len(raw_data)}")
    
    cat_pools = defaultdict(list)
    seen_questions = set()
    
    for item in raw_data:
        q = item.get("question", "")
        a = item.get("answer", "")
        
        q_clean = clean_unicode(q)
        a_clean = clean_unicode(a)
        
        # Enforce long, detailed answers (>= 30 words) with multiple sentences
        if len(a_clean.split()) < MIN_ANSWER_WORDS or len(re.split(r'(?<=[.!?])\s+', a_clean)) < 2:
            continue
            
        text = (q_clean + " " + a_clean).lower()
        
        # Exclude minor or non-urgent queries
        if any(re.search(exc, text) for exc in EXCLUSION_PATTERNS):
            continue
            
        q_key = q_clean.lower().strip()
        if not q_key or q_key in seen_questions:
            continue
            
        # Match category
        for cat, patterns in CATEGORIES.items():
            if any(re.search(pat, text) for pat in patterns):
                cat_pools[cat].append((item, cat))
                seen_questions.add(q_key)
                break

    print("\nDetailed High-Acuity Pool Counts (Answer Length >= 30 words):")
    for cat, pool in cat_pools.items():
        print(f"  - {cat}: {len(pool)} available")
        
    # Sample 1,000 pairs across categories
    selected_items = []
    per_cat_target = TARGET_SIZE // len(CATEGORIES)  # ~142-143 each
    
    for cat, pool in cat_pools.items():
        random.shuffle(pool)
        take = min(len(pool), per_cat_target)
        selected_items.extend(pool[:take])
        
    # Fill remaining to reach exactly 1,000
    if len(selected_items) < TARGET_SIZE:
        remaining_pool = []
        selected_set = set(id(item[0]) for item in selected_items)
        for cat, pool in cat_pools.items():
            for item in pool:
                if id(item[0]) not in selected_set:
                    remaining_pool.append(item)
                    
        random.shuffle(remaining_pool)
        needed = TARGET_SIZE - len(selected_items)
        selected_items.extend(remaining_pool[:needed])
        
    selected_items = selected_items[:TARGET_SIZE]
    random.shuffle(selected_items)
    
    print(f"\nTotal sampled detailed emergency pairs: {len(selected_items)}")
    
    # Process into ChatML format
    chatml_pairs = []
    category_counts = defaultdict(int)
    
    for item_dict, cat in selected_items:
        category_counts[cat] += 1
        q_raw = item_dict.get("question", "")
        a_raw = item_dict.get("answer", "")
        
        q_clean = clean_unicode(q_raw)
        a_clean = clean_unicode(a_raw)
        a_formatted = format_answer_into_imperative_steps(a_clean, cat)
        
        turn = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q_clean},
                {"role": "assistant", "content": a_formatted}
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

if __name__ == "__main__":
    process_dataset()
