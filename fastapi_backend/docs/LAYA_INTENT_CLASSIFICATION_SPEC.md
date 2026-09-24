# Laya AI Intent Classification Specification & Architecture Schema

## Executive Summary
This document specifies the complete intent classification architecture for **Laya AI** within the **ArogyaMitra** healthcare ecosystem. 

By analyzing user queries, system capabilities, and the edge n8n workflow architecture, we define **6 mutually exclusive intent classes** for free-text processing. Attachment-based input (images/PDFs) is programmatically bypassed via MIME-type routing (`N2: MIME Switch`), eliminating unnecessary LLM/classifier overhead for visual documents.

---

## Architecture Flow Overview

```
                                [User Input Request]
                                         │
                                ┌────────┴────────┐
                                ▼                 ▼
                      (Attachment Image/PDF)   (Text/Voice Query)
                                │                 │
                    [N2: MIME Switch Bypass]   [N3-N6: Translation Pipeline]
                                │                 │
                       [Track B: Vision]  [N7: Laya AI Classifier]
                                                  │
 ┌───────────────────┬───────────────────┬────────┴──────────┬───────────────────┬───────────────────┐
 ▼                   ▼                   ▼                   ▼                   ▼                   ▼
[Class 1:           [Class 2:           [Class 3:           [Class 4:           [Class 5:           [Class 6:
 EMERGENCY_CRITICAL] FACILITY_LOCATOR]  GOVT_SCHEME]        MEDICINE_GENERIC]   SYMPTOM_TRIAGE]     OUT_OF_SCOPE]
 │                   │                   │                   │                   │                   │
 ▼                   ▼                   ▼                   ▼                   ▼                   ▼
[H1: Red-Flag Alert [H2: Spatial Postgres [H2: Structured Rel  [H4: In-Memory      [H3: In-Memory      [H5: Direct Light
 Ambulance/Trauma]   Facilities DB]      Schemes DB]         Vector DB (Chroma)]  ICMR RAG + Qwen]    Response Engine]
```

---

## 1. Intent Classes Specification

### Class 1: `EMERGENCY_CRITICAL`
* **Description**: Immediate life-threatening situations, acute trauma, severe symptoms, poisoning, or urgent 108 ambulance requests.
* **Execution Path**: Bypasses LLM generation to avoid dynamic delay. Directly invokes `H1: Emergency Red-Flag Dispatcher` (Location-based emergency contact dispatch + offline emergency protocol).
* **Target Handlers**: `H1: Emergency Red Flag Handler`
* **Dataset Scope & Examples**:
  * *"Call ambulance 108 immediately, my grandfather has severe chest pain and sweating!"*
  * *"Snake bit my leg in the farm, profuse bleeding and swelling!"*
  * *"Unconscious person after a road accident near Shivpuri highway."*
  * *"Pregnant woman experiencing sudden severe abdominal pain and heavy bleeding."*
* **Edge Cases Considered**:
  * Chemical/Pesticide ingestion (common in rural farms).
  * Heat stroke / severe dehydration during peak summer.
  * Pediatric choking or acute respiratory distress.

---

### Class 2: `FACILITY_LOCATOR`
* **Description**: Searching for physical healthcare infrastructure, operating hours, emergency departments, ICU beds, blood bank stock, or primary health centers (PHC/CHC).
* **Execution Path**: SQL/Spatial Distance Query against Postgres DB. Returns mapped facilities with distances, contact numbers, and direction guidance.
* **Target Handlers**: `H2: Postgres Spatial DB Query`
* **Dataset Scope & Examples**:
  * *"Where is the nearest Primary Health Center (PHC) near Shivpuri?"*
  * *"Find government hospitals in Bhopal with open ICU beds."*
  * *"Where can I find a blood bank with O negative blood available nearby?"*
  * *"Is there a free diagnostic lab open right now in Gwalior?"*
* **Edge Cases Considered**:
  * Queries specifying blood groups (*"Need A+ blood urgently"*).
  * Requests for free immunization clinics or child vaccination centers.
  * Queries asking for 24/7 emergency trauma centers.

---

### Class 3: `GOVT_SCHEME_ELIGIBILITY`
* **Description**: Queries regarding government healthcare financial schemes (Ayushman Bharat / PM-JAY, ABHA card, PMSSY, State health subsidies), eligibility verification, required documents, and benefit limits.
* **Execution Path**: Relational SQL lookup against structured scheme database. Returns clear eligibility matrices and application instructions.
* **Target Handlers**: `H2: Postgres Scheme Relational Database`
* **Dataset Scope & Examples**:
  * *"Am I eligible for 5 lakh free treatment under Ayushman Bharat scheme with BPL card?"*
  * *"How to create ABHA digital health ID using my Aadhaar card?"*
  * *"Is maternity treatment free under Janani Suraksha Yojana in MP?"*
  * *"What documents are required to register for PM-JAY health card?"*
