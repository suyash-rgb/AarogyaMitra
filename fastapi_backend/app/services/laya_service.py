import re
import os
import hashlib
import logging
import numpy as np
from typing import Tuple, Dict, Any, Optional
import onnxruntime as ort
from transformers import AutoTokenizer

from app.schemas.user_intent_classifier import IntentEnum, ExtractedSlots
from app.services.cache_service import cache_service
from app.services.telemetry_service import telemetry_service
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

ID_TO_INTENT_MAP = {
    0: IntentEnum.EMERGENCY_CRITICAL,
    1: IntentEnum.FACILITY_LOCATOR,
    2: IntentEnum.GOVT_SCHEME_ELIGIBILITY,
    3: IntentEnum.MEDICINE_GENERIC_SEARCH,
    4: IntentEnum.OUT_OF_SCOPE_GENERAL,
    5: IntentEnum.SYMPTOM_TRIAGE_REMEDY
}

class LayaService:
    def __init__(self, model_dir: Optional[str] = None):
        if model_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            model_dir = os.path.join(base_dir, "models", "laya")
        
        self.model_dir = model_dir
        self.onnx_path = os.path.join(self.model_dir, "model_quantized.onnx")
        self._tokenizer = None
        self._session = None
        self._is_loaded = False
        
        self._load_laya_model()

    def _load_laya_model(self):
        try:
            if not os.path.exists(self.onnx_path):
                logger.error(f"Laya ONNX model file not found at {self.onnx_path}")
                return

            logger.info(f"Loading Fine-Tuned Laya ONNX Model from {self.onnx_path}...")
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self._session = ort.InferenceSession(self.onnx_path, providers=["CPUExecutionProvider"])
            self._is_loaded = True
            logger.info("Fine-Tuned Laya AI Classifier ONNX model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load Laya ONNX model: {e}", exc_info=True)
            self._is_loaded = False

    def extract_slots(self, text: str) -> ExtractedSlots:
        slots = ExtractedSlots()
        lower_text = f" {text.lower()} "

        pincode_match = re.search(r" [1-9][0-9]{5} ", text)
        if pincode_match:
            slots.pincode = pincode_match.group(0)

        for state in INDIAN_STATES:
            pattern = r" " + re.escape(state.lower()) + r" "
            if re.search(pattern, lower_text):
                if state.upper() in ["MP", "MADHYA PRADESH"]:
                    slots.state = "Madhya Pradesh"
                elif state.upper() in ["UP", "UTTAR PRADESH"]:
                    slots.state = "Uttar Pradesh"
                else:
                    slots.state = state
                break

        for key, val in SPECIALTIES_MAP.items():
            pattern = r" " + re.escape(key) + r" "
            if re.search(pattern, lower_text):
                slots.specialty = val
                break

        return slots

    def classify_intent(self, text: str, trace_id: Optional[str] = None) -> Tuple[IntentEnum, float, str]:
        meta = {"text_len": len(text), "snippet": text[:40]}
        
        with telemetry_service.span("laya_intent_classifier", trace_id=trace_id, meta=meta) as span:
            lower_text = text.lower().strip()

            query_hash = hashlib.sha256(lower_text.encode("utf-8")).hexdigest()
            cached_intent = cache_service.get(namespace="intent", key=query_hash)

            if cached_intent is not None and isinstance(cached_intent, dict):
                method_str = str(cached_intent.get("method", "LAYA_ONNX")) + "_CACHED"
                logger.info(f"Intent Cache HIT (2-Tier) for key: {query_hash[:20]}...")
                intent_enum = IntentEnum(cached_intent["intent"])
                score_val = float(cached_intent["score"])
                
                span.set_metric("intent", intent_enum.value)
                span.set_metric("confidence_score", score_val)
                span.set_metric("classification_method", method_str)
                span.set_metric("cache_hit", True)
                
                return intent_enum, score_val, method_str

            facility_regex = r" (hospital|clinic|phc|chc|dispensary|doctor|specialist|ambulance|nearest|near me) "

            if self._is_loaded and self._session and self._tokenizer:
                try:
                    inputs = self._tokenizer(text, return_tensors="np", truncation=True, max_length=512)
                    input_names = [i.name for i in self._session.get_inputs()]
                    ort_inputs = {k: v.astype(np.int64) for k, v in inputs.items() if k in input_names}
                    
                    outputs = self._session.run(None, ort_inputs)
                    logits = outputs[0][0]
                    
                    exp_logits = np.exp(logits - np.max(logits))
                    probs = exp_logits / np.sum(exp_logits)
                    
                    pred_id = int(np.argmax(probs))
                    max_score = float(round(probs[pred_id], 4))
                    best_intent = ID_TO_INTENT_MAP.get(pred_id, IntentEnum.OUT_OF_SCOPE_GENERAL)
                    method = "LAYA_ONNX_CLASSIFIER"

                    if max_score < 0.60 and re.search(facility_regex, lower_text):
                        best_intent = IntentEnum.FACILITY_LOCATOR
                        max_score = 0.90
                        method = "LAYA_HYBRID_REFINED"

                except Exception as e:
                    logger.error(f"Error executing Laya ONNX inference: {e}", exc_info=True)
                    best_intent, max_score, method = IntentEnum.SYMPTOM_TRIAGE_REMEDY, 0.5, "FALLBACK_DEFAULT"
            else:
                best_intent, max_score, method = IntentEnum.SYMPTOM_TRIAGE_REMEDY, 0.5, "FALLBACK_NO_MODEL"

            cache_service.set(
                namespace="intent",
                key=query_hash,
                value={"intent": best_intent.value, "score": max_score, "method": method},
                ttl=settings.VALKEY_INTENT_TTL_SECONDS
            )

            span.set_metric("intent", best_intent.value)
            span.set_metric("confidence_score", max_score)
            span.set_metric("classification_method", method)
            span.set_metric("cache_hit", False)

            return best_intent, max_score, method

laya_service = LayaService()
