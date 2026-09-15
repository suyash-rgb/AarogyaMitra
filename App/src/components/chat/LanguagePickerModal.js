import React from 'react';
import { View, Text, TouchableOpacity, Modal, ScrollView } from 'react-native';
import { X } from 'lucide-react-native';
import { styles } from '../../constants/styles';

const languages = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिंदी' },
  { code: 'bho', name: 'Bhojpuri', native: 'भोजपुरी' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'as', name: 'Assamese', native: 'অসমীয়া' },
  { code: 'brx', name: 'Bodo', native: 'बड़ो' },
  { code: 'doi', name: 'Dogri', native: 'डोगरी' },
  { code: 'ks', name: 'Kashmiri', native: 'कॉशुर' },
  { code: 'gom', name: 'Konkani', native: 'कोंकणी' },
  { code: 'mai', name: 'Maithili', native: 'मैथिली' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'mni', name: 'Manipuri', native: 'মৈতৈলোন্' },
  { code: 'ne', name: 'Nepali', native: 'नेपाली' },
  { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
  { code: 'sa', name: 'Sanskrit', native: 'संस्कृतम्' },
  { code: 'sat', name: 'Santali', native: 'ᱥᱟᱱᱛᱟᱲᱤ' },
  { code: 'sd', name: 'Sindhi', native: 'سنڌي' },
  { code: 'ur', name: 'Urdu', native: 'اردو' }
];

export const LanguagePickerModal = ({ visible, onClose, currentLanguage, onSelectLanguage }) => {
  return (
    <Modal
      visible={visible}
      transparent={true}
      animationType="slide"
      onRequestClose={onClose}
    >
      <TouchableOpacity
        style={styles.modalOverlay}
        activeOpacity={1}
        onPress={onClose}
      >
        <View style={styles.modalContentContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Select Language / भाषा चुनें</Text>
            <TouchableOpacity onPress={onClose}>
              <X size={24} color="#111B21" />
            </TouchableOpacity>
          </View>
          <ScrollView style={styles.langList}>
            {languages.map((lang) => (
              <TouchableOpacity
                key={lang.code}
                style={[
                  styles.langOption,
                  currentLanguage === lang.code ? styles.langOptionActive : null
                ]}
                onPress={() => onSelectLanguage(lang.code)}
              >
                <Text style={styles.langOptionText}>{lang.name}</Text>
                <Text style={styles.langOptionNative}>{lang.native}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};
