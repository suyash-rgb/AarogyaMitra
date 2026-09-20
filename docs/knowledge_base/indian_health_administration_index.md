# Indian Public Health Administration Index

This index is a compact reference for AarogyaMitra's policy and facility-retrieval
pipelines. It uses one consistent table shape so that entries can be split into
independent RAG chunks without losing the administrative context of an acronym.
Hindi names are included for common user utterances; state and regional spellings
may vary.

> **Scope note:** Administrative titles and service names can differ between
> states. The entry describes the national or most common usage, not a legal
> delegation of authority. Verify a local order, referral protocol, or helpline
> before treating this index as operational advice.

## 1. Administrative hierarchy and governance

| Acronym / Term | Full Name (English) | Hindi / Regional Term | Administrative Level | Primary Function & Jurisdiction | RAG Query Triggers / Keywords |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MoHFW** | Ministry of Health and Family Welfare | स्वास्थ्य एवं परिवार कल्याण मंत्रालय | Central | Union ministry responsible for national health policy, programmes, standards, and family welfare. | central health ministry, Delhi health ministry, family welfare |
| **MoA** | Ministry of Ayush | आयुष मंत्रालय | Central | Policy and programmes for Ayurveda, Yoga, Unani, Siddha, and Homoeopathy systems. | ayush ministry, ayurvedic government scheme |
| **DGHS** | Directorate General of Health Services | स्वास्थ्य सेवा महानिदेशालय | Central | Technical public-health directorate; advises the Union government and coordinates national services. | director general health, central hospital authority |
| **NHA** | National Health Authority | राष्ट्रीय स्वास्थ्य प्राधिकरण | Central | Leads AB PM-JAY and ABDM implementation and their national digital and purchasing standards. | PM-JAY authority, ABDM authority, health scheme approval |
| **ICMR** | Indian Council of Medical Research | भारतीय आयुर्विज्ञान अनुसंधान परिषद | Central | National biomedical research body; issues evidence and research guidance. | medical research India, ICMR guideline |
| **CCRAS** | Central Council for Research in Ayurvedic Sciences | केंद्रीय आयुर्वेदीय विज्ञान अनुसंधान परिषद | Central | Research council for Ayurvedic medicine and evidence generation. | CCRAS, ayurveda research council |
| **DHS** | Directorate of Health Services | स्वास्थ्य सेवा निदेशालय | State / UT | State technical directorate supervising public hospitals, primary care, and programme delivery. | state health directorate, DHS order |
| **DHFWS** | Department of Health and Family Welfare | स्वास्थ्य एवं परिवार कल्याण विभाग | State / UT | State administrative department that budgets, commissions, and governs health services. | state health department, health secretary |
| **SHA** | State Health Agency | राज्य स्वास्थ्य एजेंसी | State / UT | State nodal agency implementing and purchasing services under PM-JAY. | PM-JAY state office, Ayushman claim, SHA |
| **SMC** | State Medical Council | राज्य चिकित्सा परिषद | State / UT | Registers medical practitioners and handles professional regulation within the state. | doctor registration, medical council, license |
| **DHS (district)** | District Health Society | जिला स्वास्थ्य समिति | District | District Mission/NHM planning and convergence body; manages approved programme activities. | district health society, NHM district |
| **CMHO** | Chief Medical and Health Officer | मुख्य चिकित्सा एवं स्वास्थ्य अधिकारी | District | Common district public-health administrator; coordinates programmes, licensing, and reporting. | CMHO permission, district health officer sign, dispensary approval |
| **CDMO** | Chief District Medical Officer / Civil Surgeon | मुख्य जिला चिकित्सा अधिकारी / सिविल सर्जन | District | Senior district hospital and clinical-administration authority; title varies by state. | civil surgeon, CDMO sign, district hospital authority |
| **DPM** | District Programme Manager | जिला कार्यक्रम प्रबंधक | District | NHM programme operations, data, procurement coordination, and reporting. | DPM NHM, programme manager district |
| **DNO** | District Nodal Officer | जिला नोडल अधिकारी | District | Nodal contact for a designated disease, scheme, or digital programme. | district nodal officer, scheme contact |
| **BMO / BMOH** | Block Medical Officer / Block Medical Officer of Health | खंड चिकित्सा अधिकारी / प्रखंड चिकित्सा पदाधिकारी | Block / Tehsil | Supervises block facilities, staff, outreach, reporting, and primary-to-secondary referrals. | BMO sign, block doctor, BMOH permission |
| **CBHO** | Community Block Health Office | सामुदायिक खंड स्वास्थ्य कार्यालय | Block / Tehsil | Block-level public-health office supporting facility operations and national programmes. | block health office, tehsil health office |
| **VHSNC** | Village Health, Sanitation and Nutrition Committee | ग्राम स्वास्थ्य, स्वच्छता एवं पोषण समिति | Village / Grassroots | Gram Sabha-linked committee for local health planning, sanitation, nutrition, and social monitoring. | village health committee, VHSNC meeting |
| **ASHA** | Accredited Social Health Activist | मान्यता प्राप्त सामाजिक स्वास्थ्य कार्यकर्ता / आशा | Village / Grassroots | Community link worker for mobilisation, maternal-child follow-up, referrals, and health awareness. | ASHA worker, आशा दीदी, village health worker |
| **ANM** | Auxiliary Nurse Midwife | सहायक नर्स दाई | Sub-centre / Village | Front-line nurse-midwife delivering immunisation, antenatal care, family planning, and records. | ANM, sub-centre nurse, vaccination worker |
| **AWW** | Anganwadi Worker | आंगनवाड़ी कार्यकर्ता | Village / Grassroots | ICDS worker supporting nutrition, preschool services, growth monitoring, and referrals. | anganwadi, child nutrition worker |
| **CHO** | Community Health Officer | सामुदायिक स्वास्थ्य अधिकारी | AAM / Sub-centre | Leads a Health and Wellness Centre team and provides comprehensive primary care and referral. | CHO, wellness centre officer, HWC staff |
| **PRI** | Panchayati Raj Institution | पंचायती राज संस्था | Village / Local government | Elected local-government system that supports local health, sanitation, and nutrition action. | panchayat health, sarpanch health approval |

