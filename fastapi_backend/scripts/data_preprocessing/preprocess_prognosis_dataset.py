import os
import json
import random
import pandas as pd

# ---------------------------------------------------------------------------
# 1. LAYMAN SYMPTOM PHRASING MAPPING (132 SYMPTOMS)
# ---------------------------------------------------------------------------
SYMPTOM_LAYMAN_MAP = {
    'itching': ["persistent itching", "skin itchiness", "intense itching on my body"],
    'skin_rash': ["red skin rashes", "a sudden skin rash", "breakouts of skin rash"],
    'nodal_skin_eruptions': ["small bumpy skin eruptions", "nodular skin bumps", "raised skin eruptions"],
    'continuous_sneezing': ["continuous sneezing", "uncontrollable sneezing", "frequent sneezing fits"],
    'shivering': ["severe shivering", "shivering uncontrollably", "body shivering"],
    'chills': ["sudden cold chills", "feeling severe chills", "chills with fever"],
    'joint_pain': ["severe joint pain", "pain in my joints", "joint aches"],
    'stomach_pain': ["stomach pain", "pain in my stomach", "abdominal pain"],
    'acidity': ["acid reflux and acidity", "burning stomach acidity", "severe heart burn"],
    'ulcers_on_tongue': ["painful ulcers on my tongue", "canker sores on tongue"],
    'muscle_wasting': ["noticeable muscle wasting", "loss of muscle mass", "shrinking muscle volume"],
    'vomiting': ["frequent vomiting", "feeling nauseous and throwing up", "repeated vomiting episodes"],
    'burning_micturition': ["burning sensation while urinating", "painful burning urination"],
    'spotting_ urination': ["spotting of blood in urine", "small traces of blood during urination"],
    'fatigue': ["extreme fatigue and weakness", "constant tiredness", "overwhelming fatigue"],
    'weight_gain': ["unexplained weight gain", "sudden weight increase"],
    'anxiety': ["feeling anxious and nervous", "episodes of severe anxiety"],
    'cold_hands_and_feets': ["cold hands and feet", "chilly sensation in extremities"],
    'mood_swings': ["frequent mood swings", "unpredictable mood changes"],
    'weight_loss': ["rapid unexplained weight loss", "losing weight continuously"],
    'restlessness': ["feeling extremely restless", "inability to sit still or rest"],
    'lethargy': ["severe lethargy", "feeling sluggish and low on energy"],
    'patches_in_throat': ["white patches in my throat", "sore throat with visible patches"],
    'irregular_sugar_level': ["fluctuating blood sugar levels", "uncontrolled blood glucose levels"],
    'cough': ["persistent cough", "frequent coughing fits", "dry or wet cough"],
    'high_fever': ["high fever", "running a very high body temperature", "burning fever"],
    'sunken_eyes': ["sunken-looking eyes", "hallow sunken eyes from dehydration"],
    'breathlessness': ["shortness of breath", "difficulty breathing", "feeling breathless"],
    'sweating': ["excessive sweating", "profuse night sweats"],
    'dehydration': ["severe thirst and dehydration", "extreme dry mouth and dehydration"],
    'indigestion': ["indigestion and bloated stomach", "trouble digesting food"],
    'headache': ["throbbing headache", "severe headache", "persistent head pain"],
    'yellowish_skin': ["yellowish skin tone", "yellow tint on skin"],
    'dark_urine': ["dark brown or cola-colored urine", "unusually dark urine"],
    'nausea': ["constant nausea", "feeling sick to my stomach"],
    'loss_of_appetite': ["complete loss of appetite", "no desire to eat anything"],
    'pain_behind_the_eyes': ["deep pain behind my eyes", "aching sensation behind eyes"],
    'back_pain': ["severe back pain", "persistent backache"],
    'constipation': ["chronic constipation", "difficulty passing stool"],
    'abdominal_pain': ["sharp abdominal pain", "severe stomach cramps"],
    'diarrhoea': ["watery diarrhea", "loose watery motions"],
    'mild_fever': ["mild low-grade fever", "slight fever"],
    'yellow_urine': ["bright yellow urine"],
    'yellowing_of_eyes': ["yellowish discoloration of the eyes", "jaundice-like yellow eyes"],
    'acute_liver_failure': ["signs of acute liver distress", "severe abdominal swelling with jaundice"],
    'fluid_overload': ["fluid retention and swelling", "body water retention"],
    'swelling_of_stomach': ["bloated and swollen stomach", "abdominal swelling"],
    'swelled_lymph_nodes': ["swollen lymph nodes in neck and armpits", "swollen glands"],
    'malaise': ["general body discomfort and malaise", "feeling unwell overall"],
    'blurred_and_distorted_vision': ["blurred and distorted vision", "hazy eyesight"],
    'phlegm': ["thick phlegm production", "coughing up mucus and phlegm"],
    'throat_irritation': ["scratchy throat irritation", "sore irritated throat"],
    'redness_of_eyes': ["bloodshot red eyes", "eye redness and irritation"],
    'sinus_pressure': ["facial sinus pressure", "heavy pressure around nose and forehead"],
    'runny_nose': ["runny nose", "constant nasal discharge"],
    'congestion': ["nasal congestion", "blocked stuffy nose"],
    'chest_pain': ["chest pain and tightness", "pressure in the chest"],
    'weakness_in_limbs': ["weakness in arms and legs", "limb weakness"],
    'fast_heart_rate': ["rapid heart rate", "racing heartbeat"],
    'pain_during_bowel_movements': ["sharp pain during bowel movements"],
    'pain_in_anal_region': ["pain in the anal region"],
    'bloody_stool': ["passing blood in stool", "rectal bleeding"],
    'irritation_in_anus': ["anal itching and irritation"],
    'neck_pain': ["stiff neck pain", "aching neck muscles"],
    'dizziness': ["feeling dizzy and lightheaded", "episodes of dizziness"],
    'cramps': ["painful muscle cramps", "stomach cramps"],
    'bruising': ["unexplained body bruises", "easy skin bruising"],
    'obesity': ["unhealthy weight accumulation"],
    'swollen_legs': ["swelling in lower legs and ankles", "swollen legs"],
    'swollen_blood_vessels': ["prominent swollen blood vessels"],
    'puffy_face_and_eyes': ["puffy swelling around face and eyes"],
    'enlarged_thyroid': ["visible swelling in the neck (enlarged thyroid)"],
    'brittle_nails': ["weak and brittle nails"],
    'swollen_extremeties': ["swollen hands and feet"],
    'excessive_hunger': ["excessive hunger and constant craving for food"],
    'extra_marital_contacts': ["history of unprotected high-risk exposures"],
    'drying_and_tingling_lips': ["dry and tingling lips"],
    'slurred_speech': ["slurred or unclear speech"],
    'knee_pain': ["knee joint pain"],
    'hip_joint_pain': ["hip joint discomfort"],
    'muscle_weakness': ["overall muscle weakness"],
    'stiff_neck': ["neck stiffness making it hard to turn head"],
    'swelling_joints': ["swollen inflamed joints"],
    'movement_stiffness': ["stiffness during physical movement"],
    'spinning_movements': ["spinning sensation (vertigo)"],
    'loss_of_balance': ["loss of physical balance while walking"],
    'unsteadiness': ["feeling unsteady on my feet"],
    'weakness_of_one_body_side': ["weakness or numbness on one side of the body"],
    'loss_of_smell': ["complete loss of smell"],
    'bladder_discomfort': ["discomfort in lower abdomen bladder region"],
    'foul_smell_of urine': ["foul-smelling urine"],
    'continuous_feel_of_urine': ["constant urge to urinate"],
    'passage_of_gases': ["excessive gas and flatulence"],
    'internal_itching': ["deep internal itching sensation"],
    'toxic_look_(typhos)': ["dull, exhausted, and toxic facial appearance"],
    'depression': ["persistent low mood and depression"],
    'irritability': ["feeling extremely irritable"],
    'muscle_pain': ["widespread muscle aches"],
    'altered_sensorium': ["confusion and altered mental awareness"],
    'red_spots_over_body': ["tiny red spots spread over skin"],
    'belly_pain': ["sharp lower belly pain"],
    'abnormal_menstruation': ["irregular or painful menstrual cycles"],
    'dischromic _patches': ["discolored patches on the skin"],
    'watering_from_eyes': ["excessive watering from eyes"],
    'increased_appetite': ["abnormally increased appetite"],
    'polyuria': ["frequent urination throughout day and night"],
    'family_history': ["family medical history of similar conditions"],
    'mucoid_sputum': ["clear or white mucus sputum"],
    'rusty_sputum': ["rusty brownish-red sputum"],
    'lack_of_concentration': ["difficulty concentrating"],
    'visual_disturbances': ["flashing lights or visual disturbances"],
    'receiving_blood_transfusion': ["history of recent blood transfusion"],
    'receiving_unsterile_injections': ["history of receiving unsterile injections"],
    'coma': ["episodes of unconsciousness"],
    'stomach_bleeding': ["signs of gastrointestinal bleeding"],
    'distention_of_abdomen': ["visibly distended abdomen"],
    'history_of_alcohol_consumption': ["long-term history of heavy alcohol consumption"],
    'fluid_overload.1': ["body fluid accumulation"],
    'blood_in_sputum': ["coughing up blood-stained sputum"],
    'prominent_veins_on_calf': ["swollen prominent veins on calves"],
    'palpitations': ["feeling irregular rapid heart palpitations"],
    'painful_walking': ["severe pain while walking"],
    'pus_filled_pimples': ["pus-filled pimples and acne lesions"],
    'blackheads': ["blackheads and clogged facial pores"],
    'scurring': ["acne scarring on skin"],
    'skin_peeling': ["peeling and flaking skin"],
    'silver_like_dusting': ["silvery scaly dust over skin patches"],
    'small_dents_in_nails': ["pitting and tiny dents in nails"],
    'inflammatory_nails': ["painful swollen inflammatory nail beds"],
    'blister': ["fluid-filled skin blisters"],
    'red_sore_around_nose': ["red painful sores around nose and mouth"],
    'yellow_crust_ooze': ["honey-colored yellow crust oozing from skin sores"]
}

