import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import api from "../services/api";

const memoryCache = {};

export function useContentTranslation(content = {}) {
  const { i18n } = useTranslation();
  const currentLang = i18n.language || "en";
  const [showOriginal, setShowOriginal] = useState(false);
  const [translatedData, setTranslatedData] = useState({});
  const [isTranslating, setIsTranslating] = useState(false);

  useEffect(() => {
    // If language is English, no translation needed
    if (currentLang === "en") {
      setTranslatedData({});
      return;
    }

    const textsToTranslate = [];
    const fields = Object.keys(content);

    fields.forEach((key) => {
      const val = content[key];
      if (typeof val === "string" && val.trim().length > 0) {
        const cacheKey = `${currentLang}::${val.trim()}`;
        if (!memoryCache[cacheKey]) {
          textsToTranslate.push(val.trim());
        }
      }
    });

    if (textsToTranslate.length === 0) {
      // All items cached
      const result = {};
      fields.forEach((key) => {
        const val = content[key];
        if (typeof val === "string") {
          const cacheKey = `${currentLang}::${val.trim()}`;
          result[key] = memoryCache[cacheKey] || val;
        } else {
          result[key] = val;
        }
      });
      setTranslatedData(result);
      return;
    }

    let isMounted = true;
    setIsTranslating(true);

    api.translateTexts(textsToTranslate, currentLang)
      .then((translations) => {
        if (!isMounted) return;
        Object.entries(translations || {}).forEach(([orig, trans]) => {
          memoryCache[`${currentLang}::${orig}`] = trans;
        });

        const result = {};
        fields.forEach((key) => {
          const val = content[key];
          if (typeof val === "string") {
            const cacheKey = `${currentLang}::${val.trim()}`;
            result[key] = memoryCache[cacheKey] || val;
          } else {
            result[key] = val;
          }
        });
        setTranslatedData(result);
      })
      .catch((err) => {
        console.warn("Content translation error:", err);
      })
      .finally(() => {
        if (isMounted) setIsTranslating(false);
      });

    return () => {
      isMounted = false;
    };
  }, [currentLang, JSON.stringify(content)]);

  const getTranslated = (key) => {
    if (showOriginal || currentLang === "en") {
      return content[key];
    }
    return translatedData[key] || content[key];
  };

  return {
    getTranslated,
    showOriginal,
    setShowOriginal,
    toggleOriginal: () => setShowOriginal((prev) => !prev),
    isTranslating,
    isTranslated: currentLang !== "en" && !showOriginal,
    currentLang
  };
}

export default useContentTranslation;

