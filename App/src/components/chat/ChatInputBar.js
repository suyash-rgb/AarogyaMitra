import React from 'react';
import { View, TextInput, TouchableOpacity } from 'react-native';
import { Smile, Paperclip, Camera, Mic } from 'lucide-react-native';
import { styles } from '../../constants/styles';
import RecordingBar from '../RecordingBar';

export const ChatInputBar = ({ 
  isRecording, 
  setIsRecording, 
  inputText, 
  setInputText, 
  handleSendMessage, 
  handleAttachment, 
  handleCamera,
  onRecordSend 
}) => {
  return (
    <View style={styles.inputBar}>
      {isRecording ? (
        <RecordingBar
          onSend={onRecordSend}
          onCancel={() => setIsRecording(false)}
        />
      ) : (
        <>
          <View style={styles.inputContainer}>
            <TouchableOpacity style={styles.inputIconButton}>
              <Smile size={24} color="#8696a0" />
            </TouchableOpacity>

            <TextInput
              placeholder="Type a message"
              placeholderTextColor="#8696a0"
              style={styles.chatTextInput}
              value={inputText}
              onChangeText={setInputText}
              onSubmitEditing={handleSendMessage}
            />

            <TouchableOpacity style={styles.inputIconButton} onPress={handleAttachment}>
              <Paperclip size={24} color="#8696a0" />
            </TouchableOpacity>
            <TouchableOpacity style={styles.inputIconButton} onPress={handleCamera}>
              <Camera size={24} color="#8696a0" />
            </TouchableOpacity>
          </View>

          <TouchableOpacity style={styles.micButton} onPress={inputText.trim() ? handleSendMessage : () => setIsRecording(true)}>
            <View style={styles.micCircle}>
              <Mic size={24} color="#fff" />
            </View>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
};
