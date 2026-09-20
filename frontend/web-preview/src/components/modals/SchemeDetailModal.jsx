import React, { useState } from 'react';
import { X, Award, ShieldCheck, Share2, ExternalLink, CheckCircle, HelpCircle, FileText, ListOrdered, Users } from 'lucide-react';

export default function SchemeDetailModal({ scheme, onClose }) {
  const [activeTab, setActiveTab] = useState('overview');
  if (!scheme) return null;

  const tabs = [
    { id: 'overview', label: 'Overview', icon: FileText },
    { id: 'benefits', label: 'Benefits', icon: ShieldCheck },
    { id: 'eligibility', label: 'Eligibility', icon: Users },
    { id: 'documents', label: 'Documents', icon: CheckCircle },
    { id: 'process', label: 'Application Process', icon: ListOrdered },
    { id: 'faqs', label: 'FAQs', icon: HelpCircle },
    { id: 'references', label: 'References & Portal', icon: ExternalLink },
  ];

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: scheme.title,
          text: `Check out government healthcare scheme: ${scheme.title}`,
          url: window.location.href,
        });
      } catch (err) {
        console.log('Share error:', err);
      }
    } else {
      navigator.clipboard.writeText(`${scheme.title} - ${scheme.description}`);
      alert('Scheme summary copied to clipboard!');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
      <div className="bg-white dark:bg-[#111b21] w-full max-w-4xl max-h-[90vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200 dark:border-[#222d34]">
        {/* Modal Header */}
        <div className="bg-[#202c33] text-white p-5 flex items-start justify-between border-b border-gray-700">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="bg-[#00a884] text-white text-[10px] font-bold px-2 py-0.5 rounded tracking-wide uppercase">
                {scheme.level}
              </span>
              <span className="text-xs text-gray-300 font-medium">{scheme.department}</span>
            </div>
            <h2 className="text-lg md:text-xl font-bold text-white">{scheme.title}</h2>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleShare}
              title="Share Scheme"
              className="p-2 hover:bg-[#2a3942] rounded-full text-gray-300 hover:text-white transition-all"
            >
              <Share2 className="w-5 h-5" />
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-[#2a3942] rounded-full text-gray-300 hover:text-white transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* 7 Tab Headers */}
        <div className="flex overflow-x-auto bg-[#111b21] border-b border-gray-800 scrollbar-thin">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-xs font-semibold whitespace-nowrap transition-all border-b-2 ${
                  isActive
                    ? 'border-[#00a884] text-[#00a884] bg-[#202c33]/50'
                    : 'border-transparent text-gray-400 hover:text-gray-200 hover:bg-[#202c33]/20'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Modal Tab Content Body */}
        <div className="flex-1 overflow-y-auto p-6 text-gray-800 dark:text-gray-200">
          {activeTab === 'overview' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Scheme Overview</h3>
              <p className="text-sm leading-relaxed text-gray-300">{scheme.description}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div className="bg-[#202c33] p-4 rounded-xl border border-gray-700">
                  <span className="text-xs text-gray-400 block font-semibold uppercase">Category / Level</span>
                  <span className="text-sm font-bold text-white mt-1 block">{scheme.level}</span>
                </div>
                <div className="bg-[#202c33] p-4 rounded-xl border border-gray-700">
                  <span className="text-xs text-gray-400 block font-semibold uppercase">Nodal Ministry</span>
                  <span className="text-sm font-bold text-white mt-1 block">{scheme.department}</span>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'benefits' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Key Coverage & Financial Benefits</h3>
              <ul className="space-y-3">
                {scheme.benefits?.map((item, i) => (
                  <li key={i} className="flex items-start gap-3 bg-[#202c33] p-3.5 rounded-xl border border-gray-700">
                    <ShieldCheck className="w-5 h-5 text-[#00a884] flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-200">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === 'eligibility' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Eligibility Criteria</h3>
              <ul className="space-y-3">
                {scheme.eligibility?.map((item, i) => (
                  <li key={i} className="flex items-start gap-3 bg-[#202c33] p-3.5 rounded-xl border border-gray-700">
                    <Users className="w-5 h-5 text-[#00a884] flex-shrink-0 mt-0.5" />
                    <span className="text-sm text-gray-200">{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {activeTab === 'documents' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Required Documents</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {scheme.documents?.map((doc, i) => (
                  <div key={i} className="flex items-center gap-3 bg-[#202c33] p-3.5 rounded-xl border border-gray-700">
                    <CheckCircle className="w-5 h-5 text-[#00a884]" />
                    <span className="text-sm font-medium text-gray-200">{doc}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'process' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">How to Apply / Claim Benefits</h3>
              <ol className="space-y-3">
                {scheme.process?.map((step, i) => (
                  <li key={i} className="flex items-start gap-3 bg-[#202c33] p-3.5 rounded-xl border border-gray-700">
                    <span className="w-6 h-6 rounded-full bg-[#00a884] text-white flex items-center justify-center font-bold text-xs flex-shrink-0 mt-0.5">
                      {i + 1}
                    </span>
                    <span className="text-sm text-gray-200">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          {activeTab === 'faqs' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Frequently Asked Questions</h3>
              <div className="space-y-3">
                {scheme.faqs?.map((faq, i) => (
                  <div key={i} className="bg-[#202c33] p-4 rounded-xl border border-gray-700">
                    <h4 className="font-semibold text-sm text-white mb-1">Q: {faq.q}</h4>
                    <p className="text-sm text-gray-300">A: {faq.a}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'references' && (
            <div className="space-y-4">
              <h3 className="text-base font-bold text-[#00a884]">Official Links & Resources</h3>
              <div className="space-y-3">
                {scheme.references?.map((ref, i) => (
                  <a
                    key={i}
                    href={ref.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between bg-[#202c33] hover:bg-[#2a3942] p-4 rounded-xl border border-gray-700 transition-all text-white font-medium text-sm group"
                  >
                    <span>{ref.title}</span>
                    <ExternalLink className="w-4 h-4 text-[#00a884] group-hover:translate-x-0.5 transition-transform" />
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="bg-[#202c33] p-4 flex justify-between items-center border-t border-gray-700">
          <span className="text-xs text-gray-400">Verified National Health Portal Data</span>
          <button
            onClick={onClose}
            className="bg-[#00a884] hover:bg-[#008f6f] text-white px-5 py-2 rounded-lg text-xs font-bold transition-all shadow"
          >
            Close Modal
          </button>
        </div>
      </div>
    </div>
  );
}
