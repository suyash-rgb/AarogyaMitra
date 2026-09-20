export const INDIAN_STATES = [
  "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar",
  "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa",
  "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka",
  "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh", "Maharashtra", "Manipur",
  "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Puducherry", "Punjab",
  "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh",
  "Uttarakhand", "West Bengal"
];

export const INDIC_LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिंदी' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' }
];

export const EMPANELED_DOCTORS = [
  {
    id: 'doc-1',
    name: 'Dr. Rahul Sharma',
    specialty: 'General Physician & Family Medicine',
    experience: '12 Years Exp',
    rating: 4.9,
    reviews: 1420,
    fees: 'FREE (Govt. Empaneled)',
    availableTime: 'Today, 11:30 AM',
    avatar: 'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=200&auto=format&fit=crop&q=80',
    hospital: 'AIIMS Tele-Consult Hub'
  },
  {
    id: 'doc-2',
    name: 'Dr. Ananya Roy',
    specialty: 'Pediatrics & Child Healthcare',
    experience: '9 Years Exp',
    rating: 4.8,
    reviews: 980,
    fees: 'FREE (Govt. Empaneled)',
    availableTime: 'Today, 02:00 PM',
    avatar: 'https://images.unsplash.com/photo-1594824813571-2153349aed06?w=200&auto=format&fit=crop&q=80',
    hospital: 'District Hospital OPD'
  },
  {
    id: 'doc-3',
    name: 'Dr. Suresh Varma',
    specialty: 'Cardiology & Vascular Health',
    experience: '16 Years Exp',
    rating: 4.95,
    reviews: 2150,
    fees: 'FREE (Govt. Empaneled)',
    availableTime: 'Tomorrow, 10:00 AM',
    avatar: 'https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=200&auto=format&fit=crop&q=80',
    hospital: 'State Heart Institute'
  },
  {
    id: 'doc-4',
    name: 'Dr. Priya Nair',
    specialty: 'Obstetrics & Gynecology (Maternal Care)',
    experience: '11 Years Exp',
    rating: 4.85,
    reviews: 1100,
    fees: 'FREE (Govt. Empaneled)',
    availableTime: 'Today, 04:30 PM',
    avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=200&auto=format&fit=crop&q=80',
    hospital: 'District Women Hospital'
  }
];

export const NEARBY_FACILITIES = [
  {
    id: 'fac-1',
    name: 'District Civil Hospital & Trauma Centre',
    tier: 'Government Tertiary Hospital',
    distanceKm: '1.2 km away',
    lat: 19.0760,
    lon: 72.8777,
    statusBadge: '24/7 TRAUMA & EMERGENCY',
    services: ['ICU', 'Emergency', 'Blood Bank', 'OPD', 'Free Dialysis'],
    phone: '022-24301122',
    address: 'Station Road, Ward 4, District HQ',
    image: 'https://images.unsplash.com/photo-1587351021759-3e566b6af7cc?w=400&auto=format&fit=crop&q=80'
  },
  {
    id: 'fac-2',
    name: 'Community Health Centre (CHC) Sunrise',
    tier: 'Government Secondary Healthcare',
    distanceKm: '3.5 km away',
    lat: 19.0850,
    lon: 72.8900,
    statusBadge: 'CHC OPD & MATERNITY',
    services: ['24x7 Delivery', 'Immunization', 'Essential Drugs', 'Lab Tests'],
    phone: '022-25983344',
    address: 'Main Bazaar Road, Sub-District Block',
    image: 'https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=400&auto=format&fit=crop&q=80'
  },
  {
    id: 'fac-3',
    name: 'Ayushman Arogya Mandir (PHC Sub-Centre)',
    tier: 'Primary Health Centre (Wellness Hub)',
    distanceKm: '0.8 km away',
    lat: 19.0700,
    lon: 72.8650,
    statusBadge: 'PHC OPD & NCD SCREENING',
    services: ['Free Medicine', 'BP & Diabetes Screening', 'Tele-consultation', 'ANC Checkup'],
    phone: '104 Helpline',
    address: 'Near Panchayat Bhavan, Sector 2',
    image: 'https://images.unsplash.com/photo-1516549655169-df83a0774514?w=400&auto=format&fit=crop&q=80'
  }
];

