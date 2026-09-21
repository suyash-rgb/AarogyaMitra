import React from 'react';
import { View, Text, TouchableOpacity, Modal, TouchableWithoutFeedback } from 'react-native';
import { useTheme } from '../context/ThemeContext';

export default function ThemePickerModal({ onClose }) {
  const { themePreference, changeThemePreference, colors } = useTheme();

  const handleSelect = (pref) => {
    changeThemePreference(pref);
    onClose();
  };

  return (
    <Modal visible transparent animationType="fade" onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center' }}>
          <TouchableWithoutFeedback>
            <View style={{ backgroundColor: colors.surface, width: '80%', borderRadius: 8, padding: 24, elevation: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.25, shadowRadius: 4 }}>
              <Text style={{ fontSize: 20, color: colors.text, fontWeight: 'bold', marginBottom: 16 }}>Choose theme</Text>
              
              <RadioOption label="System default" selected={themePreference === 'system'} onPress={() => handleSelect('system')} colors={colors} />
              <RadioOption label="Light" selected={themePreference === 'light'} onPress={() => handleSelect('light')} colors={colors} />
              <RadioOption label="Dark" selected={themePreference === 'dark'} onPress={() => handleSelect('dark')} colors={colors} />

              <View style={{ flexDirection: 'row', justifyContent: 'flex-end', marginTop: 16 }}>
                <TouchableOpacity onPress={onClose}>
                  <Text style={{ color: colors.accent, fontWeight: 'bold', fontSize: 16 }}>CANCEL</Text>
                </TouchableOpacity>
              </View>
            </View>
          </TouchableWithoutFeedback>
        </View>
      </TouchableWithoutFeedback>
    </Modal>
  );
}

const RadioOption = ({ label, selected, onPress, colors }) => {
  return (
    <TouchableOpacity style={{ flexDirection: 'row', alignItems: 'center', paddingVertical: 12 }} onPress={onPress}>
      <View style={{ width: 20, height: 20, borderRadius: 10, borderWidth: 2, borderColor: selected ? colors.accent : colors.textSecondary, justifyContent: 'center', alignItems: 'center', marginRight: 16 }}>
        {selected && <View style={{ width: 10, height: 10, borderRadius: 5, backgroundColor: colors.accent }} />}
      </View>
      <Text style={{ fontSize: 16, color: colors.text }}>{label}</Text>
    </TouchableOpacity>
  );
};
