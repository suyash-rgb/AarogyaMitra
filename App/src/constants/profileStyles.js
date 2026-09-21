import { StyleSheet, Platform, StatusBar } from 'react-native';

import { useTheme } from '../context/ThemeContext';
import { lightColors, darkColors } from './theme';
import { useMemo } from 'react';

export const useStyles = () => {
  const { activeTheme } = useTheme();
  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return useMemo(() => {
    return StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.doctorBg, // Light grey background for spacing
  },
  header: {
    height: 60,
    backgroundColor: colors.surface,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  headerButton: {
    padding: 10,
  },
  headerTitleContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: 4,
  },
  smallAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    marginRight: 10,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    resizeMode: 'contain',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: '500',
    color: colors.text,
  },
  scrollContent: {
    flex: 1,
  },
  sectionCard: {
    backgroundColor: colors.surface,
    marginTop: 8,
    paddingVertical: 4,
  },
  heroContainer: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  heroAvatar: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
    resizeMode: 'contain',
  },
  heroNameContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
  },
  heroName: {
    fontSize: 22,
    fontWeight: '400',
    color: colors.text,
    textAlign: 'center',
  },
  heroPhone: {
    fontSize: 16,
    color: colors.textSecondary,
    marginTop: 4,
  },
  shareButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.doctorBg,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 24,
  },
  shareText: {
    fontSize: 14,
    color: colors.text,
    marginTop: 8,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  listIcon: {
    marginRight: 24,
  },
  listContent: {
    flex: 1,
    justifyContent: 'center',
  },
  listTextPrimary: {
    fontSize: 16,
    color: colors.text,
    lineHeight: 22,
  },
  listTextSecondary: {
    fontSize: 14,
    color: colors.textSecondary,
    marginTop: 2,
    lineHeight: 20,
  },
  listTextLink: {
    fontSize: 16,
    color: '#027EB5', // Light mode link color
  },
  sectionHeader: {
    fontSize: 14,
    color: colors.textSecondary,
    marginLeft: 20,
    marginTop: 16,
    marginBottom: 4,
    fontWeight: '500',
  },
  greenCircleIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.accent,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  modalBackground: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.9)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  fullScreenAvatar: {
    width: '100%',
    aspectRatio: 1,
    backgroundColor: colors.surface,
    resizeMode: 'contain',
  }
    });
  }, [colors]);
};
