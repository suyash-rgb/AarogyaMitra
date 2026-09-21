import re
import hashlib
import logging
import torch
from typing import Tuple, Dict, Any
from sentence_transformers import SentenceTransformer, util
from app.schemas.user_intent_classifier import IntentEnum, ExtractedSlots
from app.services.cache_service import cache_service
from app.core.config import settings

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

        pincode_match = re.search(r'[1-9][0-9]{5}', text)
        if pincode_match:
            slots.pincode = pincode_match.group(0)

        for state in INDIAN_STATES:
            pattern = r'' + re.escape(state.lower()) + r''
            if re.search(pattern, lower_text):
                if state.upper() in ["MP", "MADHYA PRADESH"]:
                    slots.state = "Madhya Pradesh"
                elif state.upper() in ["UP", "UTTAR PRADESH"]:
                    slots.state = "Uttar Pradesh"
                else:
                    slots.state = state
                break

        for key, val in SPECIALTIES_MAP.items():
            if re.search(r'' + re.escape(key) + r'', lower_text):
                slots.specialty = val
                break

        return slots

    def classify_intent(self, text: str) -> Tuple[IntentEnum, float, str]:
        lower_text = text.lower().strip()

        # Check 2-Tier Cache HIT
        query_hash = hashlib.sha256(lower_text.encode("utf-8")).hexdigest()
        cached_intent = cache_service.get(namespace="intent", key=query_hash)

        if cached_intent is not None and isinstance(cached_intent, dict):
            logger.info(f"Intent Cache HIT (2-Tier) for key: {query_hash[:20]}...")
            return (
                IntentEnum(cached_intent["intent"]),
                float(cached_intent["score"]),
                f"{cached_intent['method']}_CACHED"
            )

        if re.match(r'^(hi|hello|hey|namaste|good morning|good evening|thanks|thank you)[!\.]?$', lower_text):
            best_intent, max_score, method = IntentEnum.GREETING_CONVERSATIONAL, 1.0, "REGEX_FAST_PATH"
        else:
            scheme_keywords = r'(scheme|yojana|bima|subsidy|govt benefit|financial support|ayushman|myscheme)'
            facility_keywords = r'(hospital|clinic|phc|chc|dispensary|doctor|specialist|ambulance|nearest|near me)'

            has_scheme_kw = bool(re.search(scheme_keywords, lower_text))
            has_facility_kw = bool(re.search(facility_keywords, lower_text))

            if has_scheme_kw and not has_facility_kw:
                best_intent, max_score, method = IntentEnum.GOVT_SCHEMES_DISCOVERY, 0.95, "REGEX_RULE"
            elif has_facility_kw and not has_scheme_kw:
                best_intent, max_score, method = IntentEnum.FACILITY_DISCOVERY, 0.95, "REGEX_RULE"
            else:
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

                max_score = round(max_score, 4)
                method = "HYBRID_EMBEDDING"

        # Cache SET
        cache_service.set(
            namespace="intent",
            key=query_hash,
            value={"intent": best_intent.value, "score": max_score, "method": method},
            ttl=settings.VALKEY_INTENT_TTL_SECONDS
        )

        return best_intent, max_score, method

intent_classifier_service = UserIntentClassifierService()
