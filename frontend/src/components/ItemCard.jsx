import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { MapPin, Calendar, Tag, ShieldCheck, HelpCircle, ArrowRight } from "lucide-react";
import StatusBadge from "./StatusBadge";
import { API_BASE_URL } from "../utils/constants";
import useContentTranslation from "../utils/useContentTranslation";

export const ItemCard = ({ item }) => {
  const { t } = useTranslation();
  const isLost = item.report_type === "lost";
  const imageUrl = item.primary_image 
    ? (item.primary_image.startsWith("http") ? item.primary_image : `${API_BASE_URL}${item.primary_image}`)
    : null;

  const { getTranslated } = useContentTranslation({
    title: item.title,
    description: item.description,
    brand: item.brand
  });

  const displayTitle = getTranslated("title");
  const displayDescription = getTranslated("description");
  const displayBrand = getTranslated("brand");

  return (
    <div className="group bg-white rounded-2xl border border-slate-200/80 shadow-sm hover:shadow-xl hover:shadow-slate-200/60 hover:-translate-y-1 hover:border-blue-200 transition-all duration-300 flex flex-col overflow-hidden">
      {/* Visual Header / Image Preview */}
      <div className="relative h-52 bg-slate-100 overflow-hidden flex items-center justify-center">
        {imageUrl ? (
          <>
            <img
              src={imageUrl}
              alt={displayTitle}
              className="w-full h-full object-cover group-hover:scale-108 transition-transform duration-500 ease-out"
            />
            {/* Subtle Gradient Shadow Overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/60 via-transparent to-black/20 pointer-events-none" />
          </>
        ) : (
          <div className="flex flex-col items-center justify-center text-slate-400 gap-2 p-6 text-center">
            {isLost ? (
              <div className="w-14 h-14 rounded-2xl bg-rose-50 border border-rose-100 flex items-center justify-center">
                <HelpCircle className="w-7 h-7 text-rose-400" />
              </div>
            ) : (
              <div className="w-14 h-14 rounded-2xl bg-teal-50 border border-teal-100 flex items-center justify-center">
                <ShieldCheck className="w-7 h-7 text-teal-500" />
              </div>
            )}
            <span className="text-xs font-medium text-slate-400">{t("common.noPhoto")}</span>
          </div>
        )}

        {/* Report Type Badge */}
        <div className="absolute top-3 left-3">
          <span
            className={`px-3 py-1 rounded-full text-[11px] font-bold tracking-wide uppercase shadow-sm border backdrop-blur-md ${
              isLost
                ? "bg-rose-500/90 text-white border-rose-400/40"
                : "bg-emerald-600/90 text-white border-emerald-400/40"
            }`}
          >
            {isLost ? t("common.lostBelonging") : t("common.foundItem")}
          </span>
        </div>

        {/* Status Badge */}
        <div className="absolute top-3 right-3 shadow-sm">
          <StatusBadge status={item.status} className="bg-white/95 backdrop-blur-md shadow-sm" />
        </div>

        {/* Floating Reference Tag at bottom-right of image */}
        <div className="absolute bottom-2.5 right-3 px-2 py-0.5 rounded-md bg-black/60 backdrop-blur-md text-[10px] font-mono text-slate-200">
          {item.reference_code}
        </div>
      </div>

      {/* Content */}
      <div className="p-5 flex-1 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-2 text-xs font-semibold text-blue-600 mb-1.5">
            <Tag className="w-3.5 h-3.5 text-blue-500" />
            <span>{t(`categories.${item.category}`, item.category)}</span>
            {item.brand && (
              <>
                <span className="text-slate-300">•</span>
                <span className="text-slate-500 font-normal">{displayBrand}</span>
              </>
            )}
          </div>

          <h3 className="font-bold text-slate-900 text-base group-hover:text-blue-600 transition line-clamp-1 mb-2">
            {displayTitle}
          </h3>

          <p className="text-xs text-slate-600 line-clamp-2 mb-4 leading-relaxed">
            {displayDescription}
          </p>
        </div>

        <div>
          {/* Metadata chips */}
          <div className="space-y-1.5 pt-3 border-t border-slate-100 text-xs text-slate-500">
            <div className="flex items-center gap-2">
              <MapPin className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <span className="truncate text-slate-700 font-medium">{t(`locations.${item.general_location}`, item.general_location)}</span>
            </div>
            <div className="flex items-center gap-2">
              <Calendar className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
              <span>{item.event_date}</span>
            </div>
          </div>

          {/* Action button */}
          <Link
            to={`/items/${item.id}`}
            className="mt-4 flex items-center justify-center gap-1.5 w-full py-2.5 px-4 text-center rounded-xl bg-slate-900 hover:bg-blue-600 text-white text-xs font-semibold shadow-sm transition-all duration-200 group-hover:shadow-md cursor-pointer"
          >
            <span>{t("common.viewDetailsAndMatches")}</span>
            <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ItemCard;
