import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, Image, Pressable, ActivityIndicator } from 'react-native';
import { CheckCheck, FileText, User, CornerUpRight, Volume2, VolumeX } from 'lucide-react-native';
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';
import { styles } from '../../constants/styles';
import AudioMessage from '../AudioMessage';
import { HospitalCard } from '../HospitalCard';
import { SchemeCard } from '../SchemeCard';
import { FormattedMarkdownText } from './FormattedMarkdownText';
import { TtsPlayerButton } from '../TtsPlayerButton';

export const ChatMessageBubble = ({ 

  msg, 
  isMe, 
  onButtonPress, 
  onBookDoctor,
  onLongPressMessage
}) => {
  return (
    <View
      style={[
        styles.msgRow,
        isMe ? styles.msgRowRight : styles.msgRowLeft,
        (msg.carouselItems || msg.hospitalCarouselItems || msg.schemeCarouselItems) ? { flexDirection: 'column', alignItems: 'flex-start' } : null
      ]}
    >
      <Pressable
        onLongPress={() => onLongPressMessage && onLongPressMessage(msg)}
        delayLongPress={250}
        style={({ pressed }) => [
          styles.bubble,
          isMe ? styles.bubbleMe : styles.bubbleOther,
          pressed ? { opacity: 0.85 } : null
        ]}
      >
        {msg.isForwarded && (
          <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 4 }}>
            <CornerUpRight size={12} color="#667781" style={{ marginRight: 4 }} />
            <Text style={{ fontSize: 11, color: '#667781', fontStyle: 'italic', fontWeight: '500' }}>Forwarded</Text>
          </View>
        )}

        {msg.type === 'image' && (
          <Image source={{ uri: msg.uri }} style={styles.bubbleImage} />
        )}
        {msg.type === 'document' && (
          <View style={styles.documentContainer}>
            <View style={styles.documentIconBox}>
              <FileText size={20} color="#fff" />
            </View>
            <Text style={styles.documentName} numberOfLines={1}>{msg.name}</Text>
          </View>
        )}
        {msg.type === 'audio' && <AudioMessage uri={msg.uri} />}

        {msg.type === 'ticket' && msg.ticketData && (
          <View style={styles.ticketContainer}>
            <View style={styles.ticketHeader}>
              <Text style={styles.ticketTitle}>Appointment Confirmed</Text>
              <View style={styles.ticketBadge}>
                <Text style={styles.ticketBadgeText}>FREE</Text>
              </View>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>Doctor:</Text>
              <Text style={styles.ticketValue}>{msg.ticketData.doctorName}</Text>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>Specialty:</Text>
              <Text style={styles.ticketValue}>{msg.ticketData.specialty}</Text>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>Date:</Text>
              <Text style={styles.ticketValue}>{msg.ticketData.date}</Text>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>Time:</Text>
              <Text style={styles.ticketValue}>{msg.ticketData.time}</Text>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>ABHA Token:</Text>
              <Text style={[styles.ticketValue, { fontWeight: '600', color: '#128C7E' }]}>ABHA-9182-4412-0091</Text>
            </View>
            <View style={styles.ticketRow}>
              <Text style={styles.ticketLabel}>Status:</Text>
              <Text style={[styles.ticketValue, { color: '#00A884' }]}>Confirmed (Token Generated)</Text>
            </View>
          </View>
        )}

        {msg.text ? (
          <FormattedMarkdownText text={msg.text} style={styles.bubbleText} selectable={true} />
        ) : null}
        
        {msg.buttons && (
          <View style={styles.actionButtonsContainer}>
            {msg.buttons.map((btn, i) => (
              <TouchableOpacity
                key={i}
                style={styles.actionButton}
                onPress={() => onButtonPress(btn)}
              >
                <Text style={styles.actionButtonText}>{btn}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
        
        <View style={styles.bubbleFooter}>
          {!isMe && msg.text ? (
            <TtsPlayerButton text={msg.text} langTag={msg.langTag} />
          ) : null}
          <Text style={styles.bubbleTime}>{msg.time}</Text>
          {isMe && <CheckCheck size={14} color="#53bdeb" style={styles.checkIcon} />}
        </View>
      </Pressable>

      {/* Carousels attached to the message */}
      {msg.hospitalCarouselItems && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.carouselContainer}
        >
          {msg.hospitalCarouselItems.map((hosp, index) => (
            <HospitalCard key={hosp.id || `hosp-${index}`} hospital={hosp} />
          ))}
        </ScrollView>
      )}

      {msg.carouselItems && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.carouselContainer}
        >
          {msg.carouselItems.map((doc) => (
            <View key={doc.id} style={styles.doctorCard}>
              <View style={[styles.doctorImage, { justifyContent: 'center', alignItems: 'center' }]}>
                <User size={30} color="#8696a0" />
              </View>
              <Text style={styles.doctorName}>{doc.name}</Text>
              <Text style={styles.doctorSpecialty}>{doc.specialty}</Text>
              <Text style={styles.doctorSub}>{doc.experience}</Text>
              <Text style={styles.doctorRating}>{doc.rating}</Text>
              <Text style={styles.doctorSub}>{doc.fees}</Text>
              <TouchableOpacity
                style={styles.bookDocButton}
                onPress={() => onBookDoctor(doc)}
              >
                <Text style={styles.bookDocButtonText}>Book Free Call</Text>
              </TouchableOpacity>
            </View>
          ))}
        </ScrollView>
      )}

      {msg.schemeCarouselItems && (
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.carouselContainer}
        >
          {msg.schemeCarouselItems.map((scheme, index) => (
            <SchemeCard key={scheme.id || `scheme-${index}`} scheme={scheme} />
          ))}
        </ScrollView>
      )}
    </View>
  );
};


