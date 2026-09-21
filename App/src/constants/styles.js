import { StyleSheet, Platform, StatusBar } from 'react-native';

import { useTheme } from '../context/ThemeContext';
import { lightColors, darkColors } from './theme';
import { useMemo } from 'react';

export const useStyles = () => {
  const { activeTheme } = useTheme();
  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return useMemo(() => {
    return StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.headerBg, // Matches iOS status bar area
  },
  keyboardView: {
    flex: 1,
  },
  header: {
    height: 60,
    backgroundColor: colors.headerBg,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    justifyContent: 'space-between',
    elevation: 4,
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    zIndex: 10,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  backButton: {
    padding: 4,
    marginRight: 4,
  },
  avatarImage: {
    width: 40,
    height: 40,
    borderRadius: 20,
    marginRight: 10,
    backgroundColor: colors.surface,
    resizeMode: 'contain',
  },
  headerTitleContainer: {
    flex: 1,
    justifyContent: 'center',
  },
  headerName: {
    color: colors.textInverse,
    fontWeight: 'bold',
    fontSize: 18,
  },
  headerStatus: {
    color: colors.textInverse,
    fontSize: 13,
    opacity: 0.8,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  iconButton: {
    padding: 10,
    marginLeft: 4,
  },
  chatAreaWrapper: {
    flex: 1,
    position: 'relative',
  },
  chatBackground: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: colors.background, // WhatsApp classic light background
  },
  messageArea: {
    flex: 1,
  },
  messageAreaContent: {
    paddingHorizontal: 12,
    paddingVertical: 16,
    paddingBottom: 20,
  },
  msgRow: {
    flexDirection: 'row',
    marginVertical: 4,
    width: '100%',
  },
  msgRowLeft: {
    justifyContent: 'flex-start',
  },
  msgRowRight: {
    justifyContent: 'flex-end',
  },
  bubble: {
    maxWidth: '80%',
    borderRadius: 12,
    paddingHorizontal: 10,
    paddingVertical: 6,
    position: 'relative',
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 1,
    elevation: 1,
  },
  bubbleMe: {
    backgroundColor: colors.bubbleMe,
    borderTopRightRadius: 0,
  },
  bubbleOther: {
    backgroundColor: colors.surface,
    borderTopLeftRadius: 0,
  },
  bubbleText: {
    color: colors.text,
    fontSize: 15,
    lineHeight: 20,
  },
  bubbleFooter: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    alignItems: 'center',
    marginTop: 2,
  },
  bubbleTime: {
    color: colors.textSecondary,
    fontSize: 11,
    marginRight: 4,
  },
  checkIcon: {
    marginLeft: 2,
  },
  typingBubble: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  typingText: {
    color: colors.textSecondary,
    fontSize: 14,
    marginLeft: 8,
    fontStyle: 'italic',
  },
  bubbleImage: {
    width: 240,
    height: 240,
    borderRadius: 8,
    marginBottom: 4,
  },
  documentContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.border,
    padding: 8,
    borderRadius: 8,
    marginBottom: 4,
  },
  documentIconBox: {
    width: 40,
    height: 40,
    backgroundColor: '#FF5722',
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  documentName: {
    flex: 1,
    fontSize: 14,
    color: colors.text,
    fontWeight: '500'
  },
  audioContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    width: 220,
    paddingVertical: 6,
  },
  audioPlayButton: {
    marginRight: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  audioProgressTrack: {
    flex: 1,
    height: 4,
    backgroundColor: colors.border,
    borderRadius: 2,
    marginRight: 10,
    position: 'relative',
    justifyContent: 'center',
  },
  audioProgressBar: {
    height: 4,
    backgroundColor: colors.accent,
    borderRadius: 2,
  },
  audioProgressDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.accent,
    position: 'absolute',
    marginLeft: -6,
  },
  audioDuration: {
    fontSize: 12,
    color: colors.textSecondary,
    minWidth: 36,
    textAlign: 'right',
  },
  inputBar: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    paddingHorizontal: 8,
    paddingVertical: 8,
    backgroundColor: colors.background, // Match chat background to look transparent
  },
  inputContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'flex-end',
    backgroundColor: colors.surface,
    borderRadius: 24,
    minHeight: 48,
    marginRight: 8,
    paddingHorizontal: 4,
  },
  inputIconButton: {
    padding: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  recordingPill: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: 24,
    minHeight: 48,
    marginRight: 8,
    paddingHorizontal: 16,
  },
  redDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.error,
    marginRight: 6,
  },
  recordingTimerText: {
    fontSize: 16,
    color: colors.error,
    fontWeight: '600',
    fontVariant: ['tabular-nums'],
  },
  waveformContainer: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 8,
  },
  waveformBar: {
    width: 2.5,
    backgroundColor: colors.textSecondary,
    marginHorizontal: 1.5,
    borderRadius: 1.5,
  },
  trashCircleButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.doctorBg,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
  },
  sendCircleButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.accent,
    justifyContent: 'center',
    alignItems: 'center',
  },
  pauseIconButton: {
    padding: 8,
    marginLeft: 6,
  },
  chatTextInput: {
    flex: 1,
    fontSize: 16,
    color: colors.text,
    paddingTop: 12,
    paddingBottom: 12,
    maxHeight: 120,
  },
  micButton: {
    justifyContent: 'flex-end',
    paddingBottom: 2,
  },
  micCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: colors.headerBg, // WhatsApp Green Button
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  // --- Chat List Styles ---
  homeHeader: {
    height: 60,
    backgroundColor: colors.headerBg,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
  },
  homeTitle: {
    color: colors.textInverse,
    fontSize: 20,
    fontWeight: 'bold',
  },
  homeIcons: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  homeTabs: {
    flexDirection: 'row',
    backgroundColor: colors.headerBg,
  },
  tabItem: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
  },
  activeTab: {
    borderBottomWidth: 3,
    borderBottomColor: colors.surface,
  },
  tabText: {
    color: colors.textSecondary,
    fontSize: 15,
    fontWeight: 'bold',
  },
  activeTabText: {
    color: colors.textInverse,
    fontSize: 15,
    fontWeight: 'bold',
  },
  chatListContainer: {
    backgroundColor: colors.surface,
  },
  chatListItem: {
    flexDirection: 'row',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  chatListAvatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 16,
    backgroundColor: colors.surface,
    resizeMode: 'contain',
    borderWidth: 1,
    borderColor: colors.border,
  },
  chatListDetails: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  chatListHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  chatListName: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  chatListTime: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  chatListLastMessage: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  unreadBadge: {
    backgroundColor: colors.accent,
    borderRadius: 10,
    minWidth: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 4,
    paddingHorizontal: 4,
  },
  unreadBadgeText: {
    color: colors.textInverse,
    fontSize: 10,
    fontWeight: 'bold',
  },
  actionButtonsContainer: {
    marginTop: 8,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    paddingTop: 4,
    minWidth: 200,
  },
  actionButton: {
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    alignItems: 'center',
  },
  actionButtonText: {
    color: colors.buttonText,
    fontSize: 15,
    fontWeight: '500',
  },
  // --- Doctor Carousel Styles ---
  carouselContainer: {
    marginVertical: 8,
    paddingRight: 10,
  },
  doctorCard: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    padding: 12,
    marginRight: 12,
    width: 200,
    alignItems: 'center',
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  doctorImage: {
    width: 60,
    height: 60,
    borderRadius: 30,
    marginBottom: 8,
    backgroundColor: colors.doctorBg,
  },
  doctorName: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.text,
    textAlign: 'center',
  },
  doctorSpecialty: {
    fontSize: 12,
    color: colors.accent, // Green highlight for specialty
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 2,
  },
  doctorSub: {
    fontSize: 11,
    color: colors.textSecondary,
    textAlign: 'center',
    marginTop: 2,
  },
  doctorRating: {
    fontSize: 12,
    color: colors.accent,
    fontWeight: 'bold',
    marginTop: 4,
  },
  bookDocButton: {
    backgroundColor: colors.accent,
    borderRadius: 16,
    paddingVertical: 6,
    paddingHorizontal: 20,
    marginTop: 10,
    width: '100%',
    alignItems: 'center',
  },
  bookDocButtonText: {
    color: colors.textInverse,
    fontSize: 13,
    fontWeight: 'bold',
  },
  // --- Booking Ticket Styles ---
  ticketContainer: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.accent,
    padding: 12,
    width: 240,
    marginVertical: 4,
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  ticketHeader: {
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
    paddingBottom: 6,
    marginBottom: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  ticketTitle: {
    fontSize: 13,
    fontWeight: 'bold',
    color: colors.accent,
  },
  ticketBadge: {
    backgroundColor: colors.accentLight,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  ticketBadgeText: {
    color: colors.accent,
    fontSize: 10,
    fontWeight: 'bold',
  },
  ticketRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginVertical: 3,
  },
  ticketLabel: {
    fontSize: 12,
    color: colors.textSecondary,
  },
  ticketValue: {
    fontSize: 12,
    fontWeight: 'bold',
    color: colors.text,
  },
  // --- Language Selector Modal Styles ---
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
    justifyContent: 'flex-end',
  },
  modalContentContainer: {
    backgroundColor: colors.surface,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: Platform.OS === 'ios' ? 34 : 24, // extra padding for iOS home indicator
    maxHeight: '60%',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: colors.doctorBg,
    paddingBottom: 12,
    marginBottom: 8,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.text,
  },
  langList: {
    marginVertical: 8,
  },
  langOption: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 14,
    borderBottomWidth: 1,
    borderBottomColor: colors.doctorBg,
  },
  langOptionActive: {
    backgroundColor: colors.accentLight,
    borderRadius: 8,
    paddingHorizontal: 8,
  },
  langOptionText: {
    fontSize: 16,
    color: colors.text,
  },
  langOptionNative: {
    fontSize: 15,
    color: colors.textSecondary,
    fontWeight: '500',
  },
        });
  }, [colors]);
};

