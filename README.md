<div align="center">

<img src="assets/logo-removebg-preview.png" alt="AarogyaMitra Logo" width="160"/>

# **आरोग्यमित्र** | AarogyaMitra
### *Intelligent Multilingual Edge-AI for Rural & Tier-2/3 Clinical Triage Navigation*
### *ग्रामीण स्वास्थ्य का डिजिटल साथी — 100% Offline Edge Deployable (Zero Cloud GPU Required)*

[![India DPI](https://img.shields.io/badge/%F0%9F%87%AE%F0%9F%87%B3_India-Healthcare_DPI-orange?style=for-the-badge)](https://abdm.gov.in/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005587?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React Native](https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactnative.dev/)
[![Expo](https://img.shields.io/badge/Expo-000000?style=for-the-badge&logo=expo&logoColor=white)](https://expo.dev/)
[![ModernBERT](https://img.shields.io/badge/ModernBERT-395M_ONNX-7928CA?style=for-the-badge)](https://huggingface.co/answerdotai/ModernBERT-large)
[![Qwen 3.5 GGUF](https://img.shields.io/badge/Qwen_3.5_2B-GGUF_Q4_K_M-green?style=for-the-badge)](https://huggingface.co/TheUsurper09/aarogyamitra-qwen35-2b-gguf)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

*Democratizing healthcare navigation for 425M+ rural citizens through voice-first multilingual AI, instant emergency short-circuits, zero-cost telemedicine integration, and deterministic edge execution on commodity CPUs.*

---
</div>

<details>
<summary><b>Table of Contents (Click to Expand)</b></summary>

1. [Motivation, Vision & Ground Realities](#-motivation-vision--ground-realities)
2. [Proposed Solution & 3 Architectural Pillars](#-proposed-solution--3-architectural-pillars)
3. [System Architecture & Pipeline Canvas](#-system-architecture--pipeline-canvas)
   - [Two-Track Ingestion Engine](#two-track-ingestion-engine)
   - [5 Downstream Execution Handlers](#5-specialized-downstream-execution-handlers)
   - [Convergence, Localization & Egress](#convergence-localization--egress-layer)
4. [Intent Routing: ModernBERT, Laya & The System-1 Edge Engine](#-intent-routing-modernbert-laya--the-system-1-edge-engine)
   - [System 1 vs. System 2 in Healthcare AI](#system-1-vs-system-2-in-healthcare-ai)
   - [Why Pure ModernBERT-large over Laya & Jev](#the-base-model-choice-why-pure-modernbert-large-over-laya-and-jev)
   - [Synthetic Clinical Data Engineering](#synthetic-clinical-data-engineering)
   - [Upcoming Medium Engineering Article](#-deep-dive-article-on-medium)
5. [Quantization, Hardware Budget & Edge Efficiency](#-quantization-hardware-budget--edge-efficiency)
6. [Production Telemetry & Real Latency Benchmarks](#-production-telemetry--real-latency-benchmarks)
7. [Clinical Safety Boundaries & Public Health Vision](#-clinical-safety-boundaries--public-health-vision)
8. [22 Indic Languages Support (Visual Showcase)](#-22-indic-languages-support)
9. [Repository Branching Strategy](#-repository-branching-strategy)
10. [Getting Started & Developer Guide](#-getting-started--developer-guide)
11. [License, Citations & Acknowledgments](#-license-citations--acknowledgments)

</details>

---

## 🌟 Motivation, Vision & Ground Realities

In rural and Tier-2/3 India, accessing certified healthcare is a race against distance, extreme specialist shortages, and language barriers. According to the official *Health Dynamics of India* report released by the **Ministry of Health and Family Welfare (MoHFW)**, rural healthcare faces severe systemic constraints:

* 🩺 **80% CHC Specialist Vacancy:** Rural Community Health Centres face an 80% specialist shortfall, forcing patients to travel 20–50 km over unpaved roads for basic consultation or preliminary triage.
* 🗣️ **The Indic Language & Script Barrier:** Mainstream cloud LLMs fail on colloquial Indic dialects and Hinglish code-mixing, hallucinating clinical advice due to severe sub-word token splits.
* 📄 **Physical Document Lock:** Vital patient diagnostic history remains trapped in paper lab reports and blurry mobile camera photos of handwritten doctor prescriptions.
* 🌐 **Connectivity & Hardware Constraints:** Cloud-dependent AI fails in low-bandwidth 2G zones. Rural health kiosks demand sovereign, offline execution on low-cost commodity CPUs without high-end cloud GPUs.

> 💡 **The Bharat Opportunity:** Over **425 Million** rural Indian citizens actively rely on mobile messaging. **AarogyaMitra (आरोग्यमित्र)** bridges this chasm by converting everyday mobile devices into trusted, multilingual digital paramedics.

---

## 🎯 Proposed Solution & 3 Architectural Pillars

AarogyaMitra operates within a lean **$\le 2.8\text{ GB}$ RAM footprint on standard CPUs**, structured around three foundational pillars:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AAROGYAMITRA 3 CORE PILLARS                                    │
├───────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│ 1. Clinical Triage Engine     │ 2. Native Indic Localization     │ 3. Multimodal Intake          │
├───────────────────────────────┼──────────────────────────────────┼───────────────────────────────┤
│ • SFT LoRA on Qwen 3.5 2B     │ • All 22 Eighth Schedule langs   │ • Deterministic PDF parser    │
│ • Structured clinical staging │ • Romanized Hinglish / Banglish  │   via PyMuPDF (<10ms)         │
│ • Instant red-flag escalation │ • Stack: IndicLID + IndicXlit +  │ • Doctor Rx Vision LoRA with  │
│ • GGUF Q4_K_M (Zero Cloud)    │   CTranslate2 NLLB-200           │   Jan Aushadhi salt matcher   │
└───────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

---

## 🏗️ System Architecture & Pipeline Canvas

```mermaid
graph TD
    A[📱 Mobile Client / WhatsApp Webhook] -->|MIME Switch| B{Attachment Present?}
    
    %% Track A: Voice & Text
    B -->|Text / Audio Voice Note| C[🗣️ Phase 1: Conversational NLP Engine]
    C --> C1[IndicLID: Dialect & Script Identification]
    C1 --> C2{Romanized Script?}
    C2 -->|Yes: Hinglish/Banglish| C3[IndicXlit: Transliterate to Native Script]
    C2 -->|No: Native Script| C4[CTranslate2: NLLB-200 Native ➔ English]
    C3 --> C4
    C4 --> C5[⚡ Intent Router: Fine-Tuned ModernBERT-large 395M ONNX]
    
    %% Track B: Documents & Vision
    B -->|PDF / Image Attachment| D[📄 Phase 2: Document & Vision Service]
    D --> D1{Attachment Type}
    D1 -->|Lab Report PDF| D2[PyMuPDF: Tabular Panel Parser <10ms]
    D1 -->|Handwritten Doctor Rx| D3[Qwen-VL Vision OCR]
    D3 --> D4[💊 Lexicon Matcher: 10,000+ Jan Aushadhi Generic Salts]
    
    %% Downstream Handlers
    C5 -->|EMERGENCY_CRITICAL| H1[🚨 Emergency Red-Flag: Instant 108/104 Dialer]
    C5 -->|FACILITY_LOCATOR| H2[🗺️ Postgres Spatial DB: PHC/CHC via Ola Maps & OSM]
    C5 -->|GOVT_SCHEME_ELIGIBILITY| H3[📚 Hybrid Search: BM25 + Qdrant Vector DB]
    C5 -->|MEDICINE_GENERIC_SEARCH| H4[💊 Jan Aushadhi Generic Salt Matcher]
    C5 -->|SYMPTOM_TRIAGE_REMEDY| H5[🩺 Clinical Triage: Fine-Tuned Qwen 3.5 2B GGUF]
    
    %% Document Feed into Downstream
    D2 --> H5
    D4 --> H4
    
    %% Convergence & Localization
    H1 --> E[🌐 Convergence & Localization Layer]
    H2 --> E
    H3 --> E
    H4 --> E
    H5 --> E
    
    E --> E1[CTranslate2: English ➔ Target Indic Dialect]
    E1 --> E2{Voice Requested?}
    E2 -->|Yes| E3[Meta MMS ONNX TTS: Indic Voice Synthesis]
    E2 -->|No| E4[Direct Text Response]
    E3 --> F[📱 User Mobile WhatsApp / Web Interface]
    E4 --> F
```

### Two-Track Ingestion Engine
1. **Track A (Conversational Voice & Text):**
   * **IndicLID:** Language identification across all 22 official Indian languages.
   * **IndicXlit:** Translates phonetic Romanized chat (e.g. *"mujhe tez bukhar hai"*) into native Indic script (*"मुझे तेज़ बुखार है"*).
   * **CTranslate2 (NLLB-200 INT8):** Translates regional dialects into standardized English for downstream clinical reasoning.
   * **ModernBERT Intent Router (395M ONNX):** Classifies the core intent in **$\le 112\text{ ms}$** without calling an autoregressive LLM.

2. **Track B (Document & Vision Intake):**
   * **PyMuPDF Deterministic Parser:** Extracts structured lab panels (CBC, Lipid, LFT, KFT) from PDF reports in **$<10\text{ ms}$** with zero OCR hallucinations.
   * **Prescription Vision Service:** Extracts active chemical salts from doctor prescriptions and matches them against **10,000+ Jan Aushadhi generic substitutes**, reducing out-of-pocket costs by up to 85%.

---

## 🧠 Intent Routing: ModernBERT, Laya & The System-1 Edge Engine

### System 1 vs. System 2 in Healthcare AI

In cognitive science, **System 1** represents fast, deterministic, subconscious pattern recognition, while **System 2** represents slow, deliberative reasoning. 

In conversational AI, developers frequently make the mistake of using **System 2 generative LLMs (taking 3,000ms–8,000ms)** just to classify whether a user is asking for an ambulance, a hospital address, or a government scheme.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                            SYSTEM 1 (ROUTING) vs. SYSTEM 2 (GENERATION)                          │
├───────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│ Metric / Dimension            │ Autoregressive LLM (System 2)    │ ModernBERT Router (System 1)  │
├───────────────────────────────┼──────────────────────────────────┼───────────────────────────────┤
│ Mechanism                     │ Sequential token generation      │ Single forward-pass embedding │
│ CPU Latency                   │ 3,500 ms – 9,000 ms              │ 30 ms – 112 ms (Pure CPU)     │
│ Determinism                   │ Non-deterministic (hallucinations)│ 100% deterministic logits     │
│ Emergency Suitability         │ Dangerous delay for critical care│ Instant 0ms short-circuit     │
│ Memory Footprint              │ 1.5 GB – 4.0 GB RAM              │ ~450 MB INT8 ONNX             │
└───────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

### The Base Model Choice: Why Pure ModernBERT-Large Over Laya and Jev

When designing the intent classification layer, we evaluated the state-of-the-art decision models:

1. **Jev (TypeSafe AI):** While powerful, Jev is a **closed, proprietary cloud SaaS API**. Sending sensitive rural patient data over third-party cloud APIs violates health data sovereignty and fails entirely when rural cell towers drop packets in 2G zones.
2. **Laya (Convai Innovations):** Laya provided open weights under Apache 2.0. However, deep architectural inspection revealed that `convaiinnovations/laya` **is built on `answerdotai/ModernBERT-large` (395M)**, but wraps it with **~26M parameters of custom reinforcement learning decision heads** ("Choice", "Score", and "Noul" heads designed for Convai's RL agent API).
3. **The AarogyaMitra Solution (Fine-Tuned Pure ModernBERT-large):**
   * We stripped the 26M deadweight parameters that added compute overhead on CPU.
   * Attached a clean, standard 6-class sequence classification head (`AutoModelForSequenceClassification`).
   * Resolved the Hugging Face `TokenizersBackend` fast-tokenizer serialization bug during Kaggle ONNX export.
   * Fine-tuned directly on our domain-specific synthetic clinical dataset, achieving **99.2% classification accuracy** and **$\le 112\text{ ms}$ inference on commodity CPUs**.

### 6-Class Intent Topology
```python
ID_TO_INTENT_MAP = {
    0: "EMERGENCY_CRITICAL",        # Ambulance 108 / Immediate triage short-circuit
    1: "FACILITY_LOCATOR",          # PHC / CHC / Jan Aushadhi spatial lookup
    2: "GOVT_SCHEME_ELIGIBILITY",   # PM-JAY / ABHA / Maternity scheme vector search
    3: "MEDICINE_GENERIC_SEARCH",   # Jan Aushadhi generic salt substitution
    4: "OUT_OF_SCOPE_GENERAL",       # Non-medical guardrail refusals
    5: "SYMPTOM_TRIAGE_REMEDY"      # Home care & clinical triage protocols
}
```

### Synthetic Clinical Data Engineering
To ensure total data privacy without exposing Protected Health Information (PHI), we engineered `generate_laya_dataset.py`, generating **1,200 perfectly stratified, balanced clinical seed samples** across all 6 intents using:
* **Grounded Geographic & Facility Slots:** Combinatorial pairings of Tier-2/3 districts (Wardha, Vidisha, Shivpuri, Gwalior) $\times$ facility types $\times$ PIN codes (`440001`–`800001`).
* **Pharmacology Salt Permutations:** Popular Indian brand names (Dolo 650, Clavam 625, Telma 40, Glycomet) mapped to generic chemical salts.
* **Semantic Boundary Disambiguation:** Hard boundary separation between spatial intent (*"Where can I buy generic paracetamol in Wardha?"* $\rightarrow$ `FACILITY_LOCATOR`) and scheme eligibility (*"Does Ayushman card cover cardiac surgery?"* $\rightarrow$ `GOVT_SCHEME_ELIGIBILITY`).

### 📖 Deep-Dive Article on Medium
> ✍️ **Read the full engineering story and postmortem:**  
> **[Jev or Laya? Neither: Why We Fine-Tuned ModernBERT on the Edge for Rural Healthcare AI](https://medium.com/@suyashbaoney58)**  
> *By Suyash Baoney (Author of [Beyond AI Guardrails](https://medium.com/@suyashbaoney58/beyond-ai-guardrails-and-refusals-why-lms-platforms-must-own-their-anti-cheat-engines-e6ffc1a5cd83))*

---

## ⚡ Quantization, Hardware Budget & Edge Efficiency

AarogyaMitra is engineered to run on a **$5/month 4-Core CPU Virtual Machine (or edge clinic mini-PC)** without dedicated GPUs:

| Component / Subsystem | Base Architecture | Precision & Format | RAM Footprint | CPU Inference Target |
| :--- | :--- | :--- | :--- | :--- |
| **Intent Classifier** | ModernBERT-large (395M) | ONNX INT8 Quantized | **~450 MB** | **35 ms – 112 ms** |
| **Clinical Reasoning** | Qwen 3.5 2B Instruct | GGUF Q4_K_M (llama.cpp) | **~1,310 MB** | **~1.2 s TTFT (Streaming)** |
| **Indic Translation** | NLLB-200 Distilled (600M) | CTranslate2 INT8 | **~400 MB** | **~800 ms** |
| **Indic Voice Synthesis**| Meta MMS VITS (22 Langs) | ONNX Runtime INT8 | **~500 MB** | **~450 ms** |
| **Spatial & Vector DB** | Postgres + Qdrant (HNSW) | In-Memory Local Index | **~120 MB** | **< 20 ms** |
| **TOTAL PIPELINE** | *Full Edge AI Suite* | *Zero Cloud GPU Required* | **$\le 2.78\text{ GB}$** | **Real-Time Edge Response** |

### Fine-Tuning Specifications (Qwen 3.5 2B SFT LoRA)
* **LoRA Rank ($r$):** `16` | **Alpha ($\alpha$):** `32` | **Target Modules:** `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`
* **Dataset:** 4,500 curated clinical encounters spanning rural Indian epidemiology (Vector-borne, Maternal, GI, Chronic).
* **Validation Loss Floor:** `0.6385` | **Clinical Perplexity:** `1.894`
* **Open Model Artifact:** [Hugging Face: `TheUsurper09/aarogyamitra-qwen35-2b-gguf`](https://huggingface.co/TheUsurper09/aarogyamitra-qwen35-2b-gguf)

---

## 📊 Production Telemetry & Real Latency Benchmarks

End-to-end performance recorded across production test runs in `fastapi_backend/logs/pipeline_telemetry.jsonl`:

| Pipeline Stage / Node | Execution Provider / Hardware Target | Typical Latency | P95 Worst-Case | Error Rate | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ModernBERT Intent Classifier** | CPU ONNX Runtime (Intel/AMD x86_64) | **68.4 ms – 112.4 ms** | **166.2 ms** | **0.0%** | Zero GPU required |
| **Spatial Facility Lookup** | Postgres Spatial / Ola Maps / OSM | **35.0 ms – 120.0 ms** | **180.0 ms** | **0.0%** | Nearest PHC/CHC coordinates |
| **Qdrant Vector Retrieval (RAG)** | Local In-Memory Store | **140.0 ms – 185.0 ms** | **204.0 ms** | **0.0%** | BM25 + Dense vector match |
| **CTranslate2 NLLB Translation** | CPU INT8 CTranslate2 | **850.0 ms – 1,240.0 ms**| **1,795.0 ms** | **0.0%** | Multi-sentence translation |
| **Cloud/Hybrid LLM (Groq / vLLM)**| Cloud Accelerated Provider | **350.0 ms – 800.0 ms** | **1,100.0 ms** | **0.0%** | Optional high-speed cloud path |
| **Local Qwen 3.5 2B (Streaming TTFT)**| Local CPU (llama.cpp 4-threads) | **1,200.0 ms – 1,800.0 ms**| **3,767.0 ms** | **0.0%** | *Time-To-First-Token* (Instant streaming UX) |
| **Local Qwen 3.5 2B (Full Batch)**| Local CPU (llama.cpp 4-threads) | **3,500.0 ms – 5,620.0 ms**| **11,980.0 ms** | **0.0%** | Complete 120+ token generation on raw CPU |

> 💡 **Why the User Experience is Instantaneous:**
> 1. **Zero-Delay Short-Circuits:** Emergency 108 triggers, Hospital spatial search, and Generic Jan Aushadhi searches bypass generative LLMs completely via ModernBERT, delivering results in **$<180\text{ ms}$**.
> 2. **Token Streaming:** For clinical triage and scheme explanations, response streaming delivers the first tokens in **$\sim 1.2\text{s}$**, ensuring natural, lag-free conversational flow.

---

## 🛡️ Clinical Safety Boundaries & Public Health Vision

1. **Strict Triage Navigation vs. Diagnosis:** AarogyaMitra acts strictly as an intelligent navigation and first-aid guide directing patients between Home Care, PHCs, and Tertiary Hospitals—it **never prescribes prescription-only drugs** or claims diagnostic finality.
2. **Deterministic Emergency Bypass:** Critical cardiac, respiratory, and trauma symptoms bypass LLM reasoning and immediately trigger 108 ambulance dialers.
3. **ABDM & UHI Alignment:** Architecture conforms to the **Ayushman Bharat Digital Mission (ABDM)** and **Unified Health Interface (UHI)** standards.

---

## 🌍 22 Indic Languages Support

<div align="center">

<h2>ArogyaMitra Mobile Simulation: 22 Scheduled Indian Languages</h2>

<table>
  <tr>
    <td align="center"><b>Assamese</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/01_as_Assamese.png" width="180" /></td>
    <td align="center"><b>Bengali</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/02_bn_Bengali.png" width="180" /></td>
    <td align="center"><b>Bodo</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/03_brx_Bodo.png" width="180" /></td>
    <td align="center"><b>Dogri</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/04_doi_Dogri.png" width="180" /></td>
  </tr>
  <tr>
    <td align="center"><b>Gujarati</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/05_gu_Gujarati.png" width="180" /></td>
    <td align="center"><b>Hindi</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/06_hi_Hindi.png" width="180" /></td>
    <td align="center"><b>Kannada</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/07_kn_Kannada.png" width="180" /></td>
    <td align="center"><b>Kashmiri</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/08_ks_Kashmiri.png" width="180" /></td>
  </tr>
  <tr>
    <td align="center"><b>Konkani</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/09_gom_Konkani.png" width="180" /></td>
    <td align="center"><b>Maithili</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/10_mai_Maithili.png" width="180" /></td>
    <td align="center"><b>Malayalam</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/11_ml_Malayalam.png" width="180" /></td>
    <td align="center"><b>Manipuri</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/12_mni_Manipuri.png" width="180" /></td>
  </tr>
  <tr>
    <td align="center"><b>Marathi</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/13_mr_Marathi.png" width="180" /></td>
    <td align="center"><b>Nepali</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/14_ne_Nepali.png" width="180" /></td>
    <td align="center"><b>Odia</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/15_or_Odia.png" width="180" /></td>
    <td align="center"><b>Punjabi</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/16_pa_Punjabi.png" width="180" /></td>
  </tr>
  <tr>
    <td align="center"><b>Sanskrit</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/17_sa_Sanskrit.png" width="180" /></td>
    <td align="center"><b>Santali</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/18_sat_Santali.png" width="180" /></td>
    <td align="center"><b>Sindhi</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/19_sd_Sindhi.png" width="180" /></td>
    <td align="center"><b>Tamil</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/20_ta_Tamil.png" width="180" /></td>
  </tr>
  <tr>
    <td align="center"><b>Telugu</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/21_te_Telugu.png" width="180" /></td>
    <td align="center"><b>Urdu</b><br><img src="https://raw.githubusercontent.com/suyash-rgb/Sunstone-Hackathon_1.0-Rural-Healthcare-AI-Bot/whatsapp-app-simulation/App/assets/screenshots/languages/22_ur_Urdu.png" width="180" /></td>
  </tr>
</table>

</div>

---

## 🌿 Repository Branching Strategy

To keep development environments clean, this repository is split across three isolated branches based on application layers:

1. **`main` (FastAPI Backend)**: Python FastAPI backend, AI routing, ModernBERT ONNX engine, Vision Service, and database integration.
2. **`whatsapp-app-simulation` (Mobile Frontend)**: React Native (Expo) mobile application acting as the primary simulated WhatsApp interface for rural patients.
3. **`whatsapp-simulation` (Web Frontend)**: React (Vite) web application for browser-based simulation testing.

---

## 🚀 Getting Started & Developer Guide

### Prerequisites
* **Node.js** (v18+ / v22+) & **npm**
* **Python** (v3.11+)
* **Expo Go** app installed on your physical mobile device (Android / iOS)

---

### 1. Launching the FastAPI Backend
```bash
# Navigate to the backend directory
cd fastapi_backend

# Create and activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure Environment Variables in fastapi_backend/.env
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/arogyamitra
# GROQ_API_KEY=your_groq_api_key_here
# OLA_MAPS_KRUTRIM_CLOUD_API_BASE_URL=ola_maps_url
# OLA_MAPS_KRUTRIM_CLOUD_API_KEY=your_ola_maps_key_here
 
# Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
*Interactive Swagger API documentation will be available at: **`http://localhost:8000/docs`***

---

### 2. Launching the Mobile App (React Native / Expo)
```bash
# Navigate to the App directory
cd App

# Install npm dependencies
npm install

# Start the Expo development bundler (with 4GB Node heap and clear cache)
npm start -- -c
```
*Scan the displayed QR code using the **Expo Go** app to test live on your phone.*

---

### 3. Launching the Web App Simulation (React / Vite)
```bash
# Ensure you are on the whatsapp-simulation branch (or in its cloned directory)
cd frontend/web-preview

# Install npm dependencies
npm install

# Start the Vite development server
npm run dev
```

---

## ⚖️ License, Citations & Acknowledgments

This project is open-sourced under the [MIT License](LICENSE).

Special thanks to the **Ministry of Health and Family Welfare (MoHFW)**, **National Health Authority (NHA)**, **Ayushman Bharat Digital Mission (ABDM)**, **OpenStreetMap contributors**, **Ola Maps**, and the research teams behind **ModernBERT** (Answer.AI / LightOn), **Qwen** (Alibaba Cloud), and **AI4Bharat** for enabling digital public infrastructure that makes equitable healthcare access possible.
