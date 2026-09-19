import json
import os
import re
import random

BASE_DIR = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend"
GRETEL_DIR = os.path.join(BASE_DIR, "datasets", "fine-tuning", "hf-gretelAI")
OUTPUT_DIR = os.path.join(BASE_DIR, "datasets", "fine-tuning")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "hf-gretel-clean.json")

SYSTEM_PROMPT = "You are ArogyaMitra, an empathetic rural healthcare AI assistant. Provide concise differential diagnostic logic, reflect symptoms clearly, explain potential causes simply, and outline self-monitoring steps and warning flags under 120 words."

LABEL_MAP = {
    'allergy': 'Allergy',
    'arthritis': 'Arthritis',
    'bronchial asthma': 'Bronchial Asthma',
    'cervical spondylosis': 'Cervical Spondylosis',
    'chicken pox': 'Chickenpox',
    'common cold': 'Common Cold',
    'dengue': 'Dengue',
    'diabetes': 'Diabetes',
    'drug reaction': 'Drug Reaction',
    'fungal infection': 'Fungal Infection',
    'gastroesophageal reflux disease': 'GERD',
    'hypertension': 'Hypertension',
    'impetigo': 'Impetigo',
    'jaundice': 'Jaundice',
    'malaria': 'Malaria',
    'migraine': 'Migraine',
    'peptic ulcer disease': 'Peptic Ulcer Disease',
    'pneumonia': 'Pneumonia',
    'psoriasis': 'Psoriasis',
    'typhoid': 'Typhoid',
    'urinary tract infection': 'Urinary Tract Infection (UTI)',
    'varicose veins': 'Varicose Veins'
}

