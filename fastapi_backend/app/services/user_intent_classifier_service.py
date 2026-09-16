import re
import logging
import torch
from typing import Tuple, Dict, Any
from sentence_transformers import SentenceTransformer, util
from app.schemas.user_intent_classifier import IntentEnum, ExtractedSlots

logger = logging.getLogger(__name__)

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", 
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", 
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", 
    "Uttarakhand", "West Bengal", "Delhi", "MP", "UP", "AP", "TN", "WB"
]

SPECIALTIES_MAP = {
    "skin": "Dermatology (Skin)",
    "dermatologist": "Dermatology (Skin)",
    "dermatology": "Dermatology (Skin)",
    "eye": "Ophthalmology (Eye)",
    "ophthalmologist": "Ophthalmology (Eye)",
    "heart": "Cardiology (Heart)",
    "cardiologist": "Cardiology (Heart)",
    "child": "Pediatrics (Child)",
    "pediatrician": "Pediatrics (Child)",
    "maternity": "Gynecology (Maternity)",
    "pregnancy": "Gynecology (Maternity)",
    "bone": "Orthopedics (Bone)",
    "orthopedic": "Orthopedics (Bone)",
    "dental": "Dentistry (Dental)",
    "dentist": "Dentistry (Dental)"
}

PROTOTYPES = {
    IntentEnum.GOVT_SCHEMES_DISCOVERY: [
        "Which government health scheme can I avail in Madhya Pradesh state?",
        "Tell me about government health insurance yojana benefits and eligibility rules",
        "Financial support for hospital bills maternity subsidy and ayushman bharat card",
        "Free treatment government healthcare scheme eligibility documents required"
    ],
    IntentEnum.FACILITY_DISCOVERY: [
        "Which is the nearest hospital or clinic for skin disease around 462001?",
        "Find primary health center CHC PHC hospital near me in Bhopal",
        "Government doctor emergency ICU ambulance public healthcare facility locator",
        "Nearest eye doctor government hospital location contact address"
    ],
    IntentEnum.GENERAL_MEDICAL_QA: [
        "I have severe fever and headache since yesterday what should I do?",
        "What are the symptoms and home remedies for common cold and throat infection?",
        "What is the treatment for stomach pain and fever?"
    ],
    IntentEnum.GREETING_CONVERSATIONAL: [
        "Hello good morning how are you doing",
        "Hi tell me what can you help me with",
        "Namaste thank you very much"
    ]
}

class UserIntentClassifierService:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._model = None
        self._centroid_embeddings = {}
        self._load_model()

    def _load_model(self):
        try:
            logger.info(f"Loading SentenceTransformer model ({self.model_name})...")
            self._model = SentenceTransformer(self.model_name)
        except Exception as e:
            logger.warning(f"Failed to load {self.model_name}: {e}. Falling back to all-MiniLM-L6-v2")
            self.model_name = "all-MiniLM-L6-v2"
            self._model = SentenceTransformer(self.model_name)

        for intent, sentences in PROTOTYPES.items():
            embeddings = self._model.encode(sentences, convert_to_tensor=True)
            centroid = torch.mean(embeddings, dim=0, keepdim=True)
            self._centroid_embeddings[intent] = centroid

        logger.info("UserIntentClassifierService initialized successfully with pre-computed centroids.")

    def extract_slots(self, text: str) -> ExtractedSlots:
        slots = ExtractedSlots()
        lower_text = text.lower()

        pincode_match = re.search(r'\b[1-9][0-9]{5}\b', text)
        if pincode_match:
            slots.pincode = pincode_match.group(0)

        for state in INDIAN_STATES:
            pattern = r'\b' + re.escape(state.lower()) + r'\b'
            if re.search(pattern, lower_text):
                if state.upper() in ["MP", "MADHYA PRADESH"]:
                    slots.state = "Madhya Pradesh"
                elif state.upper() in ["UP", "UTTAR PRADESH"]:
                    slots.state = "Uttar Pradesh"
                else:
                    slots.state = state
                break

        for key, val in SPECIALTIES_MAP.items():
            if re.search(r'\b' + re.escape(key) + r'\b', lower_text):
                slots.specialty = val
                break

        return slots

    def classify_intent(self, text: str) -> Tuple[IntentEnum, float, str]:
        lower_text = text.lower().strip()

        if re.match(r'^(hi|hello|hey|namaste|good morning|good evening|thanks|thank you)[!\.]?$', lower_text):
            return IntentEnum.GREETING_CONVERSATIONAL, 1.0, "REGEX_FAST_PATH"

        scheme_keywords = r'\b(scheme|yojana|bima|subsidy|govt benefit|financial support|ayushman|myscheme)\b'
        facility_keywords = r'\b(hospital|clinic|phc|chc|dispensary|doctor|specialist|ambulance|nearest|near me)\b'

        has_scheme_kw = bool(re.search(scheme_keywords, lower_text))
        has_facility_kw = bool(re.search(facility_keywords, lower_text))

        if has_scheme_kw and not has_facility_kw:
            return IntentEnum.GOVT_SCHEMES_DISCOVERY, 0.95, "REGEX_RULE"
        elif has_facility_kw and not has_scheme_kw:
            return IntentEnum.FACILITY_DISCOVERY, 0.95, "REGEX_RULE"

        query_embedding = self._model.encode(text, convert_to_tensor=True)
        best_intent = IntentEnum.GENERAL_MEDICAL_QA
        max_score = 0.0

        for intent, centroid in self._centroid_embeddings.items():
            score = util.cos_sim(query_embedding, centroid).item()
            if score > max_score:
                max_score = score
                best_intent = intent

        if max_score < 0.40:
            best_intent = IntentEnum.GENERAL_MEDICAL_QA

        return best_intent, round(max_score, 4), "HYBRID_EMBEDDING"

intent_classifier_service = UserIntentClassifierService()
