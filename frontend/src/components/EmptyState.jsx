import React from "react";
import { SearchX } from "lucide-react";
import { Link } from "react-router-dom";

export const EmptyState = ({
  icon: Icon = SearchX,
  title = "No reports found",
  description = "Try adjusting your search criteria or filters to find what you are looking for.",
  actionText,
  actionLink,
  onAction
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center bg-white rounded-2xl border border-dashed border-slate-300 my-4 max-w-lg mx-auto">
      <div className="w-14 h-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-500 mb-4 shadow-sm">
        <Icon className="w-7 h-7 stroke-[1.5]" />
      </div>
      <h3 className="text-lg font-semibold text-slate-900 mb-1">{title}</h3>
      <p className="text-sm text-slate-600 mb-6 max-w-sm leading-relaxed">{description}</p>
      
      {actionLink && actionText && (
        <Link
          to={actionLink}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 text-white text-sm font-medium hover:bg-slate-800 transition shadow-sm hover:shadow"
        >
          {actionText}
        </Link>
      )}

      {onAction && actionText && (
        <button
          onClick={onAction}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 text-white text-sm font-medium hover:bg-slate-800 transition shadow-sm hover:shadow"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};

export default EmptyState;