DISEASE_METADATA = {
    'Allergy': {
        'display': 'Allergic Reaction',
        'differentials': 'Contact Dermatitis or Rhinitis',
        'red_flags': 'throat swelling, difficulty breathing, or anaphylaxis',
        'monitoring': 'Track triggers like dust or food, keep skin clean, and stay hydrated.'
    },
    'Arthritis': {
        'display': 'Rheumatoid / Inflammatory Arthritis',
        'differentials': 'Osteoarthritis or Gout',
        'red_flags': 'severe joint deformity, extreme morning stiffness, or hot swollen joints',
        'monitoring': 'Gentle joint mobility exercises, rest during flare-ups, and avoid joint strain.'
    },
    'Bronchial Asthma': {
        'display': 'Bronchial Asthma',
        'differentials': 'Bronchitis or Allergic Airway Disease',
        'red_flags': 'severe breathlessness, blue lips/fingers, or inability to speak full sentences',
        'monitoring': 'Monitor peak flow, avoid cold air and smoke, and keep inhaler accessible.'
    },
    'Cervical Spondylosis': {
        'display': 'Cervical Spondylosis',
        'differentials': 'Cervical Disc Herniation or Muscle Strain',
        'red_flags': 'numbness or weakness in arms, loss of bowel/bladder control, or severe dizziness',
        'monitoring': 'Maintain neck posture, perform mild stretching, and avoid heavy lifting.'
    },
    'Chickenpox': {
        'display': 'Chickenpox (Varicella Virus)',
        'differentials': 'Measles or Hand-Foot-Mouth Disease',
        'red_flags': 'high unyielding fever, skin rash infection with pus, or shortness of breath',
        'monitoring': 'Isolate to prevent spread, apply soothing lotion, avoid scratching blisters.'
    },
    'Common Cold': {
        'display': 'Common Cold (Viral Upper Respiratory Infection)',
        'differentials': 'Influenza or Sinusitis',
        'red_flags': 'fever lasting >3 days, severe chest pain, or worsening shortness of breath',
        'monitoring': 'Rest adequately, drink warm fluids, and monitor temperature regularly.'
    },
    'Dengue': {
        'display': 'Dengue Fever',
        'differentials': 'Chikungunya, Malaria, or Viral Fever',
        'red_flags': 'persistent vomiting, bleeding gums, abdominal pain, or sudden extreme fatigue',
        'monitoring': 'Monitor platelet count daily, ensure high oral fluid intake, and rest strictly.'
    },
    'Diabetes': {
        'display': 'Diabetes Mellitus',
        'differentials': 'Hyperglycemia or Metabolic Disorder',
        'red_flags': 'extreme confusion, rapid breathing, fruity breath odor, or non-healing foot ulcers',
        'monitoring': 'Check blood sugar regularly, maintain balanced diet, and check feet daily.'
    },
    'Drug Reaction': {
        'display': 'Adverse Drug Reaction / Medication Allergy',
        'differentials': 'Viral Exanthem or Food Allergy',
        'red_flags': 'widespread skin blistering, facial swelling, or difficulty swallowing',
        'monitoring': 'Stop suspect non-essential medication immediately and seek clinical advice.'
    },
    'Fungal Infection': {
        'display': 'Fungal Skin Infection (Tinea / Dermatophytosis)',
        'differentials': 'Eczema or Psoriasis',
        'red_flags': 'rapidly spreading red painful skin, pus formation, or systemic fever',
        'monitoring': 'Keep affected area clean and dry, avoid sharing towels, wear loose cotton clothes.'
    },
    'GERD': {
        'display': 'GERD (Gastroesophageal Reflux Disease)',
        'differentials': 'Gastritis or Peptic Ulcer Disease',
        'red_flags': 'difficulty swallowing, vomiting blood, black tarry stools, or crushing chest pain',
        'monitoring': 'Avoid spicy/fatty meals, do not lie down immediately after eating, elevate head.'
    },
    'Hypertension': {
        'display': 'Hypertension (High Blood Pressure)',
        'differentials': 'Essential Hypertension or Secondary Renal Disease',
        'red_flags': 'severe sudden headache, chest pain, blurred vision, or shortness of breath',
        'monitoring': 'Check BP regularly, reduce salt intake, avoid stress, and take prescribed medicines.'
    },
    'Impetigo': {
        'display': 'Impetigo (Bacterial Skin Infection)',
        'differentials': 'Herpes Simplex or Ecthyma',
        'red_flags': 'honey-colored crusts spreading rapidly, fever, or painful swollen lymph nodes',
        'monitoring': 'Wash lesions gently with soap, cover loosely, and avoid touching or scratching.'
    },
    'Jaundice': {
        'display': 'Jaundice / Acute Viral Hepatitis',
        'differentials': 'Gallstones or Alcoholic Liver Disease',
        'red_flags': 'deep yellowing of eyes/skin, dark tea-colored urine, severe abdominal pain, or confusion',
        'monitoring': 'Rest completely, drink boiled clean water, avoid oily/fatty foods, check liver enzymes.'
    },
    'Malaria': {
        'display': 'Malaria',
        'differentials': 'Dengue or Typhoid Fever',
        'red_flags': 'rigors/shivering chills with high fever spikes, jaundice, or extreme lethargy',
        'monitoring': 'Get immediate blood smear test, monitor fever pattern, use mosquito protection.'
    },
    'Migraine': {
        'display': 'Migraine Headache',
        'differentials': 'Tension Headache or Sinus Headache',
        'red_flags': 'sudden worst headache of life, neck stiffness, high fever, or vision loss',
        'monitoring': 'Rest in a quiet dark room, stay hydrated, track headache triggers in a journal.'
    },
    'Peptic Ulcer Disease': {
        'display': 'Peptic Ulcer Disease',
        'differentials': 'Gastritis or GERD',
        'red_flags': 'vomiting coffee-ground material, black tarry stools, or sudden sharp belly pain',
        'monitoring': 'Eat small frequent bland meals, avoid NSAID pain relievers and alcohol.'
    },
    'Pneumonia': {
        'display': 'Pneumonia (Lower Respiratory Infection)',
        'differentials': 'Severe Bronchitis or Pulmonary Tuberculosis',
        'red_flags': 'high fever with chills, chest pain during breathing, rusty sputum, or low oxygen',
        'monitoring': 'Check oxygen saturation, monitor respiratory rate, stay warm and well hydrated.'
    },
    'Psoriasis': {
        'display': 'Psoriasis',
        'differentials': 'Seborrheic Dermatitis or Lichen Planus',
        'red_flags': 'widespread skin redness over >80% body, severe joint pain, or skin infection',
        'monitoring': 'Moisturize skin daily, avoid skin injury, manage stress, avoid harsh soaps.'
    },
    'Typhoid': {
        'display': 'Typhoid Fever (Enteric Fever)',
        'differentials': 'Malaria, Dengue, or Gastroenteritis',
        'red_flags': 'step-ladder high fever, severe abdominal distension, diarrhea, or delirium',
        'monitoring': 'Drink only boiled water, maintain strict hand hygiene, get Widal or Blood Culture test.'
    },
    'Urinary Tract Infection (UTI)': {
        'display': 'Urinary Tract Infection (UTI)',
        'differentials': 'Pyelonephritis or Cystitis',
        'red_flags': 'high fever with flank/back pain, chills, vomiting, or heavy blood in urine',
        'monitoring': 'Drink plenty of water (2-3L/day), do not hold urine, track urination frequency.'
    },
    'Varicose Veins': {
        'display': 'Varicose Veins',
        'differentials': 'Deep Vein Thrombosis (DVT) or Chronic Venous Insufficiency',
        'red_flags': 'sudden leg swelling/warmth, skin ulcers near ankle, or severe calf pain',
        'monitoring': 'Elevate legs while resting, avoid standing for long periods, wear compression socks.'
    },
    'Tuberculosis': {
        'display': 'Pulmonary Tuberculosis (TB)',
        'differentials': 'Chronic Bronchitis or Lung Infection',
        'red_flags': 'coughing up blood, persistent evening fever, night sweats, or rapid weight loss',
        'monitoring': 'Get Sputum Smear test and Chest X-ray, wear mask, ensure proper room ventilation.'
    },
    'Gastroenteritis': {
        'display': 'Acute Gastroenteritis / Stomach Infection',
        'differentials': 'Food Poisoning or Amoebiasis',
        'red_flags': 'inability to keep liquids down, sunken eyes, extreme thirst, or bloody diarrhea',
        'monitoring': 'Sip ORS solution frequently, eat light bland diet (BRAT), monitor hydration level.'
    }
}

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<\|.*?\|>', '', text)
    text = re.sub(r'\[(USER|BOT|INST|/INST)\]', '', text)
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([\.\,\!\?])', r'', text)
    text = re.sub(r'\.\.+', '.', text)
    if text and not text[0].isupper():
        text = text[0].upper() + text[1:]
    return text

