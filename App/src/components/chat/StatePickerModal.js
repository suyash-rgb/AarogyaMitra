import React from 'react';
import { View, Text, TouchableOpacity, Modal, ScrollView } from 'react-native';
import { X } from 'lucide-react-native';
import { styles } from '../../constants/styles';

const fallbackStates = [
  'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 
  'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala', 
  'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 
  'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 
  'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 
  'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Jammu and Kashmir', 
  'Ladakh', 'Lakshadweep', 'Puducherry'
];

export const StatePickerModal = ({ visible, onClose, availableStates, userState, onSelectState }) => {
  const displayStates = availableStates.length > 0 ? availableStates : fallbackStates;

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
            <Text style={styles.modalTitle}>Select Your State</Text>
            <TouchableOpacity onPress={onClose}>
              <X size={24} color="#111B21" />
            </TouchableOpacity>
          </View>
          <ScrollView style={styles.langList}>
            {displayStates.map((stateName) => (
              <TouchableOpacity
                key={stateName}
                style={[
                  styles.langOption,
                  userState === stateName ? styles.langOptionActive : null
                ]}
                onPress={() => onSelectState(stateName)}
              >
                <Text style={styles.langOptionText}>{stateName}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      </TouchableOpacity>
    </Modal>
  );
};
