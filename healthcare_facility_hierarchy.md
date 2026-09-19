# Government Healthcare Facilities Hierarchy

This document outlines the operational hierarchy and classification of public healthcare facilities in India as defined by the **Indian Public Health Standards (IPHS)**, and maps them to the `tier_level` logic used in the **ArogyaMitra** database and AI routing engine.

Understanding this hierarchy is critical for filtering nearby public facilities, prioritizing emergency care, and routing patients to the appropriate medical tier based on symptom acuity.

---

## 🏗️ Public Healthcare Hierarchy Diagram

```mermaid
flowchart TD
    %% Styling Definitions
    classDef t3Style fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b,font-weight:bold;
    classDef t2Style fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#92400e,font-weight:bold;
    classDef t1Style fill:#dcfce7,stroke:#22c55e,stroke-width:2px,color:#166534,font-weight:bold;
    classDef subNode fill:#ffffff,stroke:#64748b,stroke-width:1px,color:#1e293b;

    %% Main Tier Nodes
    T3["🏛️ TIER 3: TERTIARY CARE<br/>Apex Institutes & Medical Colleges"]:::t3Style
    T2["🏥 TIER 2: SECONDARY CARE<br/>District Hospitals & CHCs"]:::t2Style
    T1["🩺 TIER 1: PRIMARY CARE<br/>PHCs, HWCs & Sub-Centres"]:::t1Style

    %% Referral Escalation & Step-Down Flows
    T1 -->|"⬆️ Referral (Surgeries, Inpatient, Fractures)"| T2
    T2 -->|"⬆️ Referral (Super-Specialties, Oncology, Neuro)"| T3
    T3 -.->"⬇️ Step-Down Care & Chronic Follow-Up"-.-> T2
    T2 -.->"⬇️ Community Rehabilitation & Preventive Care"-.-> T1

    %% Tier 3 Subgraph
    subgraph Tier3Group ["Tier 3 Facilities (Apex & Tertiary)"]
        T3_1["Medical College Hospitals"]:::subNode
        T3_2["AIIMS / National Apex Institutes"]:::subNode
        T3_3["Super-Specialty Hospitals (>500 Beds)"]:::subNode
    end
    T3 --- Tier3Group

    %% Tier 2 Subgraph
    subgraph Tier2Group ["Tier 2 Facilities (First Referral Units - FRUs)"]
        T2_1["District Hospitals (100 - 500 Beds)"]:::subNode
        T2_2["Sub-District / Taluka Hospitals"]:::subNode
        T2_3["Community Health Centres (30 Beds / 4 Specialists)"]:::subNode
        T2_4["Civil & Women / Maternity Hospitals"]:::subNode
    end
    T2 --- Tier2Group

    %% Tier 1 Subgraph
    subgraph Tier1Group ["Tier 1 Facilities (Primary & Peripheral Care)"]
        T1_1["Primary Health Centres (20,000 - 30,000 Pop)"]:::subNode
        T1_2["Ayushman Bharat Health & Wellness Centres (HWCs)"]:::subNode
        T1_3["Sub-Centres / Health Sub-Centres (3,000 - 5,000 Pop)"]:::subNode
        T1_4["Urban Health Posts & Ayush Dispensaries"]:::subNode
    end
    T1 --- Tier1Group
```

---

## 📊 Comprehensive Tier Comparison Matrix

| Tier Level | DB Parameter (`tier_level`) | Facilities Included | Population Coverage | Bed Capacity | Primary Medical Services | ArogyaMitra AI Routing Logic |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1 (Primary)** | `1_primary` | Sub-Centres, PHCs, UPHCs, HWCs, Dispensaries | 3,000 – 30,000 | 0 – 6 Beds | Immunization, basic OPD, prenatal checkups, minor fevers, preliminary NCD screening | Mild symptoms, routine vaccinations, OTC consultation, minor cuts |
| **Tier 2 (Secondary)** | `2_secondary` | CHCs, Sub-District Hospitals, District Hospitals, Women Hospitals | 80,000 – 500,000+ | 30 – 500 Beds | Specialist care (Surgery, Pediatrics, OB/GYN), X-ray, ICU, blood bank, trauma | Fractures, high fever, childbirth, emergency trauma, inpatient admissions |
| **Tier 3 (Tertiary)** | `3_tertiary` | Medical Colleges, AIIMS, Regional Cancer Centres | State/National Level | > 500 Beds | Advanced super-specialty surgery, oncology, neurosurgery, organ transplants | Referred cases, cancer care, complex cardiac surgery, specialized neurology |

---

## 🩺 Tier Breakdown & Functional Details