export const useHospitalCardStyles = () => {
  const { activeTheme } = useTheme();
  const colors = activeTheme === 'dark' ? darkColors : lightColors;

  return useMemo(() => {
    return StyleSheet.create({
  card: {
    width: 270,
    backgroundColor: colors.surface,
    borderRadius: 12,
    marginRight: 12,
    marginVertical: 4,
    elevation: 3,
    shadowColor: colors.text,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.border,
  },
  previewContainer: {
    width: '100%',
    height: 120,
    position: 'relative',
    backgroundColor: colors.doctorBg,
  },
  mapImage: {
    width: '100%',
    height: '100%',
  },
  badge: {
    position: 'absolute',
    top: 8,
    right: 8,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  badgeTrauma: {
    backgroundColor: colors.dangerBadge,
  },
  badgeFacility: {
    backgroundColor: colors.facilityBadge,
  },
  badgeText: {
    color: colors.textInverse,
    fontSize: 10,
    fontWeight: 'bold',
    letterSpacing: 0.5,
  },
  content: {
    padding: 12,
  },
  title: {
    fontSize: 15,
    fontWeight: '700',
    color: colors.text,
    marginBottom: 2,
  },
  subtitle: {
    fontSize: 12,
    color: colors.textSecondary,
    fontWeight: '500',
    marginBottom: 4,
  },
  services: {
    fontSize: 11,
    color: colors.textSecondary,
    marginBottom: 10,
  },
  actionButton: {
    backgroundColor: colors.accent,
    paddingVertical: 9,
    paddingHorizontal: 12,
    borderRadius: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 4,
  },
  buttonText: {
    color: colors.textInverse,
    fontWeight: '600',
    fontSize: 13,
  },
    });
  }, [colors]);
};
