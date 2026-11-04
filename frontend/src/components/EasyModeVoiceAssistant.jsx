import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { 
  Volume2, VolumeX, Mic, MicOff, Accessibility, 
  Sparkles, CheckCircle2, AlertCircle, X, HelpCircle
} from "lucide-react";
import { getCurrentLanguage, speakText, stopSpeaking, getSpeechLocale } from "../i18n";

export const EasyModeVoiceAssistant = ({ onSpeechInput = null, pageContextText = "" }) => {
  const { t, i18n } = useTranslation();
  const currentLang = getCurrentLanguage();

  const [easyModeActive, setEasyModeActive] = useState(() => {
    return localStorage.getItem("returnloop_easymode") === "true";
  });
  const [panelOpen, setPanelOpen] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [listening, setListening] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(true);
  const [speechMessage, setSpeechMessage] = useState("");
  const [recognitionInstance, setRecognitionInstance] = useState(null);

  // Apply Easy Mode class to body (larger text, higher contrast, enhanced touch targets)
  useEffect(() => {
    if (easyModeActive) {
      document.body.classList.add("easy-mode-active");
      localStorage.setItem("returnloop_easymode", "true");
    } else {
      document.body.classList.remove("easy-mode-active");
      localStorage.setItem("returnloop_easymode", "false");
    }
  }, [easyModeActive]);

  // Clean up speech on unmount
  useEffect(() => {
    return () => {
      stopSpeaking();
      if (recognitionInstance) {
        try {
          recognitionInstance.stop();
        } catch (e) {
          // quiet error
        }
      }
    };
  }, [recognitionInstance]);

  const toggleEasyMode = () => {
    setEasyModeActive(prev => !prev);
  };

  const handleSpeakInstructions = () => {
    if (speaking) {
      stopSpeaking();
      setSpeaking(false);
      return;
    }

    const locale = getSpeechLocale(i18n.language);
    const instructionText = pageContextText || `${t("home.heroTitle")}. ${t("home.heroSubtitle")}`;
    
    setSpeaking(true);
    const success = speakText(instructionText, locale);
    
    if (!success) {
      setSpeechMessage(t("easyMode.voiceNotSupported"));
      setSpeaking(false);
      return;
    }

    // Auto-reset speaking state after approximate duration or speech end
    setTimeout(() => {
      setSpeaking(false);
    }, Math.min(Math.max(instructionText.length * 80, 4000), 15000));
  };

  const handleStartVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSpeechSupported(false);
      setSpeechMessage(t("easyMode.voiceNotSupported"));
      return;
    }

    if (listening) {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
      setListening(false);
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      const locale = getSpeechLocale(i18n.language);
      recognition.lang = locale;
      recognition.continuous = false;
      recognition.interimResults = false;

      recognition.onstart = () => {
        setListening(true);
        setSpeechMessage(t("easyMode.listening"));
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setListening(false);
        setSpeechMessage(`"${transcript}"`);
        if (onSpeechInput) {
          onSpeechInput(transcript);
        }
      };

      recognition.onerror = (event) => {
        console.warn("Speech recognition error:", event.error);
        setListening(false);
        if (event.error === "no-speech") {
          setSpeechMessage("No speech detected. Please try again.");
        } else if (event.error === "not-allowed") {
          setSpeechMessage("Microphone permission denied.");
        } else {
          setSpeechMessage(`Voice input: ${event.error}`);
        }
      };

      recognition.onend = () => {
        setListening(false);
      };

      recognition.start();
      setRecognitionInstance(recognition);
    } catch (err) {
      setSpeechSupported(false);
      setSpeechMessage(t("easyMode.voiceNotSupported"));
    }
  };

  return (
    <>
      {/* Floating Accessibility / Easy Mode Toggle Button */}
      <div className="fixed bottom-20 right-4 sm:bottom-6 sm:right-6 z-40 flex flex-col items-end gap-2">
        {easyModeActive && (
          <div className="animate-in fade-in slide-in-from-bottom-2 bg-amber-500 text-slate-950 px-3 py-1 rounded-full text-[11px] font-black shadow-lg flex items-center gap-1.5 border border-amber-300">
            <Sparkles className="w-3.5 h-3.5" />
            <span>{t("easyMode.activeTag")}</span>
          </div>
        )}

        <button
          type="button"
          onClick={() => setPanelOpen(true)}
          className={`p-3 sm:p-3.5 rounded-full shadow-xl transition-all transform hover:scale-105 active:scale-95 flex items-center justify-center cursor-pointer border ${
            easyModeActive
              ? "bg-amber-400 text-slate-950 border-amber-500 ring-4 ring-amber-300/40"
              : "bg-slate-900 text-white border-slate-700 hover:bg-slate-800"
          }`}
          title={t("easyMode.title")}
          aria-label={t("easyMode.title")}
        >
          <Accessibility className="w-5 h-5 sm:w-6 sm:h-6" />
        </button>
      </div>

      {/* Easy Mode & Voice Assistant Drawer / Modal */}
      {panelOpen && (
        <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-t-3xl sm:rounded-3xl max-w-md w-full shadow-2xl border border-slate-200 overflow-hidden flex flex-col max-h-[90vh] animate-in slide-in-from-bottom sm:zoom-in-95 duration-200">
            {/* Header */}
            <div className="px-6 py-5 border-b border-slate-100 flex items-center justify-between bg-slate-50">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-amber-100 text-amber-900 flex items-center justify-center font-bold">
                  <Accessibility className="w-5 h-5 text-amber-700" />
                </div>
                <div>
                  <h3 className="text-base font-extrabold text-slate-900">
                    {t("easyMode.title")}
                  </h3>
                  <p className="text-[11px] text-slate-500 font-medium">
                    Language: <span className="font-bold text-slate-800">{currentLang.nativeName}</span> ({currentLang.name})
                  </p>
                </div>
              </div>
              <button
                onClick={() => setPanelOpen(false)}
                className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-200/50 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Body */}
            <div className="p-6 space-y-5 overflow-y-auto">
              {/* Easy Mode Switch */}
              <div className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 flex items-center justify-between">
                <div>
                  <h4 className="text-sm font-bold text-slate-900">
                    {easyModeActive ? t("easyMode.toggleOff") : t("easyMode.toggleOn")}
                  </h4>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {t("easyMode.description")}
                  </p>
                </div>
                <button
                  type="button"
                  onClick={toggleEasyMode}
                  className={`w-14 h-8 flex items-center rounded-full p-1 transition cursor-pointer ${
                    easyModeActive ? "bg-amber-500" : "bg-slate-300"
                  }`}
                >
                  <div
                    className={`bg-white w-6 h-6 rounded-full shadow-md transform transition ${
                      easyModeActive ? "translate-x-6" : "translate-x-0"
                    }`}
                  />
                </button>
              </div>

              {/* Text-to-Speech Aloud */}
              <div className="p-4 rounded-2xl border border-blue-200 bg-blue-50/50 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Volume2 className="w-5 h-5 text-blue-600" />
                    <span className="text-xs font-bold text-blue-950 uppercase tracking-wider">
                      {t("easyMode.speakInstruction")}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono font-bold text-blue-800 bg-blue-100 px-2 py-0.5 rounded-full">
                    {currentLang.speechCode}
                  </span>
                </div>

                <p className="text-xs text-blue-900 leading-relaxed font-medium">
                  {speaking ? t("easyMode.speaking") : t("easyMode.voiceFallback", { lang: currentLang.nativeName })}
                </p>

                <button
                  type="button"
                  onClick={handleSpeakInstructions}
                  className={`w-full py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition cursor-pointer shadow-xs ${
                    speaking 
                      ? "bg-rose-600 hover:bg-rose-500 text-white" 
                      : "bg-blue-600 hover:bg-blue-500 text-white"
                  }`}
                >
                  {speaking ? (
                    <>
                      <VolumeX className="w-4 h-4" />
                      <span>{t("easyMode.stopSpeaking")}</span>
                    </>
                  ) : (
                    <>
                      <Volume2 className="w-4 h-4" />
                      <span>{t("easyMode.speakInstruction")} ({currentLang.nativeName})</span>
                    </>
                  )}
                </button>
              </div>

              {/* Speech Input / Microphone */}
              <div className="p-4 rounded-2xl border border-emerald-200 bg-emerald-50/50 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Mic className="w-5 h-5 text-emerald-600" />
                    <span className="text-xs font-bold text-emerald-950 uppercase tracking-wider">
                      {t("easyMode.voiceSearchTitle")}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded-full">
                    {currentLang.nativeName}
                  </span>
                </div>

                <p className="text-xs text-emerald-900 font-medium">
                  {t("easyMode.tapToSpeak", { lang: currentLang.nativeName })}
                </p>

                <button
                  type="button"
                  onClick={handleStartVoiceInput}
                  className={`w-full py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition cursor-pointer shadow-xs ${
                    listening 
                      ? "bg-rose-600 text-white animate-pulse" 
                      : "bg-emerald-600 hover:bg-emerald-500 text-white"
                  }`}
                >
                  {listening ? (
                    <>
                      <MicOff className="w-4 h-4" />
                      <span>{t("easyMode.listening")}</span>
                    </>
                  ) : (
                    <>
                      <Mic className="w-4 h-4" />
                      <span>Speak in {currentLang.nativeName}</span>
                    </>
                  )}
                </button>

                {speechMessage && (
                  <div className="p-2.5 rounded-xl bg-white border border-emerald-300 text-emerald-900 text-xs font-medium flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                    <span className="truncate">{speechMessage}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
              <button
                onClick={() => setPanelOpen(false)}
                className="px-5 py-2 rounded-xl bg-slate-900 text-white font-bold text-xs hover:bg-slate-800 transition"
              >
                {t("common.close")}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default EasyModeVoiceAssistant;