# ---------------------------------------------------------------------------
# 2. DISEASE METADATA MAP FOR ALL 41 DISEASES
# ---------------------------------------------------------------------------
DISEASE_METADATA = {
    "Malaria": {
        "display": "Malaria",
        "category": "endemic_vector_borne",
        "differentials": "Dengue Fever or Typhoid Fever",
        "red_flags": "high persistent fever, extreme lethargy, yellow eyes, or altered mental clarity",
        "tests": "Rapid Diagnostic Test (RDT) for Malaria, Peripheral Blood Smear, and Complete Blood Count (CBC)"
    },
    "Dengue": {
        "display": "Dengue Fever",
        "category": "endemic_vector_borne",
        "differentials": "Chikungunya or Malaria",
        "red_flags": "severe abdominal pain, persistent vomiting, bleeding gums/nose, or sudden shock",
        "tests": "Dengue NS1 Antigen, IgM/IgG antibody test, and daily CBC for platelet monitoring"
    },
    "Typhoid": {
        "display": "Typhoid Fever (Enteric Fever)",
        "category": "endemic_gi",
        "differentials": "Gastroenteritis, Dengue, or Acute Hepatitis",
        "red_flags": "high sustained fever, extreme weakness, bloody stool, or severe stomach distension",
        "tests": "Widal test, Blood Culture for Salmonella, and Complete Blood Count (CBC)"
    },
    "Gastroenteritis": {
        "display": "Acute Gastroenteritis",
        "category": "endemic_gi",
        "differentials": "Food Poisoning or Amoebic Dysentery",
        "red_flags": "inability to retain fluids, sunken eyes, dry mouth, or severe postural dizziness",
        "tests": "Stool routine & culture, serum electrolytes, and CBC"
    },
    "Jaundice": {
        "display": "Jaundice / Acute Hepatic Dysfunction",
        "category": "endemic_gi",
        "differentials": "Viral Hepatitis (A/E) or Biliary Obstruction",
        "red_flags": "intense yellow skin/eyes, pale clay-colored stool, or confusion",
        "tests": "Liver Function Test (LFT: Bilirubin, SGOT/SGPT), Abdominal Ultrasound, and Viral Serology"
    },
    "hepatitis A": {
        "display": "Hepatitis A",
        "category": "endemic_gi",
        "differentials": "Hepatitis E or Typhoid Fever",
        "red_flags": "dark brown urine, severe yellowing of eyes, persistent vomiting, or right upper abdominal pain",
        "tests": "Anti-HAV IgM test, LFT panel, and Abdominal Ultrasound"
    },
    "Hepatitis B": {
        "display": "Hepatitis B Infection",
        "category": "endemic_gi",
        "differentials": "Hepatitis C or Alcoholic Liver Disease",
        "red_flags": "unexplained bleeding, abdominal fluid buildup (ascites), or severe jaundice",
        "tests": "HBsAg (Hepatitis B Surface Antigen) test, HBV DNA PCR, and LFT panel"
    },
    "Hepatitis C": {
        "display": "Hepatitis C Infection",
        "category": "endemic_gi",
        "differentials": "Hepatitis B or Fatty Liver Disease",
        "red_flags": "chronic fatigue, swelling in legs/abdomen, or yellow skin/eyes",
        "tests": "Anti-HCV Antibody test, HCV RNA Quantitative PCR, and Liver Function Tests"
    },
    "Hepatitis D": {
        "display": "Hepatitis D (Coinfection)",
        "category": "endemic_gi",
        "differentials": "Acute Hepatitis B flare or Cirrhosis",
        "red_flags": "rapid onset jaundice, severe fatigue, or abdominal distention",
        "tests": "Anti-HDV Antibodies test, HBsAg test, and LFT panel"
    },
    "Hepatitis E": {
        "display": "Hepatitis E",
        "category": "endemic_gi",
        "differentials": "Hepatitis A or Waterborne Acute Gastroenteritis",
        "red_flags": "acute jaundice in pregnant women, persistent vomiting, or extreme lethargy",
        "tests": "Anti-HEV IgM test, LFT panel, and Abdominal Ultrasound"
    },
    "Alcoholic hepatitis": {
        "display": "Alcoholic Hepatitis",
        "category": "endemic_gi",
        "differentials": "Non-Alcoholic Fatty Liver Disease or Cirrhosis",
        "red_flags": "abdominal distension, confusion, vomiting blood, or deep jaundice",
        "tests": "LFT (AST/ALT ratio > 2), Ultrasound Abdomen, and Complete Blood Count"
    },
    "Chronic cholestasis": {
        "display": "Chronic Cholestasis",
        "category": "endemic_gi",
        "differentials": "Gallstones or Primary Biliary Cholangitis",
        "red_flags": "intense body itching, dark urine, pale stools, or severe abdominal pain",
        "tests": "Serum Alkaline Phosphatase (ALP), GGT, Bilirubin profile, and Ultrasound Abdomen"
    },
    "Peptic ulcer diseae": {
        "display": "Peptic Ulcer Disease",
        "category": "endemic_gi",
        "differentials": "GERD or Gastritis",
        "red_flags": "vomiting coffee-ground material, black tarry stool, or severe abdominal pain radiating to back",
        "tests": "Upper GI Endoscopy, H. pylori Stool Antigen test, and CBC"
    },
    "GERD": {
        "display": "Gastroesophageal Reflux Disease (GERD)",
        "category": "endemic_gi",
        "differentials": "Peptic Ulcer Disease or Esophagitis",
        "red_flags": "difficulty swallowing (dysphagia), unexplained weight loss, or persistent chest pain",
        "tests": "Upper GI Endoscopy and Esophageal pH Monitoring"
    },
    "Tuberculosis": {
        "display": "Pulmonary Tuberculosis",
        "category": "endemic_respiratory",
        "differentials": "Chronic Bronchitis, Pneumonia, or Lung Infection",
        "red_flags": "coughing up blood (hemoptysis), persistent fever over 3 weeks, profuse night sweats, or rapid weight loss",
        "tests": "Sputum AFB Stain & GeneXpert MTB/RIF test, Chest X-ray, and ESR/CBC"
    },
    "Pneumonia": {
        "display": "Pneumonia",
        "category": "endemic_respiratory",
        "differentials": "Acute Bronchitis or Pulmonary Tuberculosis",
        "red_flags": "high fever with sharp chest pain when breathing, rusty sputum, or severe breathlessness",
        "tests": "Chest X-ray (PA View), Complete Blood Count (CBC with differential), and Sputum Culture"
    },
    "Bronchial Asthma": {
        "display": "Bronchial Asthma",
        "category": "endemic_respiratory",
        "differentials": "Allergic Rhinitis or Acute Bronchitis",
        "red_flags": "gasping for air, blue tint on lips/nails (cyanosis), or inability to speak full sentences",
        "tests": "Spirometry / Pulmonary Function Test (PFT) and Chest X-ray"
    },
    "Common Cold": {
        "display": "Viral Upper Respiratory Tract Infection (Common Cold)",
        "category": "endemic_respiratory",
        "differentials": "Allergic Rhinitis or Influenza",
        "red_flags": "fever lasting >4 days, severe facial sinus pain, or difficulty breathing",
        "tests": "Clinical evaluation; routine CBC or Nasal Swab if symptoms persist"
    },
    "Urinary tract infection": {
        "display": "Urinary Tract Infection (UTI)",
        "category": "endemic_infection",
        "differentials": "Cystitis or Pyelonephritis (Kidney Infection)",
        "red_flags": "high fever with back/flank pain, chills, or visible blood in urine",
        "tests": "Urine Routine & Microscopy (Pus cells), Urine Culture & Sensitivity"
    },
    "Chicken pox": {
        "display": "Chickenpox (Varicella Zoster Infection)",
        "category": "endemic_vector_borne",
        "differentials": "Measles or Hand-Foot-Mouth Disease",
        "red_flags": "high fever, infected pus-filled blisters, or shortness of breath",
        "tests": "Clinical visual exam, Varicella Zoster IgM antibody test"
    },
    "Fungal infection": {
        "display": "Cutaneous Fungal Infection (Tinea / Ringworm)",
        "category": "endemic_infection",
        "differentials": "Psoriasis or Contact Dermatitis",
        "red_flags": "spreading painful sores, pus oozing, or secondary bacterial infection",
        "tests": "KOH Skin Scraping preparation and fungal culture"
    },
    "Impetigo": {
        "display": "Impetigo (Bacterial Skin Infection)",
        "category": "endemic_infection",
        "differentials": "Ecthyma or Herpes Simplex",
        "red_flags": "rapidly spreading honey-crusted lesions, swollen lymph nodes, or fever",
        "tests": "Skin swab culture & sensitivity test"
    },
    "Diabetes": {
        "display": "Diabetes Mellitus",
        "category": "endemic_infection",
        "differentials": "Prediabetes or Metabolic Syndrome",
        "red_flags": "extreme thirst, frequent urination, fruity breath odor, or non-healing foot ulcers",
        "tests": "Fasting Blood Glucose, Postprandial Blood Sugar, and HbA1c test"
    },
    "Hypertension": {
        "display": "Essential Hypertension (High Blood Pressure)",
        "category": "endemic_infection",
        "differentials": "Secondary Hypertension or Anxiety Disorder",
        "red_flags": "severe occipital headache, blurred vision, chest tightness, or dizziness",
        "tests": "Digital Blood Pressure Monitoring, ECG, and Renal Function Tests (KFT)"
    },
    "Hypoglycemia": {
        "display": "Hypoglycemia (Low Blood Sugar)",
        "category": "endemic_infection",
        "differentials": "Vasovagal Syncope or Panic Attack",
        "red_flags": "confusion, loss of consciousness, cold sweats, or seizures",
        "tests": "Immediate capillary blood glucose test (Glucometer)"
    },
    "Hypothyroidism": {
        "display": "Hypothyroidism",
        "category": "endemic_infection",
        "differentials": "Hashimoto's Thyroiditis or Chronic Fatigue Syndrome",
        "red_flags": "extreme cold intolerance, marked weight gain, severe depression, or hoarseness",
        "tests": "Serum Thyroid Profile (TSH, Free T3, Free T4)"
    },
    "Hyperthyroidism": {
        "display": "Hyperthyroidism (Thyrotoxicosis)",
        "category": "endemic_infection",
        "differentials": "Graves' Disease or Toxic Nodular Goiter",
        "red_flags": "rapid irregular heart rate (palpitations), trembling hands, or sudden weight loss",
        "tests": "Serum Thyroid Profile (TSH, Free T3, Free T4) and Thyroid Scan"
    },
    "Acne": {
        "display": "Acne Vulgaris",
        "category": "endemic_infection",
        "differentials": "Folliculitis or Rosacea",
        "red_flags": "painful deep cystic lesions or spreading facial swelling",
        "tests": "Dermatological visual assessment"
    },
    "Psoriasis": {
        "display": "Psoriasis",
        "category": "endemic_infection",
        "differentials": "Eczema or Seborrheic Dermatitis",
        "red_flags": "joint pain accompanied by skin lesions (Psoriatic Arthritis) or erythroderma",
        "tests": "Clinical skin evaluation and Skin Biopsy if diagnostic doubt exists"
    },
    "Allergy": {
        "display": "Allergic Reaction / Rhinitis",
        "category": "general",
        "differentials": "Viral Upper Respiratory Infection or Urticaria",
        "red_flags": "facial/lip swelling (angioedema), wheezing, or tightness in throat",
        "tests": "Absolute Eosinophil Count (AEC) and Total Serum IgE test"
    },
    "Drug Reaction": {
        "display": "Adverse Drug Reaction / Cutaneous Eruption",
        "category": "general",
        "differentials": "Viral Exanthem or Contact Dermatitis",
        "red_flags": "blistering skin, mucosal peeling (Stevens-Johnson Syndrome), or fever",
        "tests": "Complete Blood Count, Renal & Liver Function Tests"
    },
    "AIDS": {
        "display": "HIV/AIDS Immunodeficiency",
        "category": "general",
        "differentials": "Opportunistic Infections or Chronic Lymphoma",
        "red_flags": "recurrent high fever, rapid weight loss, persistent oral thrush, or chronic diarrhea",
        "tests": "HIV 1/2 ELISA Screening, Western Blot, and CD4+ T-cell count"
    },
    "Heart attack": {
        "display": "Myocardial Infarction (Heart Attack)",
        "category": "general",
        "differentials": "Angina Pectoris or Severe GERD",
        "red_flags": "crushing retrosternal chest pain radiating to left arm/jaw, cold sweating, or breathlessness",
        "tests": "Immediate 12-lead ECG, Cardiac Troponin I/T blood markers, and Echocardiogram"
    },
    "Paralysis (brain hemorrhage)": {
        "display": "Cerebrovascular Accident / Hemorrhagic Stroke",
        "category": "general",
        "differentials": "Ischemic Stroke or Transient Ischemic Attack (TIA)",
        "red_flags": "sudden facial droop, arm weakness, slurred speech, or loss of consciousness",
        "tests": "Emergency Non-contrast CT Scan of Brain or Brain MRI"
    },
    "(vertigo) Paroymsal  Positional Vertigo": {
        "display": "Benign Paroxysmal Positional Vertigo (BPPV)",
        "category": "general",
        "differentials": "Labyrinthitis or Vestibular Neuritis",
        "red_flags": "constant unremitting spinning, severe hearing loss, or weakness in limbs",
        "tests": "Dix-Hallpike Maneuver and Neurological examination"
    },
    "Migraine": {
        "display": "Migraine Headache",
        "category": "general",
        "differentials": "Tension Headache or Sinus Headache",
        "red_flags": "thunderclap onset headache, neck stiffness, fever, or visual field loss",
        "tests": "Neurological examination; Brain MRI/CT if red flag symptoms present"
    },
    "Cervical spondylosis": {
        "display": "Cervical Spondylosis",
        "category": "general",
        "differentials": "Cervical Radiculopathy or Muscle Strain",
        "red_flags": "numbness/tingling in hands, loss of balance, or loss of bowel/bladder control",
        "tests": "Cervical Spine X-ray (AP/Lateral) and Cervical MRI"
    },
    "Dimorphic hemmorhoids(piles)": {
        "display": "Hemorrhoids (Piles)",
        "category": "general",
        "differentials": "Anal Fissure or Colorectal Polyps",
        "red_flags": "heavy bright red rectal bleeding, dizziness, or severe perianal pain",
        "tests": "Anoscopy / Digital Rectal Examination and Colonoscopy if indicated"
    },
    "Varicose veins": {
        "display": "Varicose Veins",
        "category": "general",
        "differentials": "Deep Vein Thrombosis (DVT) or Venous Insufficiency",
        "red_flags": "sudden single leg swelling, skin discoloration, or non-healing stasis ulcer",
        "tests": "Venous Doppler Ultrasound of lower limbs"
    },
    "Osteoarthristis": {
        "display": "Osteoarthritis",
        "category": "general",
        "differentials": "Rheumatoid Arthritis or Gout",
        "red_flags": "severe joint deformity, hot swollen joint, or inability to bear weight",
        "tests": "Joint X-ray, Serum Uric Acid, and ESR"
    },
    "Arthritis": {
        "display": "Rheumatoid / Inflammatory Arthritis",
        "category": "general",
        "differentials": "Osteoarthritis or Systemic Lupus Erythematosus (SLE)",
        "red_flags": "morning joint stiffness lasting >1 hour, joint redness, or fever",
        "tests": "Rheumatoid Factor (RF), Anti-CCP antibodies, and ESR/CRP"
    }
}

