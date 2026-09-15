import { getOrCreateDeviceId } from '../utils/userSession';

// Fallback to localhost if not provided via .env
export const BASE_URL = process.env.EXPO_PUBLIC_API_URL;

/**
 * A wrapper around fetch that automatically includes the X-Device-ID header
 * and standard application/json Accept headers.
 */
export const fetchWithDeviceContext = async (endpoint, options = {}) => {
  const deviceId = await getOrCreateDeviceId();

  const headers = {
    'Accept': 'application/json',
    'X-Device-ID': deviceId,
    ...(options.headers || {})
  };

  const url = `${BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} at ${url}`);
  }

  return response.json();
};
