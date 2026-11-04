import React, { useState, useEffect } from "react";
import { History, Shield, Calendar, ArrowLeft, ArrowRight, User } from "lucide-react";
import api from "../../services/api";

export const AdminAuditLogsPage = () => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [total, setTotal] = useState(0);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const res = await api.getAuditLogs(page);
      setLogs(res.logs || []);
      setTotalPages(res.pages || 1);
      setTotal(res.total || 0);
    } catch (err) {
      console.error("Failed to load audit logs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [page]);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex justify-between items-center">
        <div>
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-blue-600" />
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">{t("admin.auditLogsTitle")}</h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Immutable log of all administrative status changes, moderation events, and handovers.
          </p>
        </div>
        <span className="text-xs text-slate-500 font-medium">
          Total Recorded: <strong className="text-slate-900">{total}</strong>
        </span>
      </div>

      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">{t("admin.loadingAudit")}</div>
        ) : logs.length === 0 ? (
          <div className="p-12 text-center text-xs text-slate-500">{t("admin.noAuditEvents")}</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-100">
                <tr>
                  <th className="py-3 px-4">{t("admin.timestamp")}</th>
                  <th className="py-3 px-4">{t("admin.actor")}</th>
                  <th className="py-3 px-4">{t("admin.action")}</th>
                  <th className="py-3 px-4">{t("admin.targetEntity")}</th>
                  <th className="py-3 px-4">Details / Parameters</th>
                  <th className="py-3 px-4">{t("admin.ipAddress")}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/60 transition">
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-500 whitespace-nowrap">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-900 whitespace-nowrap">
                      {log.actor_name}
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-[11px] text-blue-700 whitespace-nowrap">
                      {log.action}
                    </td>
                    <td className="py-3 px-4 whitespace-nowrap">
                      <span className="font-semibold text-slate-800">{log.target_type}</span>{" "}
                      <span className="text-slate-400">#{log.target_id}</span>
                    </td>
                    <td className="py-3 px-4 max-w-xs font-mono text-[11px] text-slate-600 truncate">
                      {log.details ? (typeof log.details === "object" ? JSON.stringify(log.details) : log.details) : "—"}
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-400">
                      {log.ip_address || "127.0.0.1"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center gap-2 pt-2">
          <button
            disabled={page <= 1}
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            className="px-3.5 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40"
          >
            ← Previous
          </button>
          <span className="text-xs font-medium text-slate-500 px-3">
            Page {page} of {totalPages}
          </span>
          <button
            disabled={page >= totalPages}
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            className="px-3.5 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40"
          >
            Next →
          </button>
        </div>
      )}
    </div>
  );
};

export default AdminAuditLogsPage;