* **Edge Cases Considered**:
  * BPL vs APL card eligibility threshold questions.
  * Coverage queries for pre-existing chronic conditions under PM-JAY.
  * Cashless hospital empanelment verification.

---

### Class 4: `MEDICINE_GENERIC_SEARCH`
* **Description**: Searching generic substitutes for branded medicines, Jan Aushadhi Kendra locations, medicine usage, dosage guidelines, side effects, and **plain-text prescription explanations** (when user types out medicine names instead of uploading an image).
* **Execution Path**: High-throughput In-Memory Vector DB (ChromaDB / Qdrant / ZVec) for instant drug index lookup and generic savings calculation.
* **Target Handlers**: `H4: In-Memory Fast Vector DB (ChromaDB/Qdrant)`
* **Dataset Scope & Examples**:
  * *"What is the cheap generic alternative for Paracetamol 650?"*
  * *"Doctor prescribed Pantoprazole 40mg and Amoxicillin 500mg, what are these for?"*
  * *"Where is the nearest Jan Aushadhi store to buy discounted medicines?"*
  * *"Can I take Metformin diabetes tablet on an empty stomach?"*
* **Edge Cases Considered**:
  * Plain text doctor notes (*"Doc wrote PCM and Azithro, how many times a day?"*).
  * Medication safety queries during pregnancy or breastfeeding.
  * Side-effect warnings and drug-drug interaction checks.

---

### Class 5: `SYMPTOM_TRIAGE_REMEDY`
* **Description**: Describing non-emergency medical symptoms, seeking primary healthcare advisory, ICMR-compliant home remedies, disease prevention, nutrition, and knowing when to consult a doctor.
* **Execution Path**: ICMR Vector RAG Retriever $\rightarrow$ Context Synthesizer $\rightarrow$ 4-bit Quantized Qwen2.5-7B Local LLM.
* **Target Handlers**: `H3: In-Memory ICMR RAG` $\rightarrow$ `C1 Context Synthesizer` $\rightarrow$ `N12: Qwen LLM`
* **Dataset Scope & Examples**:
  * *"My 5-year-old child has mild fever (100F) and runny nose since morning."*
  * *"What safe home remedy can I use for dry cough and sore throat?"*
  * *"I have joint pain and morning stiffness, could it be arthritis?"*
  * *"How can a diabetic patient manage blood sugar through rural Indian diet?"*
* **Edge Cases Considered**:
  * Seasonal endemic outbreaks (Dengue, Malaria, Chikungunya, Typhoid).
  * Maternal health & child vaccination schedule guidance.
  * Basic mental health check-ins and anxiety coping techniques.

---

### Class 6: `OUT_OF_SCOPE_GENERAL`
* **Description**: Conversational greetings, asking about ArogyaMitra capabilities, language switching requests, or non-medical off-topic queries.
* **Execution Path**: Direct light-response engine with zero LLM/RAG overhead.
* **Target Handlers**: `H5: Direct Core Light Engine`
* **Dataset Scope & Examples**:
  * *"Namaste, who are you and how can you help me?"*
  * *"How do I change the voice language to Marathi or Tamil?"*
  * *"Thank you so much for your assistance!"*
  * *"What is the weather forecast for Bhopal today?"* (Politely decline non-medical queries)
* **Edge Cases Considered**:
  * Multi-lingual greetings (*"Pranam"*, *"Vanakkam"*, *"Sat Sri Akal"*, *"Khamma Ghani"*).
  * Non-medical off-topic questions (weather, sports, politics) $\rightarrow$ polite medical redirection.

---

## 2. In-Memory Vector Storage Architecture (ChromaDB / Qdrant)

To guarantee sub-100ms response times and avoid slow database ingestion overhead:
1. **Drug Index & Generic Substitutes (`Class 4`)**: Ingested into **In-Memory ChromaDB / Qdrant / ZVec**. This enables instant fuzzy vector search for medicine names, dosages, and Jan Aushadhi alternatives.
2. **ICMR Medical Guidance (`Class 5`)**: Ingested into a lightweight local vector collection, enabling fast context retrieval for the Qwen LLM.

---

## 3. Kaggle Fine-Tuning Strategy for Laya AI

* **Target Model**: Lightweight transformer (e.g. `DeBERTa-v3-small` / `BERT-Tiny` or fine-tuned `Llama-3.2-1B-Instruct`).
* **Dataset Size**: **~150 to 200 synthetic query pairs per class** (Total **~1,000–1,200 dataset pairs**).
* **Multi-Lingual Coverage**: English, Hindi (Devanagari), and Hinglish (Latin script) to ensure robust classification across code-switched queries.
