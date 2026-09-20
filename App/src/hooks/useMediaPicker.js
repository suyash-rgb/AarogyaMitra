import { useState } from 'react';
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';

export function useMediaPicker({ setMessages }) {
  const [isRecording, setIsRecording] = useState(false);

  const sendMediaMessage = (mediaData) => {
    const newMsg = {
      id: Date.now().toString(),
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      ...mediaData
    };
    setMessages(prev => [...prev, newMsg]);
  };

  const handleAttachment = async () => {
    try {
      const file = await DocumentPicker.getDocumentAsync({
        type: ['image/*', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'],
        copyToCacheDirectory: true
      });

      if (file.type === 'success' || !file.canceled) {
        const isImage = file.mimeType?.startsWith('image/') || file.name?.match(/\.(jpeg|jpg|gif|png)$/i);
        if (isImage) {
          sendMediaMessage({ type: 'image', uri: file.uri });
        } else {
          sendMediaMessage({ type: 'document', name: file.name, uri: file.uri });
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleCamera = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (!permissionResult.granted) {
      alert("Camera permission is required!");
      return;
    }
    const result = await ImagePicker.launchCameraAsync({
      mediaTypes: ['images'],
      quality: 0.5,
    });
    if (!result.canceled && result.assets && result.assets.length > 0) {
      sendMediaMessage({ type: 'image', uri: result.assets[0].uri });
    }
  };

  return {
    isRecording,
    setIsRecording,
    handleAttachment,
    handleCamera,
    sendMediaMessage
  };
}
