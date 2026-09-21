import React, { useState, useEffect } from 'react';
import { View, Text, Modal, TouchableOpacity, ScrollView, ActivityIndicator, Linking, StyleSheet, Share } from 'react-native';
import { X, FileText, ExternalLink, HelpCircle, FileCheck, CheckCircle2, Share2 } from 'lucide-react-native';
import { getSchemeDetails } from '../services/apiService';
import { TtsPlayerButton } from './TtsPlayerButton';

const TABS = [
  { id: 'overview', label: 'Overview', icon: FileText },
  { id: 'benefits', label: 'Benefits', icon: CheckCircle2 },
  { id: 'eligibility', label: 'Eligibility', icon: HelpCircle },
  { id: 'documents', label: 'Documents', icon: FileCheck },
  { id: 'process', label: 'Process', icon: FileText },
  { id: 'faqs', label: 'FAQs', icon: HelpCircle },
  { id: 'references', label: 'References', icon: ExternalLink },
];

export const SchemeDetailsModal = ({ visible, onClose, schemeId }) => {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    if (visible && schemeId) {
      setLoading(true);
      setActiveTab('overview');
      getSchemeDetails(schemeId)
        .then(data => {
          setDetails(data);
          setLoading(false);
        })
        .catch(err => {
          console.error("Failed to load scheme details:", err);
          setLoading(false);
        });
    } else {
      setDetails(null);
    }
  }, [visible, schemeId]);

  const handleShare = async () => {
    if (!details) return;
    try {
      let url = '';
      if (details.references && details.references.length > 0 && details.references[0].url) {
        url = details.references[0].url;
      } else {
        // Fallback to a Google search link since myscheme slugs can be unpredictable
        url = `https://www.google.com/search?q=${encodeURIComponent(details.scheme_name)}`;
      }

      const message = `Check out this government healthcare scheme: ${details.scheme_name}\n\n${details.brief_description || ''}\n\nLearn more: ${url}`;
      
      await Share.share({
        message: message,
        title: details.scheme_name,
        url: url // Used by iOS
      });
    } catch (error) {
      console.error("Error sharing:", error);
    }
  };

  const renderContent = () => {
    if (loading) {
      return (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#128C7E" />
          <Text style={styles.loadingText}>Loading details...</Text>
        </View>
      );
    }

    if (!details) {
      return (
        <View style={styles.loadingContainer}>
          <Text style={styles.errorText}>Failed to load scheme details.</Text>
        </View>
      );
    }

    switch (activeTab) {
      case 'overview':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={{flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12}}>
              <Text style={[styles.sectionTitle, {marginBottom: 0}]}>Brief Description</Text>
              <TtsPlayerButton text={details.brief_description || 'No description available.'} size={20} color="#128C7E" />
            </View>
            <Text style={styles.bodyText}>{details.brief_description || 'No description available.'}</Text>
            
            {details.description && (
              <>
                <View style={{flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, marginTop: 16}}>
                  <Text style={[styles.sectionTitle, {marginBottom: 0, marginTop: 0}]}>Detailed Overview</Text>
                  <TtsPlayerButton text={details.description} size={20} color="#128C7E" />
                </View>
                <Text style={styles.bodyText}>{details.description}</Text>
              </>
            )}
            
            <View style={styles.metaBox}>
              <Text style={styles.metaText}><Text style={styles.metaLabel}>Department: </Text>{details.department || 'N/A'}</Text>
              <Text style={styles.metaText}><Text style={styles.metaLabel}>Level: </Text>{details.level || 'N/A'}</Text>
              <Text style={styles.metaText}><Text style={styles.metaLabel}>Beneficiaries: </Text>{details.beneficiaries || 'N/A'}</Text>
            </View>
          </ScrollView>
        );
      case 'benefits':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={{flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12}}>
              <Text style={[styles.sectionTitle, {marginBottom: 0}]}>Benefits</Text>
              <TtsPlayerButton text={details.benefits || 'No specific benefits documented.'} size={20} color="#128C7E" />
            </View>
            <Text style={styles.bodyText}>{details.benefits || 'No specific benefits documented.'}</Text>
          </ScrollView>
        );
      case 'eligibility':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <View style={{flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12}}>
              <Text style={[styles.sectionTitle, {marginBottom: 0}]}>Eligibility Criteria</Text>
              <TtsPlayerButton text={details.eligibility || 'No specific eligibility criteria documented.'} size={20} color="#128C7E" />
            </View>
            <Text style={styles.bodyText}>{details.eligibility || 'No specific eligibility criteria documented.'}</Text>
          </ScrollView>
        );
      case 'documents':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.sectionTitle}>Required Documents</Text>
            {details.documents && details.documents.length > 0 ? (
              details.documents.map((doc, idx) => (
                <View key={idx} style={styles.listItem}>
                  <View style={styles.bullet} />
                  <Text style={styles.listText}>{doc.document_name}</Text>
                </View>
              ))
            ) : (
              <Text style={styles.bodyText}>No specific documents listed.</Text>
            )}
          </ScrollView>
        );
      case 'process':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.sectionTitle}>Application Process</Text>
            <Text style={styles.bodyText}>{details.application_process || 'Application process not documented.'}</Text>
          </ScrollView>
        );
      case 'faqs':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.sectionTitle}>Frequently Asked Questions</Text>
            {details.faqs && details.faqs.length > 0 ? (
              details.faqs.map((faq, idx) => (
                <View key={idx} style={styles.faqCard}>
                  <Text style={styles.faqQ}>Q: {faq.question}</Text>
                  <Text style={styles.faqA}>A: {faq.answer}</Text>
                </View>
              ))
            ) : (
              <Text style={styles.bodyText}>No FAQs available.</Text>
            )}
          </ScrollView>
        );
      case 'references':
        return (
          <ScrollView contentContainerStyle={styles.scrollContent}>
            <Text style={styles.sectionTitle}>References & Links</Text>
            {details.references && details.references.length > 0 ? (
              details.references.map((ref, idx) => (
                <TouchableOpacity 
                  key={idx} 
                  style={styles.linkCard} 
                  onPress={() => Linking.openURL(ref.url)}
                >
                  <ExternalLink size={20} color="#0066cc" />
                  <Text style={styles.linkText}>{ref.title || ref.url}</Text>
                </TouchableOpacity>
              ))
            ) : (
              <Text style={styles.bodyText}>No external references provided.</Text>
            )}
          </ScrollView>
        );
      default:
        return null;
    }
  };

  return (
    <Modal visible={visible} animationType="slide" transparent={true} onRequestClose={onClose}>
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.title} numberOfLines={2}>
              {details ? details.scheme_name : 'Scheme Details'}
            </Text>
            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
              {details && (
                <TouchableOpacity onPress={handleShare} style={[styles.closeBtn, { marginRight: 16 }]}>
                  <Share2 size={22} color="#128C7E" />
                </TouchableOpacity>
              )}
              <TouchableOpacity onPress={onClose} style={styles.closeBtn}>
                <X size={24} color="#111B21" />
              </TouchableOpacity>
            </View>
          </View>

          {/* Tabs */}
          {!loading && details && (
            <View>
              <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.tabScroll} contentContainerStyle={styles.tabContent}>
                {TABS.map(tab => {
                  const Icon = tab.icon;
                  const isActive = activeTab === tab.id;
                  return (
                    <TouchableOpacity
                      key={tab.id}
                      style={[styles.tabBtn, isActive && styles.tabBtnActive]}
                      onPress={() => setActiveTab(tab.id)}
                    >
                      <Icon size={16} color={isActive ? '#fff' : '#666'} style={{ marginRight: 6 }} />
                      <Text style={[styles.tabText, isActive && styles.tabTextActive]}>{tab.label}</Text>
                    </TouchableOpacity>
                  );
                })}
              </ScrollView>
            </View>
          )}

          {/* Content */}
          <View style={styles.contentArea}>
            {renderContent()}
          </View>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    height: '85%',
    flexDirection: 'column',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111B21',
    flex: 1,
    marginRight: 12,
  },
  closeBtn: {
    padding: 4,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    color: '#666',
    fontSize: 16,
  },
  errorText: {
    color: '#d32f2f',
    fontSize: 16,
  },
  tabScroll: {
    backgroundColor: '#f9f9f9',
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  tabContent: {
    paddingHorizontal: 12,
    paddingVertical: 12,
    alignItems: 'center',
  },
  tabBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#eee',
    marginRight: 8,
  },
  tabBtnActive: {
    backgroundColor: '#128C7E',
  },
  tabText: {
    color: '#666',
    fontSize: 14,
    fontWeight: '500',
  },
  tabTextActive: {
    color: '#fff',
    fontWeight: 'bold',
  },
  contentArea: {
    flex: 1,
  },
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111B21',
    marginBottom: 12,
  },
  bodyText: {
    fontSize: 15,
    color: '#333',
    lineHeight: 22,
  },
  metaBox: {
    marginTop: 20,
    backgroundColor: '#f5f5f5',
    padding: 16,
    borderRadius: 8,
  },
  metaText: {
    fontSize: 14,
    color: '#444',
    marginBottom: 6,
  },
  metaLabel: {
    fontWeight: 'bold',
    color: '#111B21',
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  bullet: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#128C7E',
    marginTop: 8,
    marginRight: 10,
  },
  listText: {
    flex: 1,
    fontSize: 15,
    color: '#333',
    lineHeight: 22,
  },
  faqCard: {
    backgroundColor: '#f8f9fa',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#eee',
  },
  faqQ: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#111B21',
    marginBottom: 8,
  },
  faqA: {
    fontSize: 15,
    color: '#444',
    lineHeight: 22,
  },
  linkCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#e6f2ff',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
  },
  linkText: {
    marginLeft: 12,
    fontSize: 15,
    color: '#0066cc',
    textDecorationLine: 'underline',
    flex: 1,
  }
});
