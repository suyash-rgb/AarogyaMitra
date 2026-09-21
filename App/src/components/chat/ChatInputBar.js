import React from 'react';
import { View, TextInput, TouchableOpacity } from 'react-native';
import { Smile, Paperclip, Camera, Mic, Send } from 'lucide-react-native';
import { useStyles } from '../../constants/styles';
import { useTheme } from '../../context/ThemeContext';
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
  const styles = useStyles();
  const { colors } = useTheme();

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
              <Smile size={24} color={colors.textSecondary} />
            </TouchableOpacity>

            <TextInput
              placeholder="Type a message"
              placeholderTextColor={colors.textSecondary}
              style={styles.chatTextInput}
              value={inputText}
              onChangeText={setInputText}
              onSubmitEditing={handleSendMessage}
            />

            <TouchableOpacity style={styles.inputIconButton} onPress={handleAttachment}>
              <Paperclip size={24} color={colors.textSecondary} />
            </TouchableOpacity>
            <TouchableOpacity style={styles.inputIconButton} onPress={handleCamera}>
              <Camera size={24} color={colors.textSecondary} />
            </TouchableOpacity>
          </View>

          <TouchableOpacity style={styles.micButton} onPress={inputText.trim() ? handleSendMessage : () => setIsRecording(true)}>
            <View style={styles.micCircle}>
              {inputText.trim() ? (
                <Send size={24} color={colors.textInverse} />
              ) : (
                <Mic size={24} color={colors.textInverse} />
              )}
            </View>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
};
