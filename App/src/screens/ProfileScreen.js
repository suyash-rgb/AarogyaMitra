import React from 'react';
import { useStyles } from '../constants/profileStyles';
import { useTheme } from '../context/ThemeContext';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Switch,
  Platform,
  StatusBar,
  Modal
} from 'react-native';
import {
  ArrowLeft,
  MoreVertical,
  Forward,
  Building2,
  Globe,
  UserPlus,
  Info,
  Bell,
  Image as ImageIcon,
  Lock,
  Shield,
  Languages,
  Users,
  UserRoundPlus,
  Ban,
  BadgeCheck,
  ThumbsDown,
  Search,
  Music,
  Timer
} from 'lucide-react-native';

export default function ProfileScreen({ activeChat, goBack }) {
  const styles = useStyles();
  const { colors } = useTheme();

  const [chatLock, setChatLock] = React.useState(false);
  const [translate, setTranslate] = React.useState(false);
  const [modalVisible, setModalVisible] = React.useState(false);

  return (
    <View style={styles.container}>
      <Modal visible={modalVisible} transparent={true} animationType="fade" onRequestClose={() => setModalVisible(false)}>
        <TouchableOpacity style={styles.modalBackground} activeOpacity={1} onPress={() => setModalVisible(false)}>
          <Image source={activeChat.avatar} style={styles.fullScreenAvatar} />
        </TouchableOpacity>
      </Modal>

      <ScrollView style={styles.scrollContent} showsVerticalScrollIndicator={false}>
        {/* Hero Section */}
        <View style={[styles.sectionCard, { marginTop: 0 }]}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', paddingHorizontal: 8, paddingTop: 8 }}>
            <TouchableOpacity onPress={goBack} style={styles.headerButton}>
              <ArrowLeft color={colors.textInverse} size={24} />
            </TouchableOpacity>
            <View style={styles.headerTitleContainer}>
              <Image source={activeChat?.avatar} style={styles.smallAvatar} />
              <Text style={styles.headerTitle}>{activeChat?.name || 'Contact Info'}</Text>
            </View>
            <TouchableOpacity style={styles.headerButton}>
              <MoreVertical color={colors.textInverse} size={24} />
            </TouchableOpacity>
          </View>
          
          <View style={[styles.heroContainer, { paddingTop: 8 }]}>
            <TouchableOpacity onPress={() => setModalVisible(true)} activeOpacity={0.8}>
              <Image source={activeChat.avatar} style={styles.heroAvatar} />
            </TouchableOpacity>
            <View style={styles.heroNameContainer}>
              <Text style={styles.heroName}>{activeChat.name}</Text>
              <BadgeCheck size={22} color="#53BDEB" fill="#fff" style={{ marginLeft: 6, marginTop: 4 }} />
            </View>
            <Text style={styles.heroPhone}>+91 22 2275 0353</Text>

            <TouchableOpacity style={styles.shareButton}>
              <Forward size={24} color="#00A884" />
            </TouchableOpacity>
            <Text style={styles.shareText}>Share</Text>
          </View>
        </View>

        {/* Business Details List */}
        <View style={styles.sectionCard}>
          <View style={styles.listItem}>
            <Building2 size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Public and government service</Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <Building2 size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>This is official business account of {activeChat.name}.</Text>
            </View>
          </View>

          <TouchableOpacity style={styles.listItem}>
            <Globe size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextLink} numberOfLines={1}>https://www.ruralhealth.gov.in</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity style={styles.listItem}>
            <UserPlus size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Add to contacts</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* Business Account Info */}
        <View style={styles.sectionCard}>
          <View style={styles.listItem}>
            <Info size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Business Account</Text>
              <Text style={styles.listTextSecondary}>This account uses WhatsApp Business</Text>
            </View>
          </View>
        </View>

        {/* Settings List */}
        <View style={styles.sectionCard}>
          <View style={styles.listItem}>
            <View style={styles.listIcon}>
              <Bell color={colors.iconColor} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Mute notifications</Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <View style={styles.listIcon}>
              <Music color={colors.iconColor} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Custom notifications</Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <View style={styles.listIcon}>
              <ImageIcon color={colors.iconColor} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Media visibility</Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <Lock size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Chat lock</Text>
              <Text style={styles.listTextSecondary}>Lock and hide this chat on this device.</Text>
            </View>
            <Switch
              value={chatLock}
              onValueChange={setChatLock}
              trackColor={{ false: '#E9EDEF', true: '#00A884' }}
              thumbColor={'#fff'}
            />
          </View>

          <View style={styles.listItem}>
            <Shield size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Security</Text>
              <Text style={styles.listTextSecondary}>
                This business uses a secure service from Meta to manage this chat. <Text style={styles.listTextLink}>Learn more</Text>
              </Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <Languages size={24} color={colors.iconColor} style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Translate messages</Text>
            </View>
            <Switch
              value={translate}
              onValueChange={setTranslate}
              trackColor={{ false: '#E9EDEF', true: '#00A884' }}
              thumbColor={'#fff'}
            />
          </View>

          <View style={styles.listItem}>
            <View style={styles.listIcon}>
              <Lock color={colors.iconColor} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Encryption</Text>
              <Text style={styles.listTextSecondary}>Messages and calls are end-to-end encrypted. Tap to verify.</Text>
            </View>
          </View>

          <View style={styles.listItem}>
            <View style={styles.listIcon}>
              <Timer color={colors.iconColor} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Disappearing messages</Text>
              <Text style={styles.listTextSecondary}>Off</Text>
            </View>
          </View>
        </View>

        {/* Groups & Actions */}
        <Text style={styles.sectionHeader}>No groups in common</Text>
        <View style={styles.sectionCard}>
          <TouchableOpacity style={styles.listItem}>
            <View style={styles.greenCircleIcon}>
              <Users size={20} color="#fff" />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Create group with {activeChat.name}</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity style={styles.listItem}>
            <View style={styles.greenCircleIcon}>
              <UserRoundPlus size={20} color="#fff" />
            </View>
            <View style={styles.listContent}>
              <Text style={styles.listTextPrimary}>Add to groups</Text>
              <Text style={styles.listTextSecondary}>Add this contact to groups you're in.</Text>
            </View>
          </TouchableOpacity>
        </View>

        <View style={[styles.sectionCard, { marginBottom: 40 }]}>
          <TouchableOpacity style={styles.listItem}>
            <Ban size={24} color="#EA0038" style={styles.listIcon} />
            <View style={styles.listContent}>
              <Text style={[styles.listTextPrimary, { color: '#EA0038' }]}>Block business</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity style={styles.listItem}>
            <View style={styles.listIcon}>
              <ThumbsDown color={colors.error} size={24} />
            </View>
            <View style={styles.listContent}>
              <Text style={[styles.listTextPrimary, { color: colors.error }]}>Report {activeChat?.name}</Text>
            </View>
          </TouchableOpacity>
        </View>

      </ScrollView>
    </View>
  );
}