## 2. Public healthcare delivery and referral tiers

| Acronym / Term | Full Name (English) | Hindi / Regional Term | Administrative Level | Primary Function & Jurisdiction | RAG Query Triggers / Keywords |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AIIMS** | All India Institute of Medical Sciences | अखिल भारतीय आयुर्विज्ञान संस्थान | Central / Tertiary | Apex teaching and referral institute providing advanced specialist and super-specialist care. | AIIMS, apex hospital, tertiary referral |
| **GMC** | Government Medical College and Hospital | शासकीय चिकित्सा महाविद्यालय एवं अस्पताल | State / Tertiary | Teaching hospital providing specialist care, training, and referrals from district hospitals. | medical college hospital, GMC referral |
| **RRC** | Regional Referral Centre | क्षेत्रीय रेफरल केंद्र | Regional / Tertiary | Designated regional centre for cases beyond district and secondary-hospital capability. | regional referral, advanced referral centre |
| **DH** | District Hospital | जिला अस्पताल | District / Secondary | Main district-level inpatient, emergency, specialist, diagnostic, and referral hospital. | district hospital, zila hospital, emergency hospital |
| **SDH / CH** | Sub-District Hospital / Civil Hospital | उप-जिला अस्पताल / सिविल अस्पताल | Sub-district / Secondary | Intermediate referral hospital between CHC/PHC and the district hospital. | sub-district hospital, civil hospital, taluka hospital |
| **CHC** | Community Health Centre | सामुदायिक स्वास्थ्य केंद्र | Block / Secondary | First Referral Unit; commonly planned around 30 beds and core surgery, medicine, obstetric, and paediatric services. | CHC, block hospital, 30 bed ward, referral unit |
| **FRU** | First Referral Unit | प्रथम रेफरल इकाई | Block / Secondary | Facility with specialist, emergency, laboratory, blood-storage, and delivery capability designated for referrals. | FRU, emergency referral, delivery centre |
| **PHC** | Primary Health Centre | प्राथमिक स्वास्थ्य केंद्र | Primary / Block | Medical-officer-led primary-care facility and referral point for health sub-centres. | PHC, primary health centre, prathamik swasthya |
| **UPHC** | Urban Primary Health Centre | शहरी प्राथमिक स्वास्थ्य केंद्र | Urban / Primary | Urban primary-care facility for OPD, preventive care, and referral. | urban PHC, UPHC, city dispensary |
| **AAM** | Ayushman Arogya Mandir | आयुष्मान आरोग्य मंदिर | Village / Primary | Rebranded Health and Wellness Centre providing expanded comprehensive primary healthcare. | AAM, arogya mandir, wellness centre |
| **HWC** | Health and Wellness Centre | स्वास्थ्य एवं कल्याण केंद्र | Village / Primary | Former designation for upgraded sub-centres and PHCs with preventive, NCD, maternal, and telehealth services. | HWC, health wellness centre, wellness sub-centre |
| **SHC / HSC** | Sub-Health Centre / Health Sub-Centre | उप-स्वास्थ्य केंद्र | Village / Primary | Most peripheral facility, usually staffed by ANM/MPW and linked to a PHC. | sub-centre, sub centre, up-swasthya kendra |
| **MMU** | Mobile Medical Unit | मोबाइल चिकित्सा इकाई | Outreach | Mobile team or van delivering services to remote, tribal, or disaster-affected communities. | mobile clinic, medical van, remote camp |
| **MPW** | Multipurpose Health Worker | बहुउद्देशीय स्वास्थ्य कार्यकर्ता | Sub-centre / Field | Field worker supporting communicable disease control, sanitation, immunisation, and surveillance. | MPW, male health worker, field health worker |

