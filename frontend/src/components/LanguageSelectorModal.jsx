import React from "react";
import { useTranslation } from "react-i18next";
import { Globe, Check, X } from "lucide-react";
import { SUPPORTED_LANGUAGES, setAppLanguage } from "../i18n";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export const LanguageSelectorModal = ({ isOpen, onClose }) => {
  const { t, i18n } = useTranslation();
  const { user, isAuthenticated } = useAuth();

  if (!isOpen) return null;

  const handleSelectLanguage = async (langCode) => {
    // Immediately apply language across the entire application
    setAppLanguage(langCode);
    localStorage.setItem("returnloop_lang_selected", "true");

    // If user is authenticated, save preference to their profile preferences
    if (isAuthenticated) {
      try {
        const existingPrefs = user?.notification_preferences || {};
        await api.updateProfile({
          notification_preferences: {
            ...existingPrefs,
            language: langCode
          }
        });
      } catch (err) {
        // silent fallback if network is slow
      }
    }

    if (onClose) onClose();
  };

  return (
    <div 
      className="fixed inset-0 z-[100] flex items-center justify-center p-3 sm:p-4 bg-slate-950/75 backdrop-blur-sm animate-in fade-in duration-150 overflow-hidden"
      onClick={onClose}
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-3xl max-w-sm sm:max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[85vh] max-h-[85dvh] my-auto animate-in zoom-in-95 duration-150"
        role="dialog"
        aria-labelledby="language-modal-title"
      >
        {/* Header */}
        <div className="px-4 py-3 sm:px-5 sm:py-3.5 border-b border-slate-100 flex items-center justify-between bg-slate-50/80 flex-shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0 shadow-xs border border-blue-100">
              <Globe className="w-4 h-4" />
            </div>
            <div>
              <h2 id="language-modal-title" className="text-sm sm:text-base font-extrabold text-slate-900 leading-tight">
                {t("nav.changeLang") || "Select Language / భాషను ఎంచుకోండి"}
              </h2>
              <p className="text-[10px] sm:text-[11px] text-slate-500 font-medium">
                {t("home.selectLanguagePrompt") || "Choose your preferred Indian language"}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition cursor-pointer"
            aria-label={t("common.close") || "Close"}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* 7 Languages List - Perfectly sized for mobile viewports */}
        <div className="p-2.5 sm:p-3 overflow-y-auto space-y-1.5 flex-1 min-h-0 overscroll-contain">
          {SUPPORTED_LANGUAGES.map((lang) => {
            const isSelected = (i18n.language || "en").startsWith(lang.code);
            return (
              <button
                key={lang.code}
                type="button"
                onClick={() => handleSelectLanguage(lang.code)}
                className={`w-full py-2.5 px-3 rounded-xl border text-left transition flex items-center justify-between group cursor-pointer ${
                  isSelected
                    ? "bg-blue-50/90 border-blue-500 text-blue-900 ring-2 ring-blue-500/20 shadow-xs"
                    : "bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50/80 text-slate-800"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-xs font-bold font-mono text-slate-700 flex-shrink-0 border border-slate-200">
                    {lang.flag}
                  </span>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="text-sm font-bold tracking-tight text-slate-900 group-hover:text-blue-600 transition">
                        {lang.nativeName}
                      </span>
                      {isSelected && (
                        <span className="px-1.5 py-0.2 rounded-md text-[9px] font-extrabold bg-blue-600 text-white uppercase tracking-wider">
                          Active
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] text-slate-500 font-medium">
                      {lang.name} • {lang.script} script
                    </span>
                  </div>
                </div>

                <div className="flex items-center ml-2 flex-shrink-0">
                  {isSelected ? (
                    <div className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-xs">
                      <Check className="w-3 h-3 stroke-[3]" />
                    </div>
                  ) : (
                    <div className="w-5 h-5 rounded-full border-2 border-slate-300 group-hover:border-slate-400 transition" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Modal Footer */}
        <div className="p-2.5 sm:p-3 border-t border-slate-100 bg-slate-50/70 flex items-center justify-between text-xs text-slate-500 flex-shrink-0">
          <span className="text-[10px] text-slate-500">
            7 Indian languages supported
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition cursor-pointer flex-shrink-0 ml-3"
          >
            {t("common.close") || "Close"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LanguageSelectorModal;
