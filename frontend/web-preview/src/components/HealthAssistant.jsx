import { useState } from 'react';
import { FaComments, FaUser, FaBook, FaEllipsisH, FaArrowLeft } from 'react-icons/fa';
import { FaMicrophone, FaPaperPlane } from 'react-icons/fa';
import { FaAmbulance, FaHospital, FaUserMd, FaFirstAid } from 'react-icons/fa';

const chats = [
  {
    id: 1,
    name: 'AI Health Assistant',
    avatar: '/logo_cropped.png',
    lastMessage: 'Hello! How can I help you today?',
    time: '11:56 PM',
    messages: [
      {
        id: 1,
        text: "Hello! I'm your health assistant. I can help with first-aid, symptom assessment, and health guidance. What would you like to know?",
        time: '11:56 PM',
        fromMe: false,
      },
    ],
  },
  {
    id: 2,
    name: 'Doctor Consultation',
    avatar: '/logo.png',
    lastMessage: 'Your appointment is confirmed for tomorrow.',
    time: '10:30 AM',
    messages: [
      {
        id: 1,
        text: 'Your appointment is confirmed for tomorrow at 10:00 AM. Please bring your previous reports.',
        time: '10:30 AM',
        fromMe: false,
      },
    ],
  },
];

export default function HealthAssistant() {
  const [activeTab, setActiveTab] = useState('chats');
  const [selectedChat, setSelectedChat] = useState(null);
  const [inputText, setInputText] = useState('');
  const [language, setLanguage] = useState('en');
  const [chatMessages, setChatMessages] = useState(
    chats.reduce((acc, c) => ({ ...acc, [c.id]: [...c.messages] }), {})
  );

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'bn', name: 'বাংলা' },
    { code: 'te', name: 'తెలుగు' },
    { code: 'ta', name: 'தமிழ்' },
    { code: 'mr', name: 'मराठी' },
    { code: 'gu', name: 'ગુજરાતી' },
    { code: 'kn', name: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'മലയാളം' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ' },
  ];

  const handleSend = () => {
    if (!inputText.trim() || !selectedChat) return;
    const newMsg = {
      id: Date.now(),
      text: inputText.trim(),
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      fromMe: true,
    };
    setChatMessages((prev) => ({
      ...prev,
      [selectedChat.id]: [...(prev[selectedChat.id] || []), newMsg],
    }));
    setInputText('');
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col font-sans">
      {/* Header */}
      <div className="bg-white shadow-md p-4 flex-shrink-0">
        <div className="flex justify-between items-center">
          {selectedChat ? (
            <div className="flex items-center gap-3">
              <button onClick={() => setSelectedChat(null)} className="text-gray-600 hover:text-gray-800">
                <FaArrowLeft className="text-lg" />
              </button>
              <img
                src={selectedChat.avatar}
                alt={selectedChat.name}
                className="w-9 h-9 rounded-full object-cover border border-gray-200"
              />
              <h2 className="text-base font-semibold text-gray-800">{selectedChat.name}</h2>
            </div>
          ) : (
            <h2 className="text-lg font-semibold text-gray-800">RuralHealth.AI</h2>
          )}
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="px-3 py-1 mr-5 rounded-md border border-gray-300 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-y-auto">
        {activeTab === 'chats' && !selectedChat && (
          /* Chat List */
          <div className="divide-y divide-gray-200 bg-white">
            {chats.map((chat) => (
              <button
                key={chat.id}
                onClick={() => setSelectedChat(chat)}
                className="w-full flex items-center gap-4 px-4 py-3 hover:bg-gray-50 transition-colors text-left"
              >
                <img
                  src={chat.avatar}
                  alt={chat.name}
                  className="w-12 h-12 rounded-full object-cover border border-gray-200 flex-shrink-0"
                />
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-center">
                    <span className="font-semibold text-gray-800 text-sm">{chat.name}</span>
                    <span className="text-xs text-gray-400 ml-2 flex-shrink-0">{chat.time}</span>
                  </div>
                  <p className="text-xs text-gray-500 truncate mt-0.5">{chat.lastMessage}</p>
                </div>
              </button>
            ))}
          </div>
        )}

        {activeTab === 'chats' && selectedChat && (
          /* Chat Messages */
          <div className="flex flex-col gap-3 px-4 py-4 pb-36">
            {(chatMessages[selectedChat.id] || []).map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.fromMe ? 'justify-end' : 'justify-start'}`}
              >
                {!msg.fromMe && (
                  <img
                    src={selectedChat.avatar}
                    alt={selectedChat.name}
                    className="w-8 h-8 rounded-full object-cover border border-gray-200 mr-2 flex-shrink-0 self-end"
                  />
                )}
                <div
                  className={`max-w-xs px-4 py-2 rounded-2xl shadow-sm text-sm ${
                    msg.fromMe
                      ? 'bg-blue-500 text-white rounded-br-none'
                      : 'bg-blue-50 text-gray-700 rounded-bl-none'
                  }`}
                >
                  <p>{msg.text}</p>
                  <p className={`text-xs mt-1 text-right ${msg.fromMe ? 'text-blue-100' : 'text-gray-400'}`}>
                    {msg.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab !== 'chats' && (
          <div className="flex items-center justify-center h-48 text-gray-400 text-sm">
            {activeTab === 'profile' && 'Profile coming soon'}
            {activeTab === 'resources' && 'Resources coming soon'}
            {activeTab === 'more' && 'More options coming soon'}
          </div>
        )}
      </div>

      {/* Action Buttons (only on chat list view) */}
      {activeTab === 'chats' && !selectedChat && (
        <div className="grid grid-cols-4 gap-2 px-4 py-3 bg-white border-t">
          <button className="bg-red-500 text-white py-3 text-xs rounded-lg shadow hover:bg-red-600 flex flex-col items-center gap-1">
            <FaAmbulance className="text-lg" /> Emergency
          </button>
          <button className="bg-blue-500 text-white py-3 text-xs rounded-lg shadow hover:bg-blue-600 flex flex-col items-center gap-1">
            <FaHospital className="text-lg" /> Find Hospital
          </button>
          <button className="bg-blue-500 text-white py-3 text-xs rounded-lg shadow hover:bg-blue-600 flex flex-col items-center gap-1">
            <FaUserMd className="text-lg" /> Book Doctor
          </button>
          <button className="bg-blue-500 text-white py-3 text-xs rounded-lg shadow hover:bg-blue-600 flex flex-col items-center gap-1">
            <FaFirstAid className="text-lg" /> First Aid
          </button>
        </div>
      )}

      {/* Bottom Section */}
      <div className="bg-white border-t flex-shrink-0">
        {/* Chat Input (only in open chat) */}
        {activeTab === 'chats' && selectedChat && (
          <div className="px-4 py-2">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Type your symptoms or question..."
                className="flex-1 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
              />
              <button
                title="Voice Input"
                className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 focus:outline-none"
              >
                <FaMicrophone className="text-xl text-gray-600" />
              </button>
              <button
                title="Send"
                onClick={handleSend}
                className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 focus:outline-none"
              >
                <FaPaperPlane className="text-xl" />
              </button>
            </div>
          </div>
        )}

        {/* Bottom Navigation */}
        <nav className="flex justify-around items-center border-t py-2 text-sm text-gray-600">
          <button
            onClick={() => { setActiveTab('chats'); setSelectedChat(null); }}
            className={`flex flex-col items-center gap-0.5 ${activeTab === 'chats' ? 'text-blue-500' : ''}`}
          >
            <FaComments className="text-xl" />
            <span>Chats</span>
          </button>
          <button
            onClick={() => { setActiveTab('profile'); setSelectedChat(null); }}
            className={`flex flex-col items-center gap-0.5 ${activeTab === 'profile' ? 'text-blue-500' : ''}`}
          >
            <FaUser className="text-xl" />
            <span>Profile</span>
          </button>
          <button
            onClick={() => { setActiveTab('resources'); setSelectedChat(null); }}
            className={`flex flex-col items-center gap-0.5 ${activeTab === 'resources' ? 'text-blue-500' : ''}`}
          >
            <FaBook className="text-xl" />
            <span>Resources</span>
          </button>
          <button
            onClick={() => { setActiveTab('more'); setSelectedChat(null); }}
            className={`flex flex-col items-center gap-0.5 ${activeTab === 'more' ? 'text-blue-500' : ''}`}
          >
            <FaEllipsisH className="text-xl" />
            <span>More</span>
          </button>
        </nav>
      </div>
    </div>
  );
}