def build_assistant_response(disease_key):
    meta = DISEASE_METADATA.get(disease_key, {
        'display': disease_key,
        'differentials': 'other medical conditions',
        'red_flags': 'severe worsening pain, high fever, or breathing difficulty',
        'monitoring': 'Monitor your symptoms closely and rest.'
    })
    display = meta['display']
    diffs = meta['differentials']
    red_flags = meta['red_flags']
    monitoring = meta['monitoring']

    p1 = f"I understand your symptoms. Based on your description, the primary condition to consider is {display}. Differential possibilities include {diffs}."
    p2 = f"Self-Monitoring Steps: {monitoring}"
    p3 = f"Red Flags: Seek immediate medical care if you notice {red_flags}."
    return p1 + "\n\n" + p2 + "\n\n" + p3

def main():
    rows_by_class = {cls: [] for cls in DISEASE_METADATA.keys()}

    for fn in ['train.jsonl', 'test.jsonl']:
        fp = os.path.join(GRETEL_DIR, fn)
        if not os.path.exists(fp):
            continue
        with open(fp, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip(): continue
                item = json.loads(line)
                raw_label = item.get('output_text', '').strip().lower()
                mapped_label = LABEL_MAP.get(raw_label)
                if mapped_label in rows_by_class:
                    cleaned_inp = clean_text(item.get('input_text', ''))
                    if cleaned_inp:
                        rows_by_class[mapped_label].append(cleaned_inp)

    tb_samples = [
        "I have had a persistent cough for over three weeks, night sweats, low fever in the evenings, and unexplained weight loss.",
        "I am coughing up yellow phlegm with occasional blood spots, feeling fatigued, and having chest pain while breathing.",
        "I feel very weak and exhausted. I have an ongoing cough, fever at night, loss of appetite, and significant weight loss.",
        "Doctor, I have been having continuous fever, heavy coughing, sweating heavily during sleep, and loss of weight.",
        "I have a deep dry cough that will not go away, mild evening fever, chest tightness, and general weakness."
    ]
    ge_samples = [
        "I have severe stomach cramps, frequent watery diarrhea, nausea, and vomiting after eating food outside.",
        "I am experiencing watery loose stools, abdominal pain, mild fever, and extreme weakness from dehydration.",
        "Doctor, I have been vomiting since morning, having belly cramps, and continuous watery diarrhea.",
        "I feel very thirsty, dizzy when standing up, and have constant loose motions and stomach pain.",
        "I have nausea, stomach rumbling, loss of appetite, frequent watery stool, and mild chills."
    ]

    while len(rows_by_class['Tuberculosis']) < 50:
        rows_by_class['Tuberculosis'].append(random.choice(tb_samples))
    while len(rows_by_class['Gastroenteritis']) < 50:
        rows_by_class['Gastroenteritis'].append(random.choice(ge_samples))

    chatml_pairs = []
    total_count = 0

    random.seed(42)
    for disease_cls, texts in sorted(rows_by_class.items()):
        if len(texts) >= 50:
            selected_texts = random.sample(texts, 50)
        else:
            selected_texts = texts + random.choices(texts, k=50 - len(texts))

        for text in selected_texts:
            user_turn = clean_text(text)
            assistant_turn = build_assistant_response(disease_cls)

            item = {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_turn},
                    {"role": "assistant", "content": assistant_turn}
                ]
            }
            chatml_pairs.append(item)
            total_count += 1

    print(f"Total ChatML Pairs Generated: {len(chatml_pairs)} across {len(rows_by_class)} disease classes.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(chatml_pairs, f, indent=2, ensure_ascii=False)

    print(f"Dataset successfully exported to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