PATIENT_OPENERS = [
    "Doctor, I've been experiencing {symptoms}. What could this be?",
    "Hello Doctor, I have {symptoms}. Should I be worried?",
    "Hi, I am suffering from {symptoms}. Please guide me on what could be wrong.",
    "Greetings, my main symptoms are {symptoms}. What diagnostic tests should I get?",
    "Doctor, I'm feeling unwell with {symptoms}. What disease might cause these symptoms?",
    "I have been having {symptoms} for a few days now. Can you evaluate this?",
    "Hi Doctor, I am experiencing {symptoms}. What should my next clinical steps be?"
]

SYSTEM_PROMPT = "You are ArogyaMitra, an empathetic rural healthcare AI assistant. Provide concise differential diagnostic logic, highlight warning red flags requiring in-person evaluation, and recommend clinical tests under 120 words."


def convert_row_to_layman_symptoms(row, symptom_cols):
    """Convert binary 1 indicators into natural layman symptom text."""
    active_symptoms = [c for c in symptom_cols if row[c] == 1]
    if len(active_symptoms) < 2:
        return None, active_symptoms

    phrases = []
    for sym in active_symptoms:
        options = SYMPTOM_LAYMAN_MAP.get(sym, [sym.replace('_', ' ')])
        phrases.append(random.choice(options))

    if len(phrases) == 2:
        symptom_text = f"{phrases[0]} and {phrases[1]}"
    else:
        symptom_text = ", ".join(phrases[:-1]) + f", and {phrases[-1]}"

    return symptom_text, active_symptoms


