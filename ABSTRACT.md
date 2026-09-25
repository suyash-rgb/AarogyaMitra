# ArogyaMitra: Project Abstract & Strategic Rationale

### Executive Abstract
Healthcare accessibility in rural India faces severe bottlenecks due to language barriers, specialist shortfalls at CHCs, low digital literacy, and internet instability. **ArogyaMitra** bridges this gap by delivering an offline-first, voice-native, multi-lingual AI healthcare companion tailored for tier-2/3 towns and rural communities across 22 scheduled Indic languages.

Architected around edge-computing principles, ArogyaMitra runs 100% locally on low-cost commodity hardware (<=2.8 GB RAM footprint) with zero cloud GPU dependency. The pipeline integrates a high-speed intent routing core powered by **Laya AI**, classifying queries across emergency red-flags, facility locations, government scheme eligibility, generic drugs, and symptom triage. For clinical advisory, ArogyaMitra pairs a 4-bit quantized **Qwen 3.5 2B LLM (GGUF Q4_K_M)** with an **ICMR-guided Retrieval-Augmented Generation (Qdrant)** vector engine. Zero-latency translation across 28 script variations is powered by **CTranslate2 INT8** and **Meta MMS VITS** voice synthesis, complemented by an edge Vision pipeline (**Qwen VLM**) for doctor prescription OCR.

### Strategic Rationale: Why a WhatsApp-Native Interface?
Websites introduce high friction—requiring app downloads, complex UI navigation, and high digital literacy. In contrast, WhatsApp serves 425M+ rural Indian users with zero learning curve. Chatbots served as the frontier soldiers of the AI revolution because messaging is universal, conversational, and instant. Delivering clinical navigation directly via WhatsApp Business API / PWA webhooks eliminates accessibility barriers for non-tech-savvy patients.

### Compliance & Scalability
ArogyaMitra natively aligns with national health frameworks including **ABDM (Ayushman Bharat Digital Mission)**, **UHI (Unified Health Interface)**, and **NHA guidelines**, enabling seamless Primary Health Centre (PHC) queueing. By combining strict safety short-circuits (108 emergency dispatch) with an affordable /month VM deployment footprint, ArogyaMitra delivers an ultra-scalable, compliant, and life-saving healthcare navigation infrastructure for 1.4 billion citizens.