Referral direction is normally **SHC/AAM → PHC → CHC/SDH → DH → GMC/AIIMS**.
Actual referral eligibility, bed availability, ambulance routing, and state naming
must be confirmed locally; a facility's tier does not guarantee that a service is
available today.

## 3. Welfare schemes and infrastructure programmes

| Acronym / Term | Full Name (English) | Hindi / Regional Term | Administrative Level | Primary Function & Jurisdiction | RAG Query Triggers / Keywords |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AB PM-JAY** | Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana | आयुष्मान भारत प्रधानमंत्री जन आरोग्य योजना | National / State | Government-financed hospitalisation cover for eligible households through empanelled providers. | Ayushman card, PM-JAY, cashless treatment |
| **PM-ABHIM** | Pradhan Mantri Ayushman Bharat Health Infrastructure Mission | प्रधानमंत्री आयुष्मान भारत स्वास्थ्य अवसंरचना मिशन | National / State | Strengthens surveillance, laboratories, critical-care and public-health infrastructure. | PM-ABHIM, health infrastructure mission |
| **NHM** | National Health Mission | राष्ट्रीय स्वास्थ्य मिशन | National / State | Umbrella mission supporting rural and urban public health, workforce, and programmes. | NHM, health mission, state NHM |
| **NRHM** | National Rural Health Mission | राष्ट्रीय ग्रामीण स्वास्थ्य मिशन | Rural / National | Rural-health component now operating within NHM. | rural health mission, NRHM |
| **NUHM** | National Urban Health Mission | राष्ट्रीय शहरी स्वास्थ्य मिशन | Urban / National | Urban-poor primary-care component within NHM. | urban health mission, NUHM |
| **JSY** | Janani Suraksha Yojana | जननी सुरक्षा योजना | Maternal health | Conditional cash-assistance scheme promoting institutional delivery. | JSY benefit, maternity incentive, delivery scheme |
| **JSSK** | Janani Shishu Suraksha Karyakram | जननी शिशु सुरक्षा कार्यक्रम | Maternal and child health | Entitles pregnant women and sick newborns to free public-facility services and transport, subject to programme rules. | free delivery, free newborn care, JSSK transport |
| **PMMVY** | Pradhan Mantri Matru Vandana Yojana | प्रधानमंत्री मातृ वंदना योजना | Maternal / Social protection | Maternity benefit programme delivered through designated government channels. | PMMVY payment, pregnancy benefit |
| **RBSK** | Rashtriya Bal Swasthya Karyakram | राष्ट्रीय बाल स्वास्थ्य कार्यक्रम | Child health | Child screening and early intervention for the four Ds: defects, deficiencies, diseases, and developmental delays. | child screening, RBSK, school health |
| **UIP** | Universal Immunization Programme | सार्वभौमिक टीकाकरण कार्यक्रम | National / Primary | Routine immunisation programme delivered through public facilities and outreach sessions. | vaccine schedule, routine immunisation, UIP |
| **MI** | Mission Indradhanush | मिशन इंद्रधनुष | National / Outreach | Intensified immunisation drives for children and pregnant women who missed routine doses. | Indradhanush vaccine camp, missed vaccine |
| **NTEP** | National Tuberculosis Elimination Programme | राष्ट्रीय क्षय उन्मूलन कार्यक्रम | National / District | TB diagnosis, notification, treatment, adherence, and prevention services. | TB test, DOTS, NTEP |
| **NVBDCP** | National Vector Borne Disease Control Programme | राष्ट्रीय वेक्टर जनित रोग नियंत्रण कार्यक्रम | National / State | Control programme for malaria, dengue, kala-azar, filariasis, chikungunya, and Japanese encephalitis. | malaria programme, dengue control, mosquito disease |
| **IDSP** | Integrated Disease Surveillance Programme | एकीकृत रोग निगरानी कार्यक्रम | National / District | Surveillance and outbreak reporting network for epidemic-prone diseases. | outbreak reporting, disease surveillance, IDSP |
| **NPCDCS** | National Programme for Prevention and Control of Cancer, Diabetes, Cardiovascular Diseases and Stroke | कैंसर, मधुमेह, हृदय रोग एवं स्ट्रोक नियंत्रण कार्यक्रम | National / Primary | Screening and management pathway for major non-communicable diseases. | NCD screening, diabetes camp, hypertension check |

