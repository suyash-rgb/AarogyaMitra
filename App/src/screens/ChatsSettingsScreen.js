import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { ArrowLeft, Sun, Image as ImageIcon } from 'lucide-react-native';
import { useStyles } from '../constants/styles';
import { useTheme } from '../context/ThemeContext';
import ThemePickerModal from '../components/ThemePickerModal';

export default function ChatsSettingsScreen({ goBack }) {
  const styles = useStyles();
  const { colors, themePreference } = useTheme();
  const [showThemeModal, setShowThemeModal] = useState(false);

  const getThemeText = () => {
    if (themePreference === 'light') return 'Light';
    if (themePreference === 'dark') return 'Dark';
    return 'System default';
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity onPress={goBack} style={styles.backButton}>
            <ArrowLeft color={colors.textInverse} size={24} />
          </TouchableOpacity>
          <Text style={[styles.headerName, { marginLeft: 8 }]}>Chats</Text>
        </View>
      </View>

      <ScrollView style={{ flex: 1, backgroundColor: colors.surface }}>
        <View style={{ padding: 20, paddingBottom: 10 }}>
          <Text style={{ color: colors.textSecondary, fontWeight: 'bold' }}>Display</Text>
        </View>

        <TouchableOpacity style={{ flexDirection: 'row', padding: 20, alignItems: 'center' }} onPress={() => setShowThemeModal(true)}>
          <View style={{ width: 40, alignItems: 'center' }}>
            <Sun color={colors.iconColor} size={24} />
          </View>
          <View style={{ marginLeft: 16, flex: 1 }}>
            <Text style={{ fontSize: 16, color: colors.text }}>Theme</Text>
            <Text style={{ fontSize: 14, color: colors.textSecondary, marginTop: 2 }}>{getThemeText()}</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={{ flexDirection: 'row', padding: 20, alignItems: 'center' }}>
          <View style={{ width: 40, alignItems: 'center' }}>
            <ImageIcon color={colors.iconColor} size={24} />
          </View>
          <View style={{ marginLeft: 16, flex: 1 }}>
            <Text style={{ fontSize: 16, color: colors.text }}>Wallpaper</Text>
          </View>
        </TouchableOpacity>
      </ScrollView>

      {showThemeModal && (
        <ThemePickerModal onClose={() => setShowThemeModal(false)} />
      )}
    </View>
  );
}
