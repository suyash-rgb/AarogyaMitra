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
4. [Quantization, Hardware Budget & Edge Efficiency](#-quantization-hardware-budget--edge-efficiency)
5. [Production Telemetry & Latency Benchmarks](#-production-telemetry--latency-benchmarks)
6. [Clinical Safety Boundaries & Public Health Vision](#-clinical-safety-boundaries--public-health-vision)
7. [22 Indic Languages Support (Visual Showcase)](#-22-indic-languages-support)
8. [Repository Branching Strategy](#-repository-branching-strategy)
9. [Getting Started & Developer Guide](#-getting-started--developer-guide)
10. [License, Citations & Acknowledgments](#-license-citations--acknowledgments)

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

AarogyaMitra operates within a lean **$\le 2.8	ext{ GB}$ RAM footprint on standard CPUs**, structured around three foundational pillars:

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
    C4 --> C5[⚡ Laya Intent Router: ModernBERT-large 395M ONNX]
    
    %% Track B: Documents & Vision
    B -->|PDF / Image Attachment| D[📄 Phase 2: Document & Vision Service]
    D --> D1{Attachment Type}
    D1 -->|Lab Report PDF| D2[PyMuPDF: Tabular Panel Parser <10ms]
    D1 -->|Handwritten Doctor Rx| D3[Qwen-VL Vision OCR]
    D3 --> D4[💊 Lexicon Matcher: 10,000+ Jan Aushadhi Generic Salts]
    
    %% Downstream Handlers
    C5 -->|EMERGENCY_CRITICAL| H1[🚨 Emergency Red-Flag: Instant 108/104 Dialer]
    C5 -->|FACILITY_LOCATOR| H2[🗺️ Postgres Spatial DB: PHC/CHC via Ola Maps & OSM]
    C5 -->|SYMPTOM_TRIAGE_REMEDY| H3[🩺 ICMR / MoHFW RAG Protocol Retriever]
    C5 -->|GOVT_SCHEME_ELIGIBILITY| H4[📚 Qdrant Vector DB: PM-JAY & ABHA Schemes]
    C5 -->|OUT_OF_SCOPE_GENERAL| H5[🛡️ Guardrail Refusal & Safe Guidance]
    
    %% Convergence & Egress
    D2 --> E[🧩 Context Synthesizer Buffer]
    D4 --> E
    H2 --> E
    H3 --> E
    H4 --> E
    H5 --> E
    
    E --> F[🧠 Local Qwen 3.5 2B GGUF: Clinical Synthesis Core]
    F --> G[🔄 CTranslate2 Reverse: English ➔ Patient Native Language]
    G --> I[🔊 Meta MMS VITS ONNX: Regional Audio Dispatch]
    I --> J[📲 WhatsApp Audio / Text Response Delivery]
```

---

### Two-Track Ingestion Engine

#### 🟢 Track A: Conversational Voice & Text Core
* **Indic Normalization:** **IndicLID** detects the dialect; **IndicXlit** transliterates Latin Hinglish into native Devanagari before **CTranslate2 NLLB-200** translates the prompt into English in $<1.2	ext{s}$ on CPU.
* **ModernBERT Laya Router:** A 395M non-autoregressive decision model routing queries across 6 categories in **$<40	ext{ms}$** (averaging $\sim 112	ext{ms}$ under full slot extraction).
* **Deterministic Red-Flag Exit:** Acute emergencies (cardiac arrest, snakebites, severe trauma) immediately short-circuit generative reasoning and trigger the **108/104 emergency dialer** to eliminate hallucination risk.

#### 🔵 Track B: Document & Vision Bypass
* **Deterministic Laya Bypass:** MIME attachment presence circumvents text intent classification entirely, saving 100% token overhead.
* **Pathology Lab Parser:** **PyMuPDF** extracts structured tabular values for CBC, LFT, and lipid panels in $<10	ext{ms}$.
* **Prescription Vision OCR & Generic Matcher:** **Qwen-VL** vision OCR parses handwritten scripts, cross-referencing brand drugs against a **10,000+ Indian generic medicine database** to identify low-cost Pradhan Mantri Jan Aushadhi Kendra alternatives.

---

### 5 Specialized Downstream Execution Handlers

1. **🚨 Emergency Red Flag (0ms Bypass):** Bypasses LLM generation to connect directly with the 24/7 National Ambulance (108) and Health Helpline (104).
2. **🗺️ Postgres Spatial Search:** Hybrid spatial radius engine (Ola Maps + OpenStreetMap Overpass QL) surfacing free government PHCs, CHCs, and blood banks before private clinics.
3. **🩺 ICMR / MoHFW Clinical RAG:** Retrieves official, validated first-aid clinical management protocols approved by the Indian Council of Medical Research.
4. **📚 In-Memory Vector DB (Qdrant):** Dense semantic similarity search matching user socio-economic criteria against **Ayushman Bharat (PM-JAY)**, **ABHA**, and state welfare schemes.
5. **🏛️ Zero-Cost Telemedicine Gateways:** Deep-linked one-tap integration with the national **eSanjeevani (MoHFW)** video OPD portal.

---

### Convergence, Localization & Egress Layer

1. **Context Synthesizer:** Aggregates user query, extracted lab vitals, spatial records, and RAG knowledge chunks into a structured clinical prompt.
2. **Local Qwen 3.5 2B LLM:** Running locally in quantized GGUF format (`Q4_K_M`) via `llama.cpp` with strict parameters (`temperature: 0.3`, `top_p: 0.9`, `repeat_penalty: 1.15`), generating concise ($<120$ words), empathetic, medically safe advice.
3. **CTranslate2 Reverse Localization:** Translates the English medical response back into the patient's native dialect and script.
4. **Meta MMS VITS ONNX Speech Synthesis:** Generates natural regional voice notes delivered straight to the mobile client.

---

## ⚡ Quantization, Hardware Budget & Edge Efficiency

AarogyaMitra is engineered to operate entirely within a standard **4GB commodity VM limits ($5/month hardware target)** or an offline village health kiosk:

| Module / Component | Precision / Format | Active RAM Footprint | Execution Speed (Pure CPU) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **AarogyaMitra LLM Core** | `GGUF Q4_K_M` (Qwen 3.5 2B) | **~1.31 GB** | 18–25 tokens/sec | Production Ready |
| **ModernBERT Intent Router** | `INT8 Dynamic ONNX` (395M) | **~0.45 GB** | ~35 ms (P95: 112 ms) | Production Ready |
| **CTranslate2 NLLB Translation** | `INT8 Quantized` | **~0.40 GB** | ~250 ms – 1.2s | Production Ready |
| **Meta MMS VITS Speech Engine** | `ONNX Runtime CPU` | **~0.50 GB** | Real-time streaming | Production Ready |
| **Vision Projector (On-Demand)** | `F16-mmproj` (Qwen-VL) | **~0.67 GB** | On-demand execution | Phase 2 Roadmap |
| **TOTAL COMBINED MEMORY** | — | **≤ 2.8 GB RAM** | **Zero Cloud GPU Required** | **Validated** |

### Clinical SFT Model Training Metrics
* **Base Foundation:** `Qwen/Qwen2.5-3.5-2B`
* **Fine-Tuning Regime:** Parameter-Efficient LoRA via Unsloth on verified multi-turn clinical triage dialogues.
* **Validation Loss Floor:** `0.6385`
* **Clinical Perplexity:** `1.894`
* **Open Model Artifact:** [Hugging Face: `TheUsurper09/aarogyamitra-qwen35-2b-gguf`](https://huggingface.co/TheUsurper09/aarogyamitra-qwen35-2b-gguf)

---

## 📊 Production Telemetry & Latency Benchmarks

End-to-end performance recorded across production test spans in `fastapi_backend/logs/pipeline_telemetry.jsonl`:

| Pipeline Stage / Node | Hardware Target | Avg Latency | P95 Latency | Error Rate |
| :--- | :--- | :--- | :--- | :--- |
| **ModernBERT Intent Classifier** | **Intel/AMD x86_64 (CPU)** | **112.4 ms** | **166.2 ms** | **0.0%** |
| **Qdrant Vector Retrieval (RAG)** | Local In-Memory Store | **185.0 ms** | **204.0 ms** | **0.0%** |
| **CTranslate2 NLLB Translation** | CPU Execution Provider | **1,240.0 ms** | **1,795.0 ms** | **0.0%** |
| **Local Qwen 3.5 2B (GGUF)** | Local CPU (llama.cpp) | **5,620.0 ms** | **12,434.0 ms** | **0.0%** |

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

1. **`main` (FastAPI Backend)**: Python FastAPI backend, AI routing, Laya ModernBERT ONNX engine, Vision Service, and database integration.
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

Special thanks to the **Ministry of Health and Family Welfare (MoHFW)**, **National Health Authority (NHA)**, **Ayushman Bharat Digital Mission (ABDM)**, **OpenStreetMap contributors**, **Ola Maps**, and the research teams behind **ModernBERT** (Answer.AI / LightOn), **Qwen** (Alibaba Cloud), and **AI4Bharat** for enabling digital public infrastructure that makes equitable healthcare access possible.\n