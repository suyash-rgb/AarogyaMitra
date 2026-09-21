import { fetchWithDeviceContext } from './apiClient';

/**
 * Healthcare Schemes API Services
 */
export const searchSchemesRAG = async (query, state) => {
  return await fetchWithDeviceContext('/schemes/healthcare-schemes/rag/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, state }),
  });
};

export const getHealthcareSchemes = async (stateName) => {
  const queryParam = stateName ? `?state=${encodeURIComponent(stateName)}` : '';
  return await fetchWithDeviceContext(`/schemes/healthcare-schemes${queryParam}`);
};

export const getStates = async () => {
  return await fetchWithDeviceContext(`/schemes/healthcare-schemes/meta/states`);
};

export const getSchemeDetails = async (idOrSlug) => {
  return await fetchWithDeviceContext(`/schemes/healthcare-schemes/${idOrSlug}`);
};

/**
 * Healthcare Facilities API Services
 */
export const getNearbyFacilities = async (lat, lon, radius = 5000) => {
  return await fetchWithDeviceContext(`/healthcare-facilities/nearby?lat=${lat}&lon=${lon}&radius=${radius}`);
};

/**
 * User Intent Router Service
 */
export const classifyIntent = async (query, userContext = {}) => {
  return await fetchWithDeviceContext('/router/classify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      user_context: userContext,
    }),
  });
};

/**
 * Voice / Text-To-Speech API Service
 */
export const requestTTS = async (text, languageTag = 'hin_Deva') => {
  return await fetchWithDeviceContext('/voice/tts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      text,
      language_tag: languageTag,
      slow: false
    }),
  });
};


