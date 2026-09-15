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
