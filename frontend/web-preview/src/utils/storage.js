// Storage helper for persistence

const KEYS = {
  DEVICE_ID: 'X-Device-ID',
  USER_STATE: 'user_state',
  LANGUAGE: 'currentLanguage',
  CHATS: 'aarogya_chats_history',
  THEME: 'theme_preference',
};

export function getDeviceId() {
  let deviceId = localStorage.getItem(KEYS.DEVICE_ID);
  if (!deviceId) {
    deviceId = 'dev_' + Math.random().toString(36).substring(2, 11) + '_' + Date.now();
    localStorage.setItem(KEYS.DEVICE_ID, deviceId);
  }
  return deviceId;
}

export function getUserState() {
  return localStorage.getItem(KEYS.USER_STATE) || 'Maharashtra';
}

export function setUserState(stateName) {
  localStorage.setItem(KEYS.USER_STATE, stateName);
}

export function getCurrentLanguage() {
  return localStorage.getItem(KEYS.LANGUAGE) || 'en';
}

export function setCurrentLanguage(langCode) {
  localStorage.setItem(KEYS.LANGUAGE, langCode);
}

export function getSavedChats() {
  try {
    const raw = localStorage.getItem(KEYS.CHATS);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      // Filter out any personal contact chats
      const officialOnly = parsed.filter(c => c.isOfficial || c.id === 'ai-bot' || c.id === 'meta-ai');
      return officialOnly.length ? officialOnly : null;
    }
    return null;
  } catch (e) {
    console.error('Failed to load saved chats', e);
    return null;
  }
}

export function saveChats(chats) {
  try {
    localStorage.setItem(KEYS.CHATS, JSON.stringify(chats));
  } catch (e) {
    console.error('Failed to save chats', e);
  }
}
