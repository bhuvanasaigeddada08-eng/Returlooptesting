import React from "react";
import useContentTranslation from "../utils/useContentTranslation";

export const TranslatedText = ({ text, as: Component = "span", className = "" }) => {
  const { getTranslated } = useContentTranslation({ text });
  return <Component className={className}>{getTranslated("text") || text}</Component>;
};

export default TranslatedText;
