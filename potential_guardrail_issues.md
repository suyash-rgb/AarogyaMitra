### 1. Deterministic Emergency Red-Flag Interceptors

* **Pre-LLM Rule Bypass:** Intercept life-threatening presentations (e.g., crushing chest pain, sudden unilateral numbness, snakebite, stridor, or arterial bleeding) before calling the LLM. Instantly return a static, verified emergency template with **108 / 112** instructions to eliminate generation latency and prevent hallucination risk.
* **Tropical Fever / NSAID Prohibition:** Strictly prohibit the recommendation of NSAIDs (such as Ibuprofen, Combiflam, Aspirin, or Diclofenac) for undifferentiated acute fevers. In India's endemic profile, administering NSAIDs during acute Dengue can trigger catastrophic gastrointestinal bleeding and platelet dysfunction.

---

### 2. Pharmacological & Regulatory Boundaries (NMC / CDSCO)

* **Schedule H / H1 / X Hard Refusals:** Adhere strictly to the National Medical Commission (NMC) Telemedicine Practice Guidelines. The assistant must never calculate dosages, recommend initiation, or modify regimens for Schedule H/H1 medicines (such as systemic antibiotics, steroids, cardiac drugs, or psychiatric medications).
* **Dual-Paracetamol Toxicity Detection:** Detect and flag duplicate Acetaminophen/Paracetamol ingestion across multiple common Indian OTC brands (for example, warning a user against taking Dolo-650 concurrently with cold-relief formulations like Cheston Cold or Sinarest).

---

### 3. Pediatric & Vulnerable Cohort Safety Gates

* **Infant Redirection (< 1 Year):** Any presentation involving infants under 12 months with persistent vomiting, poor feeding, lethargy, or high fever must trigger an immediate referral to a pediatrician or Primary Health Centre (PHC), bypassing home remedies and adult OTC advice entirely.
* **Pregnancy & Teratogenicity Checks:** Block unvetted botanical or pharmacological advice for pregnant or lactating patients. Classical formulations containing strong emmenagogues, heavy-metal bhasmas, or herbs like *Guggulu* and *Aloe vera* (in high doses) must trigger an explicit contraindication warning.

---

### 4. RAG Retrieval & Administrative Grounding

* **Scheme Claim Verification:** Enforce a strict factual adherence threshold on government entitlement queries (PM-JAY, ABHA, state-specific funds). If the model's drafted response cannot be matched to the retrieved context, suppress the answer to prevent users from arriving at hospitals expecting non-existent benefits.
* **Low-Similarity Fallback:** When ChromaDB/PostgreSQL similarity scores fall below a predetermined threshold (e.g., cosine distance $> 0.45$), force the model to declare an absence of authoritative clinical references and advise in-person triage rather than falling back on ungrounded parametric memory.

---