def generate_assistant_response(disease_raw):
    """Generate structured response strictly under 120 words."""
    meta = DISEASE_METADATA.get(disease_raw, {
        "display": disease_raw,
        "differentials": "other viral or metabolic conditions",
        "red_flags": "high persistent fever, difficulty breathing, or severe abdominal pain",
        "tests": "Complete Blood Count (CBC) and routine clinical evaluation"
    })

    display = meta["display"]
    diffs = meta["differentials"]
    red_flags = meta["red_flags"]
    tests = meta["tests"]

    response = (
        f"Based on your symptoms, the primary suspect is {display}. "
        f"Differential possibilities include {diffs}.\n\n"
        f"⚠️ Warning Red Flags: Seek emergency clinical care immediately if you experience {red_flags}.\n\n"
        f"Recommended Action: Get a clinical evaluation and relevant testing, including {tests}. Stay hydrated and rest."
    )

    words = response.split()
    if len(words) >= 120:
        response = (
            f"Based on symptoms, the primary suspect is {display} (differentials: {diffs}).\n\n"
            f"⚠️ Warning Red Flags: Seek urgent care for {red_flags}.\n\n"
            f"Next Steps: Consult a doctor for {tests}."
        )

    return response


def main():
    base_dir = r"D:\MCA Sage Uni\Semester-3\Project Ideas\ArogyaMitra\fastapi_backend"
    dataset_dir = os.path.join(base_dir, "datasets", "fine-tuning", "k-prognosis")

    train_path = os.path.join(dataset_dir, "Training.csv")
    test_path = os.path.join(dataset_dir, "Testing.csv")

    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print(f"Error: Dataset files not found in {dataset_dir}")
        return

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    df = pd.concat([train_df, test_df], ignore_index=True)
    df.columns = [c.strip() for c in df.columns]

    if 'Unnamed: 133' in df.columns:
        df = df.drop(columns=['Unnamed: 133'])

    # Clean string whitespace in prognosis target column
    df['prognosis'] = df['prognosis'].astype(str).str.strip()

    symptom_cols = [c for c in df.columns if c != 'prognosis']

    # Filter out rows with < 2 symptoms
    df['symptom_count'] = df[symptom_cols].sum(axis=1)
    df = df[df['symptom_count'] >= 2].copy()

    # Classify endemic vs general diseases
    endemic_diseases = []
    other_diseases = []

    for disease in df['prognosis'].unique():
        meta = DISEASE_METADATA.get(disease, {})
        cat = meta.get('category', 'general')
        if cat in ['endemic_vector_borne', 'endemic_gi', 'endemic_respiratory', 'endemic_infection']:
            endemic_diseases.append(disease)
        else:
            other_diseases.append(disease)

    print(f"Total Rows: {len(df)}")
    print(f"Endemic Diseases ({len(endemic_diseases)}): {endemic_diseases[:5]}...")
    print(f"Other Diseases ({len(other_diseases)}): {other_diseases[:5]}...")

    # Target: Exactly 800 ChatML pairs (75% endemic, 25% other)
    TARGET_SIZE = 800
    chatml_data = []

    endemic_df = df[df['prognosis'].isin(endemic_diseases)]
    other_df = df[df['prognosis'].isin(other_diseases)]

    endemic_samples = endemic_df.sample(n=600, replace=True, random_state=42)
    other_samples = other_df.sample(n=200, replace=True, random_state=42)

    combined_samples = pd.concat([endemic_samples, other_samples]).sample(frac=1.0, random_state=42).reset_index(drop=True)

    word_count_exceeded = 0

    for idx, row in combined_samples.iterrows():
        disease_raw = row['prognosis']
        layman_text, active_syms = convert_row_to_layman_symptoms(row, symptom_cols)

        if not layman_text:
            continue

        opener = random.choice(PATIENT_OPENERS)
        user_content = opener.format(symptoms=layman_text)
        assistant_content = generate_assistant_response(disease_raw)

        w_count = len(assistant_content.split())
        if w_count >= 120:
            word_count_exceeded += 1

        sample = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content}
            ]
        }
        chatml_data.append(sample)

    print(f"Successfully generated {len(chatml_data)} ChatML pairs.")
    print(f"Responses exceeding 120 words: {word_count_exceeded}")

    # Output path
    out_dir = os.path.join(base_dir, "datasets", "fine-tuning")
    os.makedirs(out_dir, exist_ok=True)

    out_file = os.path.join(out_dir, "k-prognosis.json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(chatml_data, f, indent=2, ensure_ascii=False)

    print(f"Saved dataset to {out_file}")


if __name__ == "__main__":
    main()

