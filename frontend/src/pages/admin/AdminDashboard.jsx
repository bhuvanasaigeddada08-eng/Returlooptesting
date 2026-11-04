import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Shield, AlertTriangle, FileCheck, CheckCircle2, 
  HelpCircle, ShieldCheck, History, ArrowRight, TrendingUp 
} from "lucide-react";
import api from "../../services/api";
import StatusBadge from "../../components/StatusBadge";

export const AdminDashboard = () => {
  const { t } = useTranslation();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setLoading(true);
        const res = await api.getAdminDashboard();
        setData(res);
      } catch (err) {
        console.error("Failed to load admin metrics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  if (loading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const metrics = data?.metrics || {};
  const categories = data?.category_breakdown || {};
  const recentReports = data?.recent_reports || [];
  const recentClaims = data?.recent_claims || [];
  const recentLogs = data?.recent_logs || [];

  return (
    <div className="space-y-8">
      {/* Metric Cards Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-6 gap-4">
        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">{t("admin.totalReports") || "Total Reports"}</span>
          <p className="text-2xl font-bold text-slate-900">{metrics.total_reports || 0}</p>
          <span className="text-[11px] text-slate-500">All-time recorded</span>
        </div>

        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-rose-500">{t("common.lostBelonging")}</span>
          <p className="text-2xl font-bold text-rose-600">{metrics.active_lost || 0}</p>
          <span className="text-[11px] text-slate-500">{t("common.status_active")}</span>
        </div>

        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-600">{t("common.foundItem")}</span>
          <p className="text-2xl font-bold text-teal-600">{metrics.active_found || 0}</p>
          <span className="text-[11px] text-slate-500">{t("common.status_active")}</span>
        </div>

        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-amber-500">{t("common.status_claim_pending")}</span>
          <p className="text-2xl font-bold text-amber-600">{metrics.pending_claims || 0}</p>
          <span className="text-[11px] text-slate-500">{t("common.pending")}</span>
        </div>

        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-600">{t("common.status_recovered")}</span>
          <p className="text-2xl font-bold text-emerald-600">{metrics.completed_recoveries || 0}</p>
          <span className="text-[11px] text-slate-500">{t("common.status_handed_over")}</span>
        </div>

        <div className="p-4 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-rose-500">{t("common.status_withdrawn")}</span>
          <p className="text-2xl font-bold text-slate-700">{metrics.suspended_reports || 0}</p>
          <span className="text-[11px] text-slate-500">Moderated / Hidden</span>
        </div>
      </div>

      {/* Category Breakdown & Pending Queue Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Category Breakdown */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-blue-600" />
            {t("common.category")}
          </h3>

          <div className="space-y-3 pt-2">
            {Object.keys(categories).length === 0 ? (
              <p className="text-xs text-slate-400">No category statistics yet.</p>
            ) : (
              Object.entries(categories).map(([cat, count]) => {
                const total = metrics.total_reports || 1;
                const pct = Math.round((count / total) * 100);
                return (
                  <div key={cat} className="space-y-1">
                    <div className="flex justify-between text-xs">
                      <span className="font-medium text-slate-700">{t(`categories.${cat}`, cat)}</span>
                      <span className="font-mono text-slate-500">{count} ({pct}%)</span>
                    </div>
                    <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-600 rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Recent Claims Awaiting Review */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
              <FileCheck className="w-4 h-4 text-teal-600" />
              {t("myItems.tabClaims")}
            </h3>
            <Link to="/admin/claims" className="text-xs font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1">
              {t("common.viewDetails")} <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {recentClaims.length === 0 ? (
            <p className="text-xs text-slate-400 py-6 text-center">{t("myItems.noClaims")}</p>
          ) : (
            <div className="divide-y divide-slate-100">
              {recentClaims.map((claim) => (
                <div key={claim.id} className="py-3 flex items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-slate-400">{claim.reference_code}</span>
                      <StatusBadge status={claim.status} />
                    </div>
                    <p className="text-xs font-semibold text-slate-900 mt-0.5">{claim.item_title}</p>
                    <p className="text-[11px] text-slate-500">Claimant: {claim.claimant_name || "Student"}</p>
                  </div>
                  <Link
                    to="/admin/claims"
                    className="px-3 py-1.5 rounded-xl border border-slate-200 text-xs font-semibold hover:bg-slate-50 transition"
                  >
                    {t("common.inspectItem")}
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Recent Audit Logs Strip */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-bold text-slate-900 text-sm flex items-center gap-2">
            <History className="w-4 h-4 text-slate-500" />
            Security & Administration Audit Trail
          </h3>
          <Link to="/admin/audit-logs" className="text-xs font-semibold text-blue-600 hover:text-blue-800">
            {t("common.viewDetails")} →
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-100">
              <tr>
                <th className="py-2.5 px-3">{t("common.date")}</th>
                <th className="py-2.5 px-3">Actor</th>
                <th className="py-2.5 px-3">{t("common.actions")}</th>
                <th className="py-2.5 px-3">Target</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {recentLogs.map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/50">
                  <td className="py-2.5 px-3 text-slate-400 font-mono text-[11px]">
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                  <td className="py-2.5 px-3 font-semibold text-slate-900">{log.actor_name}</td>
                  <td className="py-2.5 px-3 font-mono text-[11px] text-blue-700">{log.action}</td>
                  <td className="py-2.5 px-3 text-slate-500">{log.target_type} #{log.target_id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
