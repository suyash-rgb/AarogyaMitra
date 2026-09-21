import axios from 'axios';
import { getDeviceId, getUserState, getCurrentLanguage } from '../utils/storage';
import { HEALTHCARE_SCHEMES, NEARBY_FACILITIES, EMPANELED_DOCTORS } from '../data/mockData';

const BASE_URL = 'http://localhost:8000'; // Default API backend server

const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to attach X-Device-ID header
apiClient.interceptors.request.use((config) => {
  const deviceId = getDeviceId();
  config.headers['X-Device-ID'] = deviceId;
  return config;
}, (error) => Promise.reject(error));

/**
 * Intelligent Intent Classifier & Query Router
 */
export async function classifyQuery(userQuery) {
  const userState = getUserState();
  const lang = getCurrentLanguage();
  const q = userQuery.toLowerCase().trim();

  // Check special triggers
  if (q === '104' || q.includes('helpline 104') || q.includes('call 104')) {
    return {
      intent: 'CALL_104',
      message: '📞 **Connecting to Health Helpline 104**...\n\nCall 104 for 24x7 medical advice, emergency health support, and grievance redressal.',
      actionUrl: 'tel:104'
    };
  }

  if (q.includes('esanjeevani') || q.includes('e-sanjeevani')) {
    return {
      intent: 'EXTERNAL_REDIRECT',
      message: '🩺 **Redirecting to eSanjeevani OPD National Teleconsultation Portal**...\n\nOfficial Government OPD Portal: https://esanjeevaniopd.in',
      actionUrl: 'https://esanjeevaniopd.in'
    };
  }

  if (q.includes('abha') || q.includes('book doctor') || q.includes('tele-consult') || q.includes('doctor call')) {
    return {
      intent: 'DOCTOR_CAROUSEL',
      message: '🩺 Here are empaneled Government Doctors available for **Free Tele-consultation**. Select a doctor to generate your **ABHA Appointment Ticket**:',
      doctors: EMPANELED_DOCTORS
    };
  }

  // Attempt backend API call first
  try {
    const res = await apiClient.post('/api/v1/router/classify', {
      query: userQuery,
      user_context: {
        state: userState,
        language: lang
      }
    });

    if (res.data && res.data.response_data) {
      return res.data;
    }
  } catch (err) {
    console.warn('Backend API unavailable, using intelligent local fallback:', err.message);
  }

  // Fallback Rule-Based Classifier
  if (q.includes('scheme') || q.includes('yojana') || q.includes('ayushman') || q.includes('pm-jay') || q.includes('card') || q.includes('insurance') || q.includes('know govt schemes')) {
    return {
      intent: 'GOVT_SCHEMES_DISCOVERY',
      message: `📜 Found official healthcare schemes for **${userState}** & Central Government:`,
      schemes: HEALTHCARE_SCHEMES
    };
  }

  if (q.includes('hospital') || q.includes('phc') || q.includes('chc') || q.includes('centre') || q.includes('locate') || q.includes('facility') || q.includes('nearby') || q.includes('locate a healthcare facility')) {
    return {
      intent: 'FACILITY_DISCOVERY',
      message: `🏥 Nearby primary healthcare centres & civil hospitals near your location:`,
      facilities: NEARBY_FACILITIES
    };
  }

  if (q.includes('change language') || q.includes('bhasha') || q.includes('language')) {
    return {
      intent: 'OPEN_LANGUAGE_MODAL',
      message: '🌐 Please select your preferred language below:',
      openModal: 'language'
    };
  }

  // Default Medical Conversational QA
  return {
    intent: 'GENERAL_MEDICAL_QA',
    message: `🤖 **AarogyaMitra Clinical Guidance**:\n\nThank you for reaching out. Based on your input *"_${userQuery}_"*, here is initial guidance:\n\n1. For fever or cold, ensure hydration and rest.\n2. Consult an empaneled doctor for persistent symptoms (>48 hours).\n3. Keep your **ABHA Health ID** ready for hospital OPD visits.\n\n*Would you like to book a doctor call or find a nearby PHC?*`,
    quickReplies: ['Book Doctor Call', 'Locate a Healthcare Facility', 'Know Govt Schemes', 'Call 104 Helpline']
  };
}

/**
 * Fetch Nearby Facilities based on Browser Geolocation
 */
export async function fetchNearbyFacilities(lat, lon) {
  try {
    const res = await apiClient.get(`/api/v1/healthcare-facilities/nearby?lat=${lat}&lon=${lon}&radius=5000`);
    if (res.data && Array.isArray(res.data)) {
      return res.data;
    }
  } catch (e) {
    console.warn('Backend facility API offline, returning mock facilities');
  }
  return NEARBY_FACILITIES;
}

/**
 * Fetch Text-to-Speech (TTS) audio for bot messages
 */
export async function fetchTTS(text, langTag) {
  try {
    const res = await apiClient.post('/api/v1/voice/tts', {
      text: text,
      language_tag: langTag
    });
    // Assuming backend returns { audio: 'base64...' } or just the base64 string
    // We'll return the raw data and let the component handle it.
    return res.data;
  } catch (e) {
    console.error('Failed to fetch TTS:', e);
    throw e;
  }
}
