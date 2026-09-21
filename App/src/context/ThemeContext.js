import React, { createContext, useState, useEffect, useContext } from 'react';
import { Appearance } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { lightColors, darkColors } from '../constants/theme';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [themePreference, setThemePreference] = useState('system'); // 'light', 'dark', 'system'
  const [activeTheme, setActiveTheme] = useState('light'); // 'light' or 'dark'

  useEffect(() => {
    // Load preference from AsyncStorage
    const loadTheme = async () => {
      try {
        const stored = await AsyncStorage.getItem('@theme_preference');
        if (stored) {
          setThemePreference(stored);
        }
      } catch (err) {
        console.warn('Failed to load theme preference', err);
      }
    };
    loadTheme();
  }, []);

  useEffect(() => {
    // Determine active theme based on preference and system
    if (themePreference === 'system') {
      const colorScheme = Appearance.getColorScheme();
      setActiveTheme(colorScheme === 'dark' ? 'dark' : 'light');
    } else {
      setActiveTheme(themePreference);
    }
  }, [themePreference]);

  useEffect(() => {
    // Listener for system theme changes if preference is 'system'
    const subscription = Appearance.addChangeListener(({ colorScheme }) => {
      if (themePreference === 'system') {
        setActiveTheme(colorScheme === 'dark' ? 'dark' : 'light');
      }
    });
    return () => subscription.remove();
  }, [themePreference]);

  const changeThemePreference = async (newPref) => {
    setThemePreference(newPref);
    try {
      await AsyncStorage.setItem('@theme_preference', newPref);
    } catch (err) {
      console.warn('Failed to save theme preference', err);
    }
  };

  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return (
    <ThemeContext.Provider value={{ themePreference, activeTheme, changeThemePreference, colors }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
