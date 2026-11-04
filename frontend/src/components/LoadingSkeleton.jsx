import React from "react";

export const CardSkeleton = () => (
  <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm animate-pulse flex flex-col gap-3">
    <div className="h-44 bg-slate-200 rounded-xl w-full" />
    <div className="flex justify-between items-center mt-1">
      <div className="h-4 bg-slate-200 rounded w-1/4" />
      <div className="h-4 bg-slate-200 rounded w-1/5" />
    </div>
    <div className="h-5 bg-slate-200 rounded w-3/4" />
    <div className="h-3.5 bg-slate-200 rounded w-full" />
    <div className="h-3.5 bg-slate-200 rounded w-2/3" />
    <div className="mt-3 pt-3 border-t border-slate-100 flex justify-between items-center">
      <div className="h-3 bg-slate-200 rounded w-1/3" />
      <div className="h-8 bg-slate-200 rounded-lg w-1/4" />
    </div>
  </div>
);

export const TableRowSkeleton = ({ cols = 5 }) => (
  <tr className="animate-pulse border-b border-slate-100">
    {Array.from({ length: cols }).map((_, i) => (
      <td key={i} className="py-4 px-4">
        <div className="h-4 bg-slate-200 rounded w-full" />
      </td>
    ))}
  </tr>
);

export default CardSkeleton;
