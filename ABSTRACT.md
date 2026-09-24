# ArogyaMitra Project Abstract

**ArogyaMitra: An Offline-First, Multi-Lingual Generative AI Health Assistant for Rural India**

Healthcare accessibility in rural India faces severe bottlenecks due to language barriers, limited medical infrastructure, poor internet connectivity, and low digital literacy. **ArogyaMitra** bridges this critical gap by delivering an offline-first, voice-native, multi-lingual AI healthcare companion tailored for tier-3 towns and rural communities across 22 scheduled Indic languages.

Architected around edge computing principles, ArogyaMitra runs 100% locally on low-cost consumer hardware without requiring active cloud connections. The pipeline integrates a high-speed intent routing core powered by **Laya AI**, which dynamically classifies user queries into emergency red-flags, facility locations, government scheme eligibility (e.g., Ayushman Bharat), generic drug discovery, and symptom triage. For clinical advisory, ArogyaMitra utilizes a 4-bit quantized **Qwen2.5 7B LLM** paired with an **ICMR-guided Retrieval-Augmented Generation (RAG)** vector engine, ensuring evidence-based, medically safe health advice.

To dismantle literacy barriers, the platform features a zero-latency multi-lingual speech pipeline powered by C++ ONNX-accelerated **Meta MMS VITS** for speech synthesis and **CTranslate2 INT8** for real-time translation across 28 script/dialect variations. Additionally, ArogyaMitra incorporates an edge Vision pipeline (**Qwen VLM**) to parse doctor prescriptions and lab reports directly. By unifying local LLM intelligence, instant facility matching, and scheme eligibility verification, ArogyaMitra democratizes equitable, private, and life-saving healthcare access for 1.4 billion citizens.
