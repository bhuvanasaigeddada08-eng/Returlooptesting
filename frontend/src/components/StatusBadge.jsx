import React from "react";
import { useTranslation } from "react-i18next";
import { STATUS_COLORS } from "../utils/constants";

export const StatusBadge = ({ status, className = "" }) => {
  const { t } = useTranslation();
  const config = STATUS_COLORS[status] || {
    bg: "bg-slate-100 text-slate-700 border-slate-200",
    dot: "bg-slate-400",
    label: status || "Unknown"
  };

  const translatedLabel = t(`common.status_${status}`, config.label);

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${config.bg} ${className}`}
    >
      <span className={`w-1.5 h-1.5 rounded-full ${config.dot}`} />
      {translatedLabel}
    </span>
  );
};

export default StatusBadge;
