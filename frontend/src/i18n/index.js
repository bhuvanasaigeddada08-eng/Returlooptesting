import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./locales/en.json";
import te from "./locales/te.json";
import hi from "./locales/hi.json";
import pa from "./locales/pa.json";
import ml from "./locales/ml.json";
import ta from "./locales/ta.json";
import kn from "./locales/kn.json";

export const SUPPORTED_LANGUAGES = [
  {
    code: "en",
    name: "English",
    nativeName: "English",
    flag: "🇬🇧",
    speechCode: "en-IN",
    script: "Latin",
    fontFamily: "Inter, sans-serif"
  },
  {
    code: "te",
    name: "Telugu",
    nativeName: "తెలుగు",
    flag: "🇮🇳",
    speechCode: "te-IN",
    script: "Telugu",
    fontFamily: "'Noto Sans Telugu', sans-serif"
  },
  {
    code: "hi",
    name: "Hindi",
    nativeName: "हिन्दी",
    flag: "🇮🇳",
    speechCode: "hi-IN",
    script: "Devanagari",
    fontFamily: "'Noto Sans Devanagari', sans-serif"
  },
  {
    code: "pa",
    name: "Punjabi",
    nativeName: "ਪੰਜਾਬੀ",
    flag: "🇮🇳",
    speechCode: "pa-IN",
    script: "Gurmukhi",
    fontFamily: "'Noto Sans Gurmukhi', sans-serif"
  },
  {
    code: "ml",
    name: "Malayalam",
    nativeName: "മലയാളം",
    flag: "🇮🇳",
    speechCode: "ml-IN",
    script: "Malayalam",
    fontFamily: "'Noto Sans Malayalam', sans-serif"
  },
  {
    code: "ta",
    name: "Tamil",
    nativeName: "தமிழ்",
    flag: "🇮🇳",
    speechCode: "ta-IN",
    script: "Tamil",
    fontFamily: "'Noto Sans Tamil', sans-serif"
  },
  {
    code: "kn",
    name: "Kannada",
    nativeName: "ಕನ್ನಡ",
    flag: "🇮🇳",
    speechCode: "kn-IN",
    script: "Kannada",
    fontFamily: "'Noto Sans Kannada', sans-serif"
  }
];

const savedLanguage = localStorage.getItem("returnloop_lang") || "en";

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: en },
      te: { translation: te },
      hi: { translation: hi },
      pa: { translation: pa },
      ml: { translation: ml },
      ta: { translation: ta },
      kn: { translation: kn }
    },
    lng: savedLanguage,
    fallbackLng: "en",
    interpolation: {
      escapeValue: false // React already escapes XSS
    }
  });

// Apply document language attribute on initialization
if (typeof document !== "undefined") {
  document.documentElement.lang = savedLanguage;
}

export const setAppLanguage = (code) => {
  const langObj = SUPPORTED_LANGUAGES.find(l => l.code === code) || SUPPORTED_LANGUAGES[0];
  i18n.changeLanguage(langObj.code);
  localStorage.setItem("returnloop_lang", langObj.code);
  if (typeof document !== "undefined") {
    document.documentElement.lang = langObj.code;
  }
  return langObj;
};

export const getCurrentLanguage = () => {
  const currentCode = i18n.language || "en";
  return SUPPORTED_LANGUAGES.find(l => l.code === currentCode) || SUPPORTED_LANGUAGES[0];
};

export const getSpeechLocale = (code) => {
  const lang = SUPPORTED_LANGUAGES.find(l => l.code === (code || i18n.language));
  return lang ? lang.speechCode : "en-IN";
};

// Text-to-Speech synthesis helper with graceful fallbacks
export const speakText = (text, customLocale = null) => {
  if (!("speechSynthesis" in window)) {
    console.warn("Speech synthesis is not supported in this browser.");
    return false;
  }

  window.speechSynthesis.cancel(); // Stop any ongoing utterance
  const utterance = new SpeechSynthesisUtterance(text);
  const locale = customLocale || getSpeechLocale();
  utterance.lang = locale;
  utterance.rate = 0.95; // Slightly slower for clear multi-lingual pronunciation

  // Try finding voice matching current language
  const voices = window.speechSynthesis.getVoices();
  const matchedVoice = voices.find(v => v.lang.startsWith(locale.split("-")[0]));
  if (matchedVoice) {
    utterance.voice = matchedVoice;
  }

  window.speechSynthesis.speak(utterance);
  return true;
};

// Stop speech synthesis
export const stopSpeaking = () => {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
};

export default i18n;

