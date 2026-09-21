import { getOrCreateDeviceId } from './userSession';

const BASE_URL = process.env.EXPO_PUBLIC_API_URL || "http://10.228.232.83:8080/api/v1";

const sendLogToBackend = async (level, args) => {
  try {
    const message = args.map(arg => {
      if (typeof arg === 'object') {
        try {
          // Attempt to extract useful info from error objects
          if (arg instanceof Error) {
            return `${arg.message}\n${arg.stack}`;
          }
          return JSON.stringify(arg, null, 2);
        } catch (e) {
          return String(arg);
        }
      }
      return String(arg);
    }).join(" ");

    const deviceId = await getOrCreateDeviceId();
    const BACKEND_URL = `${BASE_URL}/logs/?deviceId=${encodeURIComponent(deviceId)}`;

    await fetch(BACKEND_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        level: level,
        message: message,
        timestamp: new Date().toISOString(),
        source: "ReactNativeApp",
      }),
    });
  } catch (error) {
    // Silently fail if logging fails to prevent infinite loops
  }
};

export const setupGlobalLogging = () => {
  const originalConsoleLog = console.log;
  const originalConsoleWarn = console.warn;
  const originalConsoleError = console.error;

  console.log = (...args) => {
    originalConsoleLog(...args);
    sendLogToBackend('info', args);
  };

  console.warn = (...args) => {
    originalConsoleWarn(...args);
    sendLogToBackend('warn', args);
  };

  console.error = (...args) => {
    originalConsoleError(...args);
    sendLogToBackend('error', args);
  };
};