export const HEALTHCARE_SCHEMES = [
  {
    id: 'pmjay',
    slug: 'ayushman-bharat-pmjay',
    title: 'Ayushman Bharat PM-JAY (Pradhan Mantri Jan Arogya Yojana)',
    level: 'CENTRAL',
    department: 'National Health Authority (NHA) & Ministry of Health',
    description: 'World\'s largest government-funded health assurance scheme providing ₹5 Lakhs annual hospitalization cover per family.',
    benefits: [
      'Cashless and paperless access to healthcare services at empaneled hospitals.',
      'Cover up to ₹5,000,000 per family per year for secondary and tertiary care hospitalization.',
      'Pre and post-hospitalization expenses covered up to 15 days.',
      'Covers 1,949 medical procedures including oncology, cardiology, and orthopedics.'
    ],
    eligibility: [
      'Families identified under SECC 2011 (Socio-Economic Caste Census) database.',
      'Deprived rural families (single room, female-headed household, SC/ST, landless laborers).',
      'Occupational categories of urban workers (ragpickers, domestic workers, street vendors, construction workers).',
      'All senior citizens aged 70 and above (under PM-JAY Vaya Vandana extension).'
    ],
    documents: [
      'Aadhaar Card of family members',
      'Ration Card / Family ID',
      'Mobile number linked with Aadhaar',
      'PM-JAY Family Identification Certificate (if available)'
    ],
    process: [
      'Check eligibility online or at nearest Ayushman Mitra kiosk in empaneled hospital.',
      'Visit any Empaneled Public or Private Hospital (EHCP).',
      'Contact Ayushman Mitra at hospital desk for e-Card verification.',
      'Get cashless treatment; hospital settles claims directly with NHA.'
    ],
    faqs: [
      { q: 'Is there any family cap size?', a: 'No, there is no restriction on family size, age, or gender.' },
      { q: 'Are pre-existing conditions covered?', a: 'Yes, all pre-existing medical conditions are covered from Day 1.' }
    ],
    references: [
      { title: 'Official PM-JAY Portal', url: 'https://pmjay.gov.in' },
      { title: 'Check Eligibility Portal (NHA)', url: 'https://beneficiary.nha.gov.in' }
    ]
  },
  {
    id: 'pmsma',
    slug: 'pm-surakshit-matritva-abhiyan',
    title: 'Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)',
    level: 'CENTRAL',
    department: 'Maternal Health Division, MoHFW',
    description: 'Guarantees free, comprehensive, and quality antenatal care (ANC) services to pregnant women on the 9th of every month.',
    benefits: [
      'Free Antenatal Care (ANC) package including blood tests, ultrasound, and specialist checkup.',
      'Identification of High-Risk Pregnancies (HRP) for specialized follow-up.',
      'Free iron, folic acid, and essential nutrition supplements.',
      'Free transport assistance under Janani Shishu Suraksha Karyakram (JSSK).'
    ],
    eligibility: [
      'All pregnant women in their 2nd or 3rd trimester (after 12 weeks of pregnancy).',
      'Applicable across rural and urban government healthcare facilities.'
    ],
    documents: [
      'Mother and Child Protection (MCP) Card / RCH ID',
      'Aadhaar Card',
      'Bank account details (for Janani Suraksha Yojana cash benefit link)'
    ],
    process: [
      'Visit nearest PHC, CHC, or District Hospital on the 9th of any month.',
      'Register at PMSMA counter with MCP Card.',
      'Undergo medical examination, diagnostics, and counseling by OBGY Specialist.'
    ],
    faqs: [
      { q: 'Is ultrasound test free under PMSMA?', a: 'Yes, ultrasound screening is provided completely free of cost.' }
    ],
    references: [
      { title: 'PMSMA National Portal', url: 'https://pmsma.nhp.gov.in' }
    ]
  },
  {
    id: 'mjpjay',
    slug: 'mahatma-jyotirao-phule-jan-arogya-yojana',
    title: 'Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)',
    level: 'STATE (Maharashtra)',
    department: 'State Health Assurance Society, Govt. of Maharashtra',
    description: 'State flagship health insurance scheme providing coverage up to ₹5 Lakhs per family for Maharashtra residents.',
    benefits: [
      'Cashless quality medical care for 996 surgical and medical procedures.',
      'Coverage limit of ₹500,000 per family per year.',
      'Renal transplant surgery covered up to ₹10 Lakhs.',
      'Covers pre-existing illnesses and post-op medicines up to 10 days.'
    ],
    eligibility: [
      'Yellow, Antyodaya Anna Yojana (AAY), Annapurna, and Orange Ration Card holders in Maharashtra.',
      'Farmers from 14 distressed agricultural districts of Maharashtra.',
      'Registered construction workers and senior citizens.'
    ],
    documents: [
      'Valid Orange / Yellow / AAY Ration Card',
      'Aadhaar Card / Voter ID',
      'Domicile Certificate of Maharashtra'
    ],
    process: [
      'Visit Arogyamitra at empaneled hospital desk.',
      'Submit Ration card & photo ID for digital pre-authorization.',
      'Receive cashless treatment and free discharge medicines.'
    ],
    faqs: [
      { q: 'Can I use MJPJAY alongside PM-JAY?', a: 'Yes, Maharashtra operates an integrated MJPJAY & PM-JAY scheme on a single health card.' }
    ],
    references: [
      { title: 'MJPJAY Maharashtra Portal', url: 'https://www.jeevandayee.gov.in' }
    ]
  },
  {
    id: 'jsy',
    slug: 'janani-suraksha-yojana',
    title: 'Janani Suraksha Yojana (JSY)',
    level: 'CENTRAL',
    department: 'National Health Mission (NHM)',
    description: 'Safe motherhood intervention providing direct cash assistance to eligible pregnant women opting for institutional delivery.',
    benefits: [
      'Direct Bank Transfer of ₹1,400 (Rural) / ₹1,000 (Urban) for mothers upon hospital delivery.',
      'Cash incentive of ₹600 to ASHA worker for accompanying mother.',
      'Free C-section delivery, medicines, blood, and diet during hospital stay.'
    ],
    eligibility: [
      'Pregnant women belonging to BPL/SC/ST categories delivering in public health institutions.',
      'All pregnant women in Low Performing States (LPS) irrespective of age or number of children.'
    ],
    documents: [
      'BPL Ration Card / Caste Certificate',
      'MCP Card',
      'Bank Account Passbook (Aadhaar Seeded)'
    ],
    process: [
      'Register pregnancy at local Anganwadi or PHC with ASHA worker.',
      'Choose institutional delivery at government hospital or accredited private facility.',
      'Incentive credited directly to DBT account after birth.'
    ],
    faqs: [
      { q: 'Is home delivery eligible?', a: 'BPL women opting for home delivery get ₹500 assistance.' }
    ],
    references: [
      { title: 'NHM JSY Details', url: 'https://nhm.gov.in' }
    ]
  }
];

