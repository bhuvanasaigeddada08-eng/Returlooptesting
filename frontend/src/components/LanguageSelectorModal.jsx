import React from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Globe, Check, X, Sparkles, Home } from "lucide-react";
import { SUPPORTED_LANGUAGES, setAppLanguage } from "../i18n";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export const LanguageSelectorModal = ({ isOpen, onClose }) => {
  const { t, i18n } = useTranslation();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  if (!isOpen) return null;

  const handleSelectLanguage = async (langCode) => {
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
        // quiet error if network fails
      }
    }

    if (onClose) onClose();

    // Automatically navigate to the main/home page
    navigate("/");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleGoToMainPage = () => {
    if (onClose) onClose();
    navigate("/");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div 
      className="fixed inset-0 z-[100] flex items-end sm:items-center justify-center p-0 sm:p-4 bg-slate-950/75 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div 
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-t-[32px] sm:rounded-3xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[85vh] max-h-[85dvh] animate-in slide-in-from-bottom-8 sm:zoom-in-95 duration-200"
        role="dialog"
        aria-labelledby="language-modal-title"
      >
        {/* Mobile Drag Indicator */}
        <div className="sm:hidden w-12 h-1.5 bg-slate-300 rounded-full mx-auto mt-3 mb-1 flex-shrink-0" />

        {/* Header */}
        <div className="px-5 sm:px-6 py-4 sm:py-5 border-b border-slate-100 flex items-center justify-between bg-slate-50/70 flex-shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center flex-shrink-0 shadow-xs">
              <Globe className="w-5 h-5" />
            </div>
            <div>
              <h2 id="language-modal-title" className="text-base font-extrabold text-slate-900 leading-tight">
                {t("nav.changeLang")}
              </h2>
              <p className="text-[11px] text-slate-500 font-medium">
                {t("home.selectLanguagePrompt")}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition cursor-pointer"
            aria-label={t("common.close")}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Language Grid - Scrollable with min-h-0 so all 7 languages are always reachable */}
        <div className="p-3 sm:p-5 overflow-y-auto space-y-2 flex-1 overscroll-contain min-h-0">
          {SUPPORTED_LANGUAGES.map((lang) => {
            const isSelected = i18n.language === lang.code;
            return (
              <button
                key={lang.code}
                type="button"
                onClick={() => handleSelectLanguage(lang.code)}
                className={`w-full py-2.5 px-3.5 sm:py-3.5 sm:px-4 rounded-2xl border text-left transition flex items-center justify-between group cursor-pointer ${
                  isSelected
                    ? "bg-blue-50/80 border-blue-500 text-blue-900 ring-2 ring-blue-500/20 shadow-xs"
                    : "bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50/80 text-slate-800"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span className="w-8 h-8 rounded-xl bg-slate-100 flex items-center justify-center text-xs font-bold font-mono text-slate-700 flex-shrink-0">
                    {lang.flag}
                  </span>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-base font-bold tracking-tight text-slate-900 group-hover:text-blue-600 transition">
                        {lang.nativeName}
                      </span>
                      {isSelected && (
                        <span className="px-1.5 py-0.5 rounded-md text-[9px] font-bold bg-blue-600 text-white uppercase tracking-wider">
                          Active
                        </span>
                      )}
                    </div>
                    <span className="text-[11px] text-slate-500 font-medium">
                      {lang.name} • {lang.script} script
                    </span>
                  </div>
                </div>

                <div className="flex items-center">
                  {isSelected ? (
                    <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-xs">
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    </div>
                  ) : (
                    <div className="w-6 h-6 rounded-full border border-slate-300 group-hover:border-slate-400 transition" />
                  )}
                </div>
              </button>
            );
          })}
        </div>

        {/* Footer with Go to Main Page button and Close */}
        <div className="p-3.5 sm:p-4 border-t border-slate-100 bg-slate-50/70 flex items-center justify-between text-xs text-slate-500 flex-shrink-0">
          <button
            type="button"
            onClick={handleGoToMainPage}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 font-bold text-xs transition cursor-pointer"
          >
            <Home className="w-3.5 h-3.5" />
            <span>{t("nav.home") || "Go to Main Page"}</span>
          </button>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition cursor-pointer flex-shrink-0 ml-2"
          >
            {t("common.close")}
          </button>
        </div>
      </div>
    </div>
  );
};

export default LanguageSelectorModal;