## 4. Digital public infrastructure, telehealth, and emergency access

| Acronym / Term | Full Name (English) | Hindi / Regional Term | Administrative Level | Primary Function & Jurisdiction | RAG Query Triggers / Keywords |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ABDM** | Ayushman Bharat Digital Mission | आयुष्मान भारत डिजिटल मिशन | National / Digital | Digital-health building blocks, registries, consent, and interoperable records. | ABDM, digital health India |
| **ABHA** | Ayushman Bharat Health Account | आभा / डिजिटल स्वास्थ्य खाता | National / Individual | 14-digit digital-health identifier used to link records with user consent. It is not insurance. | ABHA card, health ID, digital parcha |
| **HFR** | Health Facility Registry | स्वास्थ्य सुविधा रजिस्ट्री | National / Registry | Registry of public and private health facilities and their digital identity. | HFR, facility ID, register hospital |
| **HPR** | Healthcare Professionals Registry | स्वास्थ्य पेशेवर रजिस्ट्री | National / Registry | Registry of verified healthcare professionals and their professional identity. | HPR, doctor registry, professional ID |
| **PHR** | Personal Health Record | व्यक्तिगत स्वास्थ्य रिकॉर्ड | Individual / Digital | Person-controlled record assembled from linked health information. | PHR, digital medical record, health history |
| **UHI** | Unified Health Interface | यूनिफाइड हेल्थ इंटरफेस | National / Digital | Open, interoperable network concept for discoverable digital health services. | UHI, digital appointment, health network |
| **eSanjeevani** | National Teleconsultation Service | ई-संजीवनी | National / Telehealth | Government teleconsultation platform connecting patients and providers through hub-and-spoke services. | eSanjeevani, online government doctor |
| **104** | State Health Advice and Grievance Helpline | राज्य स्वास्थ्य सलाह हेल्पलाइन | State / Tele-triage | State-operated health advice or grievance number; availability and services vary by state. | 104 doctor, medical advice helpline |
| **108** | Emergency Medical Ambulance Service | आपातकालीन एम्बुलेंस सेवा | State / Emergency | Emergency ambulance access in participating states; dispatch and coverage are state-specific. | 108 ambulance, emergency ambulance |
| **112** | National Unified Emergency Number | राष्ट्रीय एकीकृत आपातकालीन नंबर | National / Emergency | Unified emergency response number for police, fire, and medical assistance. | 112 emergency, national emergency number |
| **EMR** | Electronic Medical Record | इलेक्ट्रॉनिक चिकित्सा रिकॉर्ड | Facility / Digital | Digital clinical record maintained by a provider or facility. | electronic record, digital prescription |
| **OTP** | One-Time Password | एक बार का पासवर्ड | Digital identity | Temporary verification code used during consent or account authentication. | OTP not received, ABHA verification |

## 5. Retrieval and classifier alignment

The facility-discovery implementation currently performs classification in
`fastapi_backend/app/core/utils.py::classify_facility` (rather than a symbol named
`GOVT_PATTERNS`). The following terms are deliberately aligned with that
implementation:

| Classifier concern | Current matching terms | Index entries that provide context |
| :--- | :--- | :--- |
| Primary facilities | `PHC`, `primary health`, `prathamik swasthya` | PHC, UPHC |
| Community facilities | `CHC`, `community health`, `samudayik swasthya` | CHC, FRU |
| District/civil facilities | `district hospital`, `civil hospital`, `bhoj hospital`, `zila hospital` | DH, SDH / CH |
| Peripheral facilities | `sub-centre`, `sub centre`, `up-swasthya`, `HSC` | SHC / HSC, AAM, HWC |
| Tertiary facilities | `medical college`, `AIIMS` | GMC, AIIMS, RRC |
| General government markers | `govt`, `government`, `sub-district`, `swasthya kendra`, `arogya mandir`, `sarkari`, `jan aushadhi` | AAM, SDH / CH, PHC |

These matching terms are retrieval aids, not proof that a facility is public or
that a service is available. The service also considers OSM operator tags, and
user-facing results should retain the source, address, and last-verified status.

