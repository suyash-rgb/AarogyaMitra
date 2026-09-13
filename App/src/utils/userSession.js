import AsyncStorage from '@react-native-async-storage/async-storage';

const DEVICE_ID_KEY = '@arogya_device_id';

/**
 * Generates a simple RFC4122 v4 compliant UUID in pure JS
 */
const generateUUID = () => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
};

/**
 * Gets or creates a unique persistent Device ID for this installation.
 */
export const getOrCreateDeviceId = async () => {
  try {
    let deviceId = await AsyncStorage.getItem(DEVICE_ID_KEY);
    if (!deviceId) {
      deviceId = generateUUID();
      await AsyncStorage.setItem(DEVICE_ID_KEY, deviceId);
    }
    return deviceId;
  } catch (error) {
    console.error('Error with AsyncStorage device ID:', error);
    // Fallback in case storage is restricted
    if (typeof window !== 'undefined' && window.localStorage) {
      let deviceId = window.localStorage.getItem(DEVICE_ID_KEY);
      if (!deviceId) {
        deviceId = generateUUID();
        window.localStorage.setItem(DEVICE_ID_KEY, deviceId);
      }
      return deviceId;
    }
    return 'fallback-' + generateUUID().substring(0, 8);
  }
};

/**
 * Deterministic string hash function
 */
export const hashString = (str) => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = (hash << 5) - hash + str.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash);
};

/**
 * Deterministically assigns a unique avatar and dummy chat setup per device
 */
export const getUserPersona = async () => {
  const deviceId = await getOrCreateDeviceId();
  const hash = hashString(deviceId);

  // Dynamic Avatar URL using Pravatar seed
  const avatarUrl = `https://i.pravatar.cc/150?img=${(hash % 70) + 1}`;

  // Pre-configured persona presets for different testing scenarios
  const dummyChatPresets = [
    {
      id: 'persona_chw',
      testerRole: 'Community Health Worker (CHW)',
      testerName: 'Anita Sharma',
      avatarUrl: avatarUrl,
      presetChats: [
        {
          id: 'ai-bot',
          name: 'ArogyaMitra AI Bot',
          avatar: null,
          isOfficial: true,
          status: 'Online • Official Healthcare Assistant',
          unreadCount: 1,
          messages: [
            {
              id: 'init-1',
              text: 'Namaste Anita! Welcome to ArogyaMitra CHW Portal.',
              sender: 'other',
              time: '09:00 AM'
            }
          ]
        },
        {
          id: 'dr-verma',
          name: 'Dr. Verma (PHC Dhar)',
          avatar: null,
          isOfficial: false,
          status: 'Online',
          unreadCount: 2,
          messages: [
            {
              id: 'dv-1',
              text: 'Please review the maternal health checklist for Ward 4.',
              sender: 'other',
              time: '08:45 AM'
            }
          ]
        }
      ]
    },
    {
      id: 'persona_emergency',
      testerRole: 'Rural Patient / Emergency Contact',
      testerName: 'Rajesh Kumar',
      avatarUrl: avatarUrl,
      presetChats: [
        {
          id: 'ai-bot',
          name: 'ArogyaMitra AI Bot',
          avatar: null,
          isOfficial: true,
          status: 'Online • Emergency & Hospital Finder',
          unreadCount: 1,
          messages: [
            {
              id: 'init-1',
              text: 'Namaste Rajesh! Tap "Locate a Healthcare Facility" to find nearby government hospitals.',
              sender: 'other',
              time: '09:00 AM'
            }
          ]
        },
        {
          id: '104-helpline',
          name: '104 Health Helpline',
          avatar: null,
          isOfficial: true,
          status: 'Available 24x7',
          unreadCount: 0,
          messages: [
            {
              id: 'hh-1',
              text: 'Toll-free 104 medical consultation active.',
              sender: 'other',
              time: 'Yesterday'
            }
          ]
        }
      ]
    }
  ];

  const selectedPreset = dummyChatPresets[hash % dummyChatPresets.length];
  return {
    deviceId,
    shortId: deviceId.substring(0, 8),
    ...selectedPreset
  };
};
