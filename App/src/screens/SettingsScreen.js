import React from 'react';
import { View, Text, TouchableOpacity, ScrollView, Image } from 'react-native';
import { ArrowLeft, Key, Lock, MessageCircle, Bell, CircleDashed, HelpCircle, Users } from 'lucide-react-native';
import { useStyles } from '../constants/styles';
import { useTheme } from '../context/ThemeContext';

export default function SettingsScreen({ goBack, openChatsSettings, userPersona }) {
  const styles = useStyles();
  const { colors } = useTheme();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <TouchableOpacity onPress={goBack} style={styles.backButton}>
            <ArrowLeft color={colors.textInverse} size={24} />
          </TouchableOpacity>
          <Text style={[styles.headerName, { marginLeft: 8 }]}>Settings</Text>
        </View>
      </View>

      <ScrollView style={{ flex: 1, backgroundColor: colors.surface }}>
        {/* Profile Section */}
        <View style={{ flexDirection: 'row', padding: 20, borderBottomWidth: 1, borderBottomColor: colors.border, alignItems: 'center' }}>
          <View style={{ width: 60, height: 60, borderRadius: 30, backgroundColor: colors.border, justifyContent: 'center', alignItems: 'center', marginRight: 16 }}>
            <Text style={{ fontSize: 24, color: colors.text }}>👤</Text>
          </View>
          <View style={{ flex: 1 }}>
            <Text style={{ fontSize: 18, color: colors.text, fontWeight: '500' }}>
              {userPersona?.name || 'User'}
            </Text>
            <Text style={{ fontSize: 14, color: colors.textSecondary, marginTop: 4 }}>
              Busy
            </Text>
          </View>
        </View>

        {/* Settings List */}
        <SettingsItem icon={<Key color={colors.iconColor} size={24} />} title="Account" subtitle="Security notifications, change number" />
        <SettingsItem icon={<Lock color={colors.iconColor} size={24} />} title="Privacy" subtitle="Block contacts, disappearing messages" />
        <SettingsItem icon={<CircleDashed color={colors.iconColor} size={24} />} title="Avatar" subtitle="Create, edit, profile photo" />
        <SettingsItem icon={<MessageCircle color={colors.iconColor} size={24} />} title="Chats" subtitle="Theme, wallpapers, chat history" onPress={openChatsSettings} />
        <SettingsItem icon={<Bell color={colors.iconColor} size={24} />} title="Notifications" subtitle="Message, group & call tones" />
        <SettingsItem icon={<Users color={colors.iconColor} size={24} />} title="App language" subtitle="English (device's language)" />
        <SettingsItem icon={<HelpCircle color={colors.iconColor} size={24} />} title="Help" subtitle="Help center, contact us, privacy policy" />
      </ScrollView>
    </View>
  );
}

const SettingsItem = ({ icon, title, subtitle, onPress }) => {
  const { colors } = useTheme();
  return (
    <TouchableOpacity style={{ flexDirection: 'row', padding: 20, alignItems: 'center' }} onPress={onPress}>
      <View style={{ width: 40, alignItems: 'center' }}>
        {icon}
      </View>
      <View style={{ marginLeft: 16, flex: 1 }}>
        <Text style={{ fontSize: 16, color: colors.text }}>{title}</Text>
        <Text style={{ fontSize: 14, color: colors.textSecondary, marginTop: 2 }}>{subtitle}</Text>
      </View>
    </TouchableOpacity>
  );
};