export const INITIAL_CHATS = [
  {
    id: 'ai-bot',
    name: 'Aarogya Mitra',
    avatar: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=150&auto=format&fit=crop&q=80',
    isOfficial: true,
    isMetaAI: false,
    verifiedBadge: true,
    unreadCount: 1,
    onlineStatus: 'Government AI Health Assistant',
    phone: '+91 1800 11 4477',
    category: 'National Health Mission & Ministry of Health (MoHFW)',
    website: 'https://nhm.gov.in',
    lastMessageTime: '11:45 AM',
    messages: [
      {
        id: 'm1',
        sender: 'bot',
        text: '🙏 Namaste! Welcome to **AarogyaMitra** — your 24/7 Government AI Healthcare & Medical Assistant.\n\nI can help you with:\n- 🏥 **Locating nearby PHCs, CHCs & Civil Hospitals**\n- 📜 **Finding Govt Schemes & Ayushman Bharat (PM-JAY) Benefits**\n- 🩺 **Booking Free Doctor Tele-consultation Calls**\n- 🚑 **Emergency Helpline 104 Access**\n\nHow may I assist your family today?',
        timestamp: '11:45 AM',
        quickReplies: ['Know Govt Schemes', 'Locate a Healthcare Facility', 'Book Doctor Call', 'Call 104 Helpline', 'Change Language']
      }
    ]
  },
  {
    id: 'meta-ai',
    name: 'Meta AI',
    avatar: 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150&auto=format&fit=crop&q=80',
    isOfficial: true,
    isMetaAI: true,
    verifiedBadge: true,
    unreadCount: 0,
    onlineStatus: 'AI Assistant',
    phone: '+1 (800) META-AI',
    category: 'General AI Assistant',
    website: 'https://meta.ai',
    lastMessageTime: '10:15 AM',
    messages: [
      {
        id: 'mm1',
        sender: 'bot',
        text: 'Hello! I am Meta AI. Ask me anything about general wellness, fitness tips, or healthcare news.',
        timestamp: '10:15 AM'
      }
    ]
  }
];
