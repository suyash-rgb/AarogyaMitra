import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { Play, Pause, Mic } from 'lucide-react-native';
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';
import { useStyles } from '../constants/styles';
import { useTheme } from '../context/ThemeContext';

const AudioMessage = ({ uri }) => {
  const styles = useStyles();
  const { colors } = useTheme();
  const player = useAudioPlayer(uri);
  const status = useAudioPlayerStatus(player);

  const togglePlayback = () => {
    if (status.playing) {
      player.pause();
    } else {
      if (status.currentTime >= status.duration && status.duration > 0) {
        player.seekTo(0);
      }
      player.play();
    }
  };

  const formatTime = (seconds) => {
    if (!seconds) return '0:00';
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
  };

  const progressPercent = status.duration && status.currentTime
    ? (status.currentTime / status.duration) * 100
    : 0;

  return (
    <View style={styles.audioContainer}>
      <TouchableOpacity onPress={togglePlayback} style={styles.audioPlayButton}>
        {status.playing ? <Pause size={24} color={colors.accent} /> : <Play size={24} color={colors.accent} />}
      </TouchableOpacity>
      
      <View style={styles.audioProgressTrack}>
        <View style={[styles.audioProgressBar, { width: `${progressPercent}%` }]} />
        <View style={[styles.audioProgressDot, { left: `${progressPercent}%` }]} />
      </View>
      
      <Text style={styles.audioDuration}>
        {formatTime(status.currentTime || status.duration)}
      </Text>
      
      <Mic size={16} color={colors.accent} style={{ marginLeft: 6 }} />
    </View>
  );
};

export default AudioMessage;
