import os
import sys
import csv
import re
import random
from pathlib import Path

backend_dir = Path(r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend")
dataset_file = backend_dir / "datasets" / "fine-tuning" / "laya_intent_classification_synthetic_dataset.csv"

sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None

# Realistic natural human phrasing templates per class across 4 distinct styles:
# Style A: Ultra-short search keyword
# Style B: Conversational Hinglish
# Style C: Natural Voice-STT phrasing
# Style D: Detailed rural patient description

VARIATIONS_CLASS_1 = [ # EMERGENCY_CRITICAL
    # Ultra short
    "chest pain 108 ambulance urgent",
    "snake bite leg bleeding emergency",
    "accident highway patient unconscious",
    "pesticide poison vomiting urgent doctor",
    "electric shock patient pulse missing",
    "child choking breath stop urgent",
    "head trauma bleeding ears accident",
    "heart attack left arm pain emergency",
    # Hinglish
    "bhaiya jaldi 108 ambulance bhejo mere dada ko bahot tez chest pain ho raha hai!",
    "khet me saap ne kaat liya hai leg me bahot sujan aur khoon beh raha hai kya kare!",
    "highway par car accident ho gaya hai ek banda unconscious hai jaldi help karo!",
    "chote bache ne kanch ki goli nigal li hai usse saans nahi aa rahi!",
    "kisaan ne accidentally keetnashak pee liya hai ulti aur jhaag nikal raha hai!",
    "bijli ka jhatka laga hai aadmi behosh hai dhadkan nahi chal rahi!",
    "pregnant aurat ko achanak bahot tez pet dard aur heavy bleeding ho rahi hai!",
    "chhat se girne se sar me gambhir chot aayi hai kaan se khoon aa raha hai!",
    # Voice-STT
    "hello emergency... mera bhai accident me behosh ho gaya hai ambulance chahiye gwalior highway par",
    "sir turant bataiye saap kaatne par pehla ilaj kya kare khoon ruk nahi raha",
    "urgently medical help chahiye mere papa ko severe heart attack aaya hai sweating ho rahi hai",
    "bacha saans nahi le pa raha hai choking ho raha hai emergency guidance do",
    # Detailed
    "A 55-year-old farmer collapsed in the field with sudden severe crushing chest pain, sweating, and difficulty breathing. Immediate emergency response needed.",
    "Road trauma accident victim lying unresponsive near Shivpuri bypass with severe head lacerations and arterial bleeding."
]

VARIATIONS_CLASS_2 = [ # FACILITY_LOCATOR
    # Ultra short
    "nearest phc shivpuri location",
    "jan aushadhi kendra wardha contact",
    "blood bank o negative bhopal",
    "24/7 govt hospital icu gwalior",
    "free diagnostic lab near me",
    "pmjbp store pin 440003",
    "chc hospital vidisha address",
    "trauma center nh44 location",
    # Hinglish
    "bhaiya sabse paas wala primary health center (PHC) kaha hai shivpuri me?",
    "wardha me jan aushadhi kendra ka address aur phone number milega kya?",
    "bhopal me o negative blood availability kis blood bank me hai?",
    "gwalior civil lines ke paas koi free govt hospital ya phc hai kya?",
    "pin code 462001 ke paas koi janaushadhi kendra khula hai abhi?",
    "vidisha me nearest community health center (CHC) ka location batao",
    "ayushman card accept karne wala nearest hospital konsa hai jabalpur me?",
    "raat ko 24 ghante khula rehne wala emergency hospital paas me kaha hai?",
    # Voice-STT
    "hello... mujhe mere ghar ke paas jan aushadhi medical store dhoondna hai contact number dedo",
    "bhopal me kis sarkari hospital me icu bed khali hai abhi turant jana hai",
    "near me blood bank me a positive blood mil jayega kya jaldi batao",
    "shivpuri district hospital me digital x-ray facility hai kya",
    # Detailed
    "Where is the nearest Primary Health Center or District Civil Hospital in Shivpuri with functioning emergency pediatric care?",
    "Looking for a list of government empanelled hospitals near Gwalior Civil Lines that accept Ayushman Bharat e-cards."
]

VARIATIONS_CLASS_3 = [ # GOVT_SCHEME_ELIGIBILITY
    # Ultra short
    "ayushman bharat eligibility bpl card",
    "pmjay 5 lakh coverage rules",
    "abha health id documents aadhaar",
    "janani suraksha yojana free delivery mp",
    "pmssy scheme hospital list",
    "ayushman card registration process",
    "bpl vs apl health scheme limit",
    "mukhyamantri amrutam yojna benefits",
    # Hinglish
    "bhaiya bpl ration card par ayushman bharat me 5 lakh ka ilaj free milega kya?",
    "abha digital health id card banane ke liye konsa document lagta hai?",
    "janani suraksha yojana me sarkari hospital me delivery ke baad kitna paisa milta hai mp me?",
    "pm-jay health card me purani bimari jaise heart surgery cover hoti hai kya?",
    "ayushman card online mobile se kaise banaye mera aur meri family ka?",
    "kya apl card holder ko bhi sarkari swasthya bima yojana ka fayda milta hai?",
    "ayushman card se private hospital me bina paise diye ilaj ho sakta hai kya?",
    "mukhyamantri amrutam yojna me registration karne ki last date kya hai?",
    # Voice-STT
    "bhaiya thoda samjha do na ayushman bharat me eligibility check kaise karte hain",
    "abha card banane ke liye aadhaar card ke alawa aur kya kagaz chahiye",
    "janani suraksha yojana ka cash benefit account me kab tak aata hai",
    "pm-jay scheme me 5 lakh rupaye per family milta hai ya per person",
    # Detailed
    "What are the official eligibility guidelines, family income thresholds, and required documentation to register for the Ayushman Bharat PM-JAY scheme in Madhya Pradesh?",
    "How can a rural BPL family claim cashless hospitalization coverage for heart surgery under the state health protection mission?"
]

VARIATIONS_CLASS_4 = [ # MEDICINE_GENERIC_SEARCH
    # Ultra short
    "dolo 650 generic substitute price",
    "telmisartan 40 jan aushadhi salt",
    "clavam 625 cheap alternative name",
    "metformin 500 dose after food",
    "atorvastatin 10mg side effects",
    "prescription tab azithro 500 od meaning",
    "pantoprazole 40 empty stomach rule",
    "cetirizine pregnancy safe or not",
    # Hinglish
    "dolo 650 ki jagah jan aushadhi me konsi sasti generic dawa milti hai aur kitne ki hai?",
    "doctor ne clavam 625 likhi hai iska sasta sarkari generic salt name batao",
    "metformin 500mg ki tablet khana khane ke baad leni chahiye ya pehle?",
    "atorvastatin 10mg khane se koi side effect hota hai kya jaise muscle pain?",
    "doctor ke parche par likha hai 'Tab Azithro 500 OD x 3 days', iska kya matlab hai?",
    "pantoprazole 40mg subah khali pet lena zaroori hai kya?",
    "kya cetirizine allergy ki goli pregnancy me lena safe hai?",
    "paracetamol 650 ka ek din me maximum kitna dose le sakte hain?",
    # Voice-STT
    "bhaiya doctor ne pantocid likha hai iska jan aushadhi me sasta option bata do",
    "sugar ki goli glycomet 500 raat ko khane ke baad le sakte hain kya",
    "doctor ke prescription par OD aur BD ka matlab kya hota hai",
    "generic paracetamol 650 aur dolo 650 ke price me kitna farak hai",
    # Detailed
    "What is the exact pharmacological generic active salt name for Clavam 625, and what is its price comparison at Pradhan Mantri Jan Aushadhi Kendra?",
    "My doctor prescribed Azithromycin 500mg once daily for 3 days; what are the administration guidelines and common side effects?"
]

VARIATIONS_CLASS_5 = [ # SYMPTOM_TRIAGE_REMEDY
    # Ultra short
    "mild chest burning home remedy",
    "child 102f fever cold advice",
    "dry cough sore throat remedy",
    "joint pain dengue chikungunya symptom",
    "diabetes diet rural indian food",
    "headache natural remedy water",
    "typhoid fever early signs",
    "loose motion child ors zinc",
    # Hinglish
    "do din se khana khane ke baad halki छाती me jalan ho rahi hai koi ghar ka nuskha batao",
    "mere 5 saal ke bache ko subah se 102 fever aur thand lag rahi hai kya kare?",
    "sukhi khansi aur gale me kharash ke liye konsa safe desi ilaj kare?",
    "jodon me dard aur body par red rash hain, kya ye dengue ya chikungunya ho sakta hai?",
    "gaav me rehne wale diabetic patient ko blood sugar control karne ke liye kya khana chahiye?",
    "sar me dard ho raha hai halka halka, doctor ke paas jana zaroori hai ya ghar pe theek ho jayega?",
    "typhoid bukhar ke shuruaati lakshan kya hote hain aur test kab karaye?",
    "bache ko loose motion ho gaya hai, ors ghul aur zinc ki goli kaise de?",
    # Voice-STT
    "doctor sahab mere bete ko subah se bukhar hai aur khansi aa rahi hai pehla ilaj kya kare",
    "gale me kharash aur khansi ke liye garam paani aur haldi wala doodh pee sakte hain kya",
    "dengue bukhar me platelet badhane ke liye ghar me kya khana chahiye",
    "pet me dard aur ulti ho rahi hai ghar pe kya kare ilaj",
    # Detailed
    "A 40-year-old adult experiencing mild post-prandial heartburn and acid reflux for 2 days without red-flag cardiac symptoms. What are the ICMR-approved dietary home remedies?",
    "My 6-year-old child has a 101F fever and dry cough since yesterday. What baseline triage protocol and hydration measures should I follow at home?"
]

VARIATIONS_CLASS_6 = [ # OUT_OF_SCOPE_GENERAL
    # Ultra short
    "namaste who are you",
    "how to change language marathi",
    "thank you arogyamitra",
    "weather forecast indore today",
    "cricket match score india",
    "tell a doctor joke",
    "capital of madhya pradesh",
    "python code sorting array",
    # Hinglish
    "namaste arogyamitra, aap kaun ho aur meri kya help kar sakte ho?",
    "bhaiya app me bolne ki bhasha marathi ya tamil me kaise badle?",
    "bahot bahot dhanyawad aapki madad ke liye!",
    "aaj indore me barish hogi kya mausam kaisa hai?",
    "kal ka cricket match kaun jeeta india ya australia?",
    "mujhe ek accha doctor wala joke sunao na",
    "madhya pradesh ki rajdhani konsi hai?",
    "python me list ko sort karne ka code likh kar do",
    # Voice-STT
    "hello arogyamitra namaste... tum kya kya bata sakte ho mujhe",
    "bhasha hindi se marathi me kaise change kare batao",
    "thank you so much bhai tumne bahot acchi jankari di",
    "aaj bhopal me temperature kitna hai",
    # Detailed
    "Namaste! Can you please introduce yourself and explain all the healthcare support services available on ArogyaMitra?",
    "How can I toggle the speech synthesis output voice from Hindi to Marathi or Telugu in the settings?"
]

CLASS_HUMANIZERS = {
    "EMERGENCY_CRITICAL": VARIATIONS_CLASS_1,
    "FACILITY_LOCATOR": VARIATIONS_CLASS_2,
    "GOVT_SCHEME_ELIGIBILITY": VARIATIONS_CLASS_3,
    "MEDICINE_GENERIC_SEARCH": VARIATIONS_CLASS_4,
    "SYMPTOM_TRIAGE_REMEDY": VARIATIONS_CLASS_5,
    "OUT_OF_SCOPE_GENERAL": VARIATIONS_CLASS_6
}

def is_templated_row(text: str) -> bool:
    """Returns True if the text contains artificial template suffixes or unnatural patterns."""
    patterns = [
        r"variant\s*\d+",
        r"inquiry\s*\d+",
        r"item\s*\d+",
        r"case\s*\d+",
        r"Pharmacology query:",
        r"Clinical symptom triage",
        r"Show location map for",
        r"What is the eligibility criteria and claim procedure for",
        r"What is the recommended dosage for Ibuprofen",
        r"Find blood bank with B positive blood in Jabalpur city"
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False

def main():
    print("=== DATASET PARAPHRASING & HUMANIZATION PREPROCESSOR ===")
    
    if not dataset_file.exists():
        print(f"Error: Dataset file not found at {dataset_file}")
        return

    with open(dataset_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded existing dataset: {len(rows)} rows.")
    
    # Categorize existing rows
    by_class = {}
    for r in rows:
        label = r["label"]
        text = r["text"].strip()
        by_class.setdefault(label, []).append(text)

    new_dataset = []
    
    for label, texts in by_class.items():
        pool = CLASS_HUMANIZERS.get(label, [])
        authentic_texts = []
        
        # Keep authentic non-templated texts
        for t in texts:
            if not is_templated_row(t):
                authentic_texts.append(t)
                
        print(f"Class [{label}]: Retained {len(authentic_texts)} authentic seed queries. Replacing {len(texts) - len(authentic_texts)} templated rows.")
        
        # Mix authentic texts with rich natural human variations to reach exactly 200
        combined = list(authentic_texts)
        
        # Shuffle pool to get maximum diversity across 4 styles
        shuffled_pool = list(pool)
        random.shuffle(shuffled_pool)
        
        pool_idx = 0
        while len(combined) < 200:
            if pool_idx < len(shuffled_pool):
                candidate = shuffled_pool[pool_idx]
                pool_idx += 1
            else:
                # Cycle through pool with subtle realistic prefix/suffix variations
                base = pool[pool_idx % len(pool)]
                var_style = pool_idx % 4
                if var_style == 0:
                    candidate = f"please tell me {base.lower()}"
                elif var_style == 1:
                    candidate = f"{base} please help"
                elif var_style == 2:
                    candidate = f"bhai {base.lower()}"
                else:
                    candidate = f"doctor sahab {base.lower()}"
                pool_idx += 1
                
            if candidate not in combined:
                combined.append(candidate)
                
        # Trim to exactly 200
        combined = combined[:200]
        for t in combined:
            new_dataset.append({"text": t, "label": label})

    # Overwrite the existing dataset CSV directly
    with open(dataset_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(new_dataset)

    print(f"\n==================================================")
    print(f"PARAPHRASING COMPLETE & DATASET OVERWRITTEN SUCCESSFUL!")
    print(f"File Path: {dataset_file}")
    print(f"Total Rows: {len(new_dataset)} (Exactly 200 per class across 6 classes)")
    print(f"Variability Styles Included: Ultra-Short Keywords, Hinglish, Voice-STT Speech, Detailed Clinical Scenarios.")
    print(f"==================================================")

if __name__ == "__main__":
    main()