### Tier 1: Primary Healthcare (`1_primary`)
*The peripheral entry point for rural and urban communities into the public health system. Focuses on preventive care, maternal health, basic diagnostics, and outpatient treatment.*

- **Sub-Health Centres (SHC) / Health Sub-Centres (HSC):** The most accessible peripheral contact point in rural India (serving 3,000 to 5,000 residents). Staffed by ANMs, Accredited Social Health Activists (ASHA), and Health Workers.
- **Primary Health Centres (PHC) & Urban PHCs (UPHC):** Manned by a Medical Officer (MBBS). Acts as the primary referral hub for 6 Sub-Centres (serving 20,000 to 30,000 residents).
- **Health & Wellness Centres (HWC):** Upgraded SHCs/PHCs under **Ayushman Bharat**, providing comprehensive primary healthcare, essential diagnostics, free tele-consultation, and chronic NCD screening (diabetes, hypertension).
- **Urban Health Posts / Dispensaries / AYUSH Clinics:** Basic urban outpatient units providing primary care consultations and traditional Indian medicine systems (Ayurveda, Yoga, Unani, Siddha, Homeopathy).

> [!TIP]
> **AI Routing Guidance:** Recommend **Tier 1** facilities for non-emergency queries, basic fever/colds, routine vaccinations, maternal health checkups, and minor scrapes to prevent overcrowding at major hospitals.

---

### Tier 2: Secondary Healthcare (`2_secondary`)
*Serves as the First Referral Unit (FRU) for primary care facilities. Equipped with specialist physicians, operating theaters, emergency wards, and diagnostic labs.*

- **Community Health Centres (CHC):** Block-level hospitals serving 80,000 to 1,20,000 residents. Staffed by 4 core specialists (Surgeon, Physician, Gynecologist, Pediatrician) with 30 bed capacity, labor rooms, and X-ray facilities.
- **Sub-District Hospitals (SDH) / Taluka Hospitals:** Intermediate hospitals at the sub-district level that bridge CHCs and main District Hospitals.
- **District Hospitals (DH):** The flagship public hospital at the district center (100 to 500+ beds). Provides comprehensive secondary care, intensive care units (ICU), emergency trauma care, advanced labs, and blood banks.
- **Women Hospitals / Maternity Hospitals:** Specialized secondary care centers dedicated exclusively to high-risk pregnancies, obstetric emergencies, and neonatal care.

> [!IMPORTANT]
> **AI Routing Guidance:** Escalate users to **Tier 2** immediately for acute emergencies, suspected bone fractures, high persistent fever, acute abdominal pain, childbirth, or cases requiring inpatient bed admission.

---

### Tier 3: Tertiary Healthcare (`3_tertiary`)
*Top-tier apex teaching hospitals, national medical centers, and specialized research institutes.*

- **Medical Colleges & Teaching Hospitals:** Government institutions attached to state medical universities providing tertiary multi-specialty clinical care and medical education.
- **Apex Institutes & Regional Cancer Centres:** Elite national facilities such as **AIIMS (All India Institute of Medical Sciences)**, **NIMHANS**, and specialized cardiology or oncology centers equipped for complex surgeries and organ transplants.

> [!CAUTION]
> **AI Routing Guidance:** Reserve **Tier 3** recommendations strictly for specialized conditions (e.g. oncology, neurosurgery, organ failure) or formal hospital referrals. Do not recommend Tier 3 for routine first-aid or minor complaints.

---

### Unclassified / Specialized Units (`unknown`)
*Facilities serving specialized administrative roles or temporary field units.*

- **Mobile Medical Units (MMU):** Specially equipped medical vans offering diagnostic and clinical services to remote, tribal, or disaster-affected regions.
- **Unverified / Administrative Clinics:** Data records undergoing categorization.

---

## ⚡ Integration with ArogyaMitra API & AI Router

When querying the facility discovery endpoint `/api/v1/govt-healthcare-facilities/nearby`, developers and clients can filter by the `tier_level` parameter:

```http
GET /api/v1/govt-healthcare-facilities/nearby?latitude=23.2599&longitude=77.4126&tier_level=1_primary&radius_km=10
```

### Supported API Tier Parameters:
- `?tier_level=1_primary`: Returns nearby Sub-Centres, PHCs, and HWCs.
- `?tier_level=2_secondary`: Returns nearby CHCs, Sub-District, and District Hospitals.
- `?tier_level=3_tertiary`: Returns Medical Colleges and Apex Institutes (e.g., AIIMS).
- `?tier_level=all` *(Default)*: Returns all public facilities sorted by geodesic proximity.
