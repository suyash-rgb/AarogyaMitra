import React, { useState, useEffect } from 'react';
import { TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Volume2, VolumeX } from 'lucide-react-native';
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';
import { requestTTS } from '../services/apiService';

export const TtsPlayerButton = ({ text, langTag, size = 15, color = '#8696a0', activeColor = '#00A884', style }) => {
  const [audioUri, setAudioUri] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const player = useAudioPlayer(audioUri);
  const status = useAudioPlayerStatus(player);

  useEffect(() => {
    if (audioUri && player && status.isLoaded && !status.playing && isLoading) {
      player.play();
      setIsLoading(false);
    }
  }, [audioUri, status.isLoaded]);

  useEffect(() => {
    if (status.didJustFinish || (status.currentTime > 0 && status.currentTime >= status.duration)) {
      setAudioUri(null);
    }
  }, [status.playing, status.currentTime, status.duration]);

  const handlePress = async () => {
    if (status.playing) {
      if (player) player.pause();
      setAudioUri(null);
      return;
    }

    if (isLoading) return;
    if (!text) return;

    try {
      setIsLoading(true);
      const res = await requestTTS(text, langTag || 'hin_Deva');
      if (res && res.audio_base64 && res.audio_base64 !== 'QVVESU9fRFVNTVlfREFUQQ==') {
        const uri = `data:audio/mp3;base64,${res.audio_base64}`;
        setAudioUri(uri);
      } else {
        setIsLoading(false);
        Alert.alert('TTS Unavailable', 'Could not generate speech for this text right now. Please try again later.');
      }
    } catch (err) {
      console.warn('TTS Request error:', err);
      setIsLoading(false);
      Alert.alert('TTS Request Error', 'Failed to connect to the speech synthesis service.');
    }
  };

  return (
    <TouchableOpacity 
      onPress={handlePress} 
      style={[{ marginRight: 6, padding: 2 }, style]}
      hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
    >
      {isLoading ? (
        <ActivityIndicator size="small" color={activeColor} />
      ) : status.playing ? (
        <VolumeX size={size} color={activeColor} />
      ) : (
        <Volume2 size={size} color={color} />
      )}
    </TouchableOpacity>
  );
};

