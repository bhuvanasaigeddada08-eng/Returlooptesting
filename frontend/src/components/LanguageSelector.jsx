import React from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Globe } from "lucide-react";
import { getCurrentLanguage } from "../i18n";

export const LanguageSelector = ({ variant = "pill", className = "" }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const currentLang = getCurrentLanguage();

  const handleDirectRedirectToMainPage = () => {
    navigate("/");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (variant === "compact") {
    return (
      <button
        type="button"
        onClick={handleDirectRedirectToMainPage}
        className={`p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition flex items-center gap-1.5 cursor-pointer ${className}`}
        title={t("nav.changeLang") || "Language - Main Page"}
        aria-label={t("nav.changeLang") || "Language - Main Page"}
      >
        <Globe className="w-4 h-4 text-blue-600" />
        <span className="text-xs font-bold text-slate-800">{currentLang.nativeName}</span>
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={handleDirectRedirectToMainPage}
      className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold shadow-xs hover:border-slate-300 transition cursor-pointer ${className}`}
      title={t("nav.changeLang") || "Language - Main Page"}
    >
      <span className="text-sm" role="img" aria-hidden="true">{currentLang.flag}</span>
      <span className="font-bold text-slate-900">{currentLang.nativeName}</span>
    </button>
  );
};

export default LanguageSelector;
