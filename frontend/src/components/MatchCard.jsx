import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { ChevronDown, ChevronUp, Sparkles, MapPin, Calendar, Tag, AlertCircle } from "lucide-react";
import { API_BASE_URL } from "../utils/constants";
import useContentTranslation from "../utils/useContentTranslation";

export const MatchCard = ({ match, targetType }) => {
  const { t } = useTranslation();
  const [showBreakdown, setShowBreakdown] = useState(false);
  const { item, match_score, breakdown, disclaimer } = match;

  const isHighMatch = match_score >= 65;
  const isModerateMatch = match_score >= 40 && match_score < 65;

  const scoreColor = isHighMatch
    ? "text-teal-600 bg-teal-50 border-teal-200"
    : isModerateMatch
    ? "text-blue-600 bg-blue-50 border-blue-200"
    : "text-amber-600 bg-amber-50 border-amber-200";

  const imageUrl = item.primary_image
    ? (item.primary_image.startsWith("http") ? item.primary_image : `${API_BASE_URL}${item.primary_image}`)
    : null;

  const { getTranslated } = useContentTranslation({
    title: item.title
  });

  const displayTitle = getTranslated("title");

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-5 hover:shadow-md transition">
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div className="flex items-center gap-4">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt={displayTitle}
              className="w-16 h-16 rounded-xl object-cover border border-slate-200 flex-shrink-0"
            />
          ) : (
            <div className="w-16 h-16 rounded-xl bg-slate-100 border border-slate-200 flex items-center justify-center flex-shrink-0 text-slate-400">
              <Sparkles className="w-7 h-7 text-brand-500" />
            </div>
          )}

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="font-mono text-xs text-slate-400 font-medium">
                {item.reference_code}
              </span>
              <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
                {t(`categories.${item.category}`, item.category)}
              </span>
            </div>
            <h4 className="font-semibold text-slate-900 text-base leading-snug">
              {displayTitle}
            </h4>
            <div className="flex items-center gap-4 text-xs text-slate-500 mt-1">
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5" />
                {t(`locations.${item.general_location}`, item.general_location)}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="w-3.5 h-3.5" />
                {item.event_date}
              </span>
            </div>
          </div>
        </div>

        {/* Score and actions */}
        <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100">
          <div className={`px-3 py-1.5 rounded-xl border text-center ${scoreColor}`}>
            <span className="text-xs font-medium uppercase tracking-wider block">{t("common.matchScore")}</span>
            <span className="text-lg font-bold">{match_score}%</span>
          </div>

          <Link
            to={`/items/${item.id}`}
            className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition"
          >
            {t("common.inspectItem")}
          </Link>
        </div>
      </div>

      {/* Breakdown accordion toggle */}
      <div className="mt-4 pt-3 border-t border-slate-100">
        <button
          type="button"
          onClick={() => setShowBreakdown(!showBreakdown)}
          className="flex items-center justify-between w-full text-xs font-medium text-slate-500 hover:text-slate-800 transition"
        >
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-500" />
            {t("common.whyMatched")}
          </span>
          {showBreakdown ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>

        {showBreakdown && (
          <div className="mt-3 p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 space-y-2 animate-in fade-in duration-150">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div className="p-2 bg-white rounded-lg border border-slate-100">
                <span className="font-semibold text-slate-900">{t("common.category")} (35%):</span>{" "}
                <span className="text-slate-600">{breakdown?.category?.detail}</span>
              </div>
              <div className="p-2 bg-white rounded-lg border border-slate-100">
                <span className="font-semibold text-slate-900">Keywords (25%):</span>{" "}
                <span className="text-slate-600">{breakdown?.keywords?.detail}</span>
              </div>
              <div className="p-2 bg-white rounded-lg border border-slate-100">
                <span className="font-semibold text-slate-900">{t("common.colorLabel")} (15%):</span>{" "}
                <span className="text-slate-600">{breakdown?.color?.detail}</span>
              </div>
              <div className="p-2 bg-white rounded-lg border border-slate-100">
                <span className="font-semibold text-slate-900">{t("common.location")} (15%):</span>{" "}
                <span className="text-slate-600">{breakdown?.location?.detail}</span>
              </div>
              <div className="p-2 bg-white rounded-lg border border-slate-100 sm:col-span-2">
                <span className="font-semibold text-slate-900">{t("common.date")} (10%):</span>{" "}
                <span className="text-slate-600">{breakdown?.date?.detail}</span>
              </div>
            </div>

            <p className="flex items-center gap-1.5 text-[11px] text-slate-500 italic pt-1">
              <AlertCircle className="w-3.5 h-3.5 text-amber-500 flex-shrink-0" />
              {disclaimer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchCard;
