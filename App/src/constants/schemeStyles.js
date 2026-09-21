import { StyleSheet } from 'react-native';
import { useTheme } from '../context/ThemeContext';
import { lightColors, darkColors } from './theme';
import { useMemo } from 'react';

export const useSchemeCardStyles = () => {
  const { activeTheme } = useTheme();
  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return useMemo(() => {
    return StyleSheet.create({
      card: {
        width: 280,
        backgroundColor: activeTheme === 'dark' ? '#2A2210' : '#FFFDF0', // Slight gold/yellow tint
        borderRadius: 12,
        marginRight: 12,
        marginVertical: 4,
        elevation: 3,
        shadowColor: '#B8860B', // Golden shadow
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.15,
        shadowRadius: 4,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: activeTheme === 'dark' ? '#4A3B18' : '#E6D3A3',
      },
      header: {
        padding: 12,
        backgroundColor: activeTheme === 'dark' ? '#3B2F10' : '#FFF8E1',
        borderBottomWidth: 1,
        borderBottomColor: activeTheme === 'dark' ? '#4A3B18' : '#E6D3A3',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
      },
      title: {
        fontSize: 16,
        fontWeight: 'bold',
        color: activeTheme === 'dark' ? '#FFD700' : '#8B6508',
        flex: 1,
        marginRight: 8,
      },
      badge: {
        backgroundColor: '#FFD700',
        paddingHorizontal: 6,
        paddingVertical: 2,
        borderRadius: 4,
      },
      badgeText: {
        color: '#8B6508',
        fontSize: 10,
        fontWeight: 'bold',
      },
      content: {
        padding: 12,
      },
      department: {
        fontSize: 12,
        color: activeTheme === 'dark' ? '#B0B0B0' : '#666',
        fontWeight: '600',
        marginBottom: 6,
      },
      description: {
        fontSize: 13,
        color: colors.text,
        marginBottom: 8,
        lineHeight: 18,
      },
      sectionTitle: {
        fontSize: 13,
        fontWeight: 'bold',
        color: colors.textSecondary,
        marginTop: 8,
        marginBottom: 2,
      },
      sectionText: {
        fontSize: 12,
        color: colors.text,
        lineHeight: 16,
      },
    });
  }, [colors, activeTheme]);
};
