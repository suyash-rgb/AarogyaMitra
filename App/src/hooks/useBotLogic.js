import { useState, useEffect } from 'react';
import { Linking } from 'react-native';
import * as Location from 'expo-location';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAudioPlayer } from 'expo-audio';
import { getSimulatedResponse, mockDoctors, mockHospitals } from '../constants/mockData';
import { translations, getTranslation } from '../constants/translations';
import { searchSchemesRAG, getHealthcareSchemes, getNearbyFacilities, getStates, classifyIntent } from '../services/apiService';

export function useBotLogic({ chat, messages, setMessages, initialLanguage = 'en' }) {
  const player = useAudioPlayer(require('../../assets/notification.wav'));

  const playSound = () => {
    if (player) {
      try {
        player.seekTo(0);
        player.play();
      } catch (err) {
        console.log("Sound play error:", err);
      }
    }
  };

  const [isTyping, setIsTyping] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState(initialLanguage);
  const [langModalVisible, setLangModalVisible] = useState(false);
  const [stateModalVisible, setStateModalVisible] = useState(false);
  const [userState, setUserState] = useState(null);
  const [availableStates, setAvailableStates] = useState([]);

  useEffect(() => {
    const loadStateAndData = async () => {
      try {
        const savedState = await AsyncStorage.getItem('user_state');
        if (savedState) setUserState(savedState);
      } catch (e) {
        console.error("Failed to load user state", e);
      }

      try {
        const statesData = await getStates();
        if (Array.isArray(statesData)) {
          setAvailableStates(statesData);
        } else if (statesData && Array.isArray(statesData.states)) {
          setAvailableStates(statesData.states);
        }
      } catch (e) {
        console.error("Failed to fetch states meta data", e);
      }
    };
    loadStateAndData();
  }, []);

  useEffect(() => {
    if (chat.id === 'ai-bot') {
      setMessages(prev => {
        if (prev.length > 0 && prev[0].id === 'msg-0') {
          const translatedInit = getTranslation(currentLanguage, 'initMsg');
          if (translatedInit && prev[0].text !== translatedInit) {
            const updated = [...prev];
            updated[0] = { ...updated[0], text: translatedInit };
            return updated;
          }
        }
        return prev;
      });
    }
  }, [chat.id, currentLanguage]);

  useEffect(() => {
    if (chat.id === 'ai-bot' && messages.length === 1) {
      let isMounted = true;

      const loadMessages = async () => {
        const followUps = [
          {
            id: 'msg-1',
            text: getTranslation(currentLanguage, 'welcome'),
            sender: 'other',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            buttons: [
              getTranslation(currentLanguage, 'knowSchemes'),
              getTranslation(currentLanguage, 'locate'),
              getTranslation(currentLanguage, 'lang'),
              getTranslation(currentLanguage, 'book'),
              getTranslation(currentLanguage, 'doctor'),
              getTranslation(currentLanguage, 'help')
            ]
          }
        ];

        for (let i = 0; i < followUps.length; i++) {
          if (!isMounted) break;

          setIsTyping(true);
          await new Promise(resolve => setTimeout(resolve, 1500));

          if (!isMounted) break;
          setIsTyping(false);

          playSound();
          setMessages(prev => [...prev, followUps[i]]);
          await new Promise(resolve => setTimeout(resolve, 500));
        }
      };

      loadMessages();

      return () => {
        isMounted = false;
      };
    }
  }, [chat.id, currentLanguage]);

  const simulateBotResponse = async (userText) => {
    setIsTyping(true);
    const userLower = userText.toLowerCase();

    const is104Call = userLower.includes('104') || userLower.includes('helpline') || userLower.includes('call-back');
    const isSanjeevani = userLower.includes('esanjeevani') || userLower.includes('संजीवनी');
    const isAbhaDoc = userLower.includes('abha') || userLower.includes('आभा');

    if (is104Call) {
      setIsTyping(false);
      const botReply = getTranslation(currentLanguage, 'call104Reply');
      try {
        Linking.openURL('tel:104');
      } catch (e) {
        console.error("Dialer error:", e);
      }
      const botMsg = {
        id: Date.now().toString(),
        text: botReply,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
      return;
    }

    if (isSanjeevani) {
      setIsTyping(false);
      const botReply = getTranslation(currentLanguage, 'esanjeevaniReply');
      try {
        Linking.openURL('https://esanjeevaniopd.in');
      } catch (e) {
        console.error("Linking error:", e);
      }
      const botMsg = {
        id: Date.now().toString(),
        text: botReply,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
      return;
    }

    if (isAbhaDoc) {
      setIsTyping(false);
      const botReply = getTranslation(currentLanguage, 'selectDoc');
      const botMsg = {
        id: Date.now().toString(),
        text: botReply,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        carouselItems: mockDoctors
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
      return;
    }

    try {
      const userContext = {
        language: currentLanguage || 'en',
        state: userState || null
      };

      const intentRes = await classifyIntent(userText, userContext);
      setIsTyping(false);

      const { intent, response_data } = intentRes;

      let botReply = '';
      let schemeCarouselItems = null;
      let hospitalCarouselItems = null;
      let buttons = null;

      if (intent === 'GOVT_SCHEMES_DISCOVERY') {
        const schemes = response_data?.schemes || [];
        if (schemes.length > 0) {
          botReply = response_data.message || getTranslation(currentLanguage, 'schemesFound');
          schemeCarouselItems = schemes;
        } else {
          try {
            const ragData = await searchSchemesRAG(userText, userState);
            botReply = (ragData?.answer && ragData.answer.trim()) 
              ? ragData.answer 
              : getTranslation(currentLanguage, 'schemesFound');
            schemeCarouselItems = null;
          } catch (ragErr) {
            console.error("RAG Error:", ragErr);
            botReply = getTranslation(currentLanguage, 'schemesBusy');
          }
        }
      } else if (intent === 'FACILITY_DISCOVERY') {
        const facilities = response_data?.facilities || [];
        if (facilities.length > 0) {
          botReply = (response_data?.message && response_data.message.trim()) || getTranslation(currentLanguage, 'locReply');
          hospitalCarouselItems = facilities;
        } else {
          botReply = (response_data?.message && response_data.message.trim()) || getTranslation(currentLanguage, 'locReply');
          hospitalCarouselItems = mockHospitals;
        }
      } else if (intent === 'GREETING_CONVERSATIONAL') {
        botReply = (response_data?.message && response_data.message.trim()) || getTranslation(currentLanguage, 'welcome');
        buttons = [
          getTranslation(currentLanguage, 'knowSchemes'),
          getTranslation(currentLanguage, 'locate'),
          getTranslation(currentLanguage, 'lang'),
          getTranslation(currentLanguage, 'book'),
          getTranslation(currentLanguage, 'doctor'),
          getTranslation(currentLanguage, 'help')
        ];
      } else if (intent === 'GENERAL_MEDICAL_QA') {
        botReply = getSimulatedResponse(userText, chat.name);
      } else {
        botReply = (response_data?.message && response_data.message.trim()) || getSimulatedResponse(userText, chat.name);
      }

      const botMsg = {
        id: (Date.now() + 1).toString(),
        text: botReply,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        schemeCarouselItems,
        hospitalCarouselItems,
        buttons
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);

    } catch (error) {
      console.error("Intent Router Classification Error:", error);
      setIsTyping(false);

      const botReply = getSimulatedResponse(userText, chat.name);
      const botMsg = {
        id: (Date.now() + 1).toString(),
        text: botReply,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
    }
  };

  const fetchSchemes = async (stateName) => {
    setIsTyping(true);
    try {
      const data = await getHealthcareSchemes(stateName);
      setIsTyping(false);

      if (data.items && data.items.length > 0) {
        const botMsg = {
          id: Date.now().toString(),
          text: getTranslation(currentLanguage, 'schemesFound'),
          sender: 'other',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          schemeCarouselItems: data.items
        };
        playSound();
        setMessages(prev => [...prev, botMsg]);
      } else {
        const botMsg = {
          id: Date.now().toString(),
          text: `I couldn't find any specific schemes for ${stateName} at the moment.`,
          sender: 'other',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        playSound();
        setMessages(prev => [...prev, botMsg]);
      }
    } catch (error) {
      console.error("Schemes API error:", error);
      setIsTyping(false);
      const botMsg = {
        id: Date.now().toString(),
        text: getTranslation(currentLanguage, 'schemesBusy'),
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
    }
  };

  const handleBookDoctor = (doc) => {
    const userMsg = {
      id: Date.now().toString(),
      text: `I want to book an appointment with ${doc.name}`,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);

    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      const ticketMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        type: 'ticket',
        ticketData: {
          doctorName: doc.name,
          specialty: doc.specialty,
          date: new Date(Date.now() + 86400000).toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' }),
          time: '11:00 AM (Tele-consult)'
        }
      };
      playSound();
      setMessages(prev => [...prev, ticketMsg]);
    }, 1500);
  };

  const handleSelectLanguage = (langCode) => {
    setLangModalVisible(false);
    setCurrentLanguage(langCode);

    const confirmText = getTranslation(langCode, 'confirmLang');
    const userMsg = {
      id: Date.now().toString(),
      text: confirmText,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);

    setIsTyping(true);
    setTimeout(() => {
      setIsTyping(false);
      const welcomeText = getTranslation(langCode, 'welcome');
      const botMsg = {
        id: (Date.now() + 1).toString(),
        text: welcomeText,
        sender: 'other',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        buttons: [
          getTranslation(langCode, 'knowSchemes'),
          getTranslation(langCode, 'locate'),
          getTranslation(langCode, 'lang'),
          getTranslation(langCode, 'book'),
          getTranslation(langCode, 'doctor'),
          getTranslation(langCode, 'help')
        ]
      };
      playSound();
      setMessages(prev => [...prev, botMsg]);
    }, 1200);
  };

  const handleQuickReplyButtonPress = (btn) => {
    const isKnowSchemes = Object.keys(translations).some(l => btn.includes(translations[l].knowSchemes) || btn.includes('Know Govt Schemes'));
    if (isKnowSchemes) {
      const tempMsg = {
        id: Date.now().toString(),
        text: btn,
        sender: 'me',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, tempMsg]);

      setTimeout(() => {
        const botMsg = {
          id: Date.now().toString(),
          text: getTranslation(currentLanguage, 'selectState'),
          sender: 'other',
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        playSound();
        setMessages(prev => [...prev, botMsg]);
        setStateModalVisible(true);
      }, 500);
      return;
    }

    const isLocate = Object.keys(translations).some(l => btn.includes(translations[l].locate) || btn.includes('Locate a Healthcare Facility'));
    if (isLocate) {
      (async () => {
        try {
          const tempMsg = {
            id: Date.now().toString(),
            text: btn,
            sender: 'me',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          setMessages(prev => [...prev, tempMsg]);
          setIsTyping(true);

          let { status } = await Location.requestForegroundPermissionsAsync();
          if (status !== 'granted') {
            setTimeout(() => {
              setIsTyping(false);
              const botReply = getTranslation(currentLanguage, 'gps_denied') || "I need location access to find nearby healthcare facilities...";
              const botMsg = { id: Date.now().toString(), text: botReply, sender: 'other', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
              setMessages(prev => [...prev, botMsg]);
            }, 1000);
            return;
          }

          let location = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced, timeout: 10000 });
          if (!location) location = await Location.getLastKnownPositionAsync();
          if (!location) throw new Error("Could not get location");

          const locMsg = {
            id: (Date.now() + 1).toString(),
            text: `${getTranslation(currentLanguage, 'locAcquired').replace('{lat}', location.coords.latitude.toFixed(6)).replace('{lon}', location.coords.longitude.toFixed(6))}`,
            sender: 'me',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          setMessages(prev => [...prev, locMsg]);

          if (chat.isOfficial) {
            try {
              const data = await getNearbyFacilities(location.coords.latitude, location.coords.longitude, 5000);
              const hospitals = data.facilities && data.facilities.length > 0 ? data.facilities : mockHospitals;
              setIsTyping(false);
              const botReply = getTranslation(currentLanguage, 'locReply');
              const botMsg = { id: (Date.now() + 2).toString(), text: botReply, sender: 'other', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), hospitalCarouselItems: hospitals };
              setMessages(prev => [...prev, botMsg]);
            } catch (error) {
              console.error("API error:", error);
              setIsTyping(false);
              const botMsg = { id: (Date.now() + 2).toString(), text: getTranslation(currentLanguage, 'locReply'), sender: 'other', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }), hospitalCarouselItems: mockHospitals };
              setMessages(prev => [...prev, botMsg]);
            }
          } else {
            setIsTyping(false);
          }
        } catch (error) {
          console.error(error);
          setTimeout(() => {
            setIsTyping(false);
            const botMsg = { id: Date.now().toString(), text: "There was an error fetching your location.", sender: 'other', time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) };
            setMessages(prev => [...prev, botMsg]);
          }, 1000);
        }
      })();
      return;
    }

    const isLang = Object.keys(translations).some(l => btn.includes(translations[l].lang) || btn.includes('Change Language'));
    if (isLang) {
      setLangModalVisible(true);
      return;
    }

    const newMsg = {
      id: Date.now().toString(),
      text: btn,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, newMsg]);
    if (chat.isOfficial) {
      simulateBotResponse(btn);
    }
  };

  const handleStateSelect = async (stateName) => {
    setStateModalVisible(false);
    setUserState(stateName);
    await AsyncStorage.setItem('user_state', stateName);

    const userMsg = {
      id: Date.now().toString(),
      text: `I am from ${stateName}`,
      sender: 'me',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [...prev, userMsg]);
    fetchSchemes(stateName);
  };

  return {
    isTyping,
    currentLanguage,
    setCurrentLanguage,
    langModalVisible,
    setLangModalVisible,
    stateModalVisible,
    setStateModalVisible,
    userState,
    availableStates,
    simulateBotResponse,
    handleBookDoctor,
    handleSelectLanguage,
    handleQuickReplyButtonPress,
    handleStateSelect
  };
}
