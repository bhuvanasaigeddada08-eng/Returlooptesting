import React, { useState } from "react";
import { useTranslation } from "react-i18next";
import { Globe, ChevronDown } from "lucide-react";
import { getCurrentLanguage } from "../i18n";
import LanguageSelectorModal from "./LanguageSelectorModal";

export const LanguageSelector = ({ variant = "pill", className = "" }) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const currentLang = getCurrentLanguage();

  return (
    <>
      {variant === "compact" ? (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className={`inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-full border border-slate-200/90 bg-white/90 shadow-xs hover:bg-slate-50 text-slate-800 text-xs font-bold transition cursor-pointer active:scale-95 ${className}`}
          title={t("nav.changeLang") || "Change Language"}
          aria-label={t("nav.changeLang") || "Change Language"}
        >
          <span className="text-xs" role="img" aria-hidden="true">{currentLang.flag}</span>
          <span className="font-extrabold text-slate-900">{currentLang.nativeName}</span>
          <ChevronDown className="w-3 h-3 text-slate-400" />
        </button>
      ) : (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold shadow-xs hover:border-slate-300 transition cursor-pointer ${className}`}
          title={t("nav.changeLang") || "Change Language"}
        >
          <Globe className="w-3.5 h-3.5 text-blue-600" />
          <span className="font-bold text-slate-900">{currentLang.nativeName}</span>
          <ChevronDown className="w-3 h-3 text-slate-400" />
        </button>
      )}

      {/* Language Selection Modal */}
      <LanguageSelectorModal isOpen={isOpen} onClose={() => setIsOpen(false)} />
    </>
  );
};

export default LanguageSelector;
