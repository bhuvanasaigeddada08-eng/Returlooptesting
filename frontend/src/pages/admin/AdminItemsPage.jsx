import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { 
  Search, ShieldAlert, Filter, Eye, Edit, AlertCircle, 
  CheckCircle2, RefreshCw, X, Shield 
} from "lucide-react";
import api from "../../services/api";
import StatusBadge from "../../components/StatusBadge";
import Modal from "../../components/Modal";
import EmptyState from "../../components/EmptyState";
import { CATEGORIES } from "../../utils/constants";

export const AdminItemsPage = () => {
  const { t } = useTranslation();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  // Status Modal State
  const [selectedReport, setSelectedReport] = useState(null);
  const [newStatus, setNewStatus] = useState("");
  const [statusReason, setStatusReason] = useState("");
  const [statusUpdating, setStatusUpdating] = useState(false);
  const [statusError, setStatusError] = useState("");
  const [statusSuccess, setStatusSuccess] = useState("");

  const fetchReports = async () => {
    try {
      setLoading(true);
      const res = await api.getAdminReports({
        q: search,
        status: statusFilter,
        category: categoryFilter,
        type: typeFilter,
        page
      });
      setReports(res.reports || []);
      setTotalPages(res.pages || 1);
    } catch (err) {
      console.error("Failed to load admin reports:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, [search, statusFilter, categoryFilter, typeFilter, page]);

  const handleOpenStatusModal = (report) => {
    setSelectedReport(report);
    setNewStatus(report.status);
    setStatusReason("");
    setStatusError("");
    setStatusSuccess("");
  };

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    if (!selectedReport) return;
    setStatusError("");
    setStatusSuccess("");

    try {
      setStatusUpdating(true);
      await api.updateReportStatus(selectedReport.id, newStatus, statusReason);
      setStatusSuccess("Status updated successfully.");
      fetchReports();
      setTimeout(() => {
        setSelectedReport(null);
      }, 1200);
    } catch (err) {
      setStatusError(err.message || "Failed to update status");
    } finally {
      setStatusUpdating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">{t("explore.title")} - {t("admin.moderation") || "Moderation"}</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Review, update statuses, moderate inappropriate listings, or verify claims across the campus.
            </p>
          </div>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
          <div className="relative sm:col-span-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              placeholder={t("explore.searchPlaceholder")}
              className="w-full pl-9 pr-3 py-2 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <select
            value={typeFilter}
            onChange={(e) => { setTypeFilter(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-xl border border-slate-200 text-xs text-slate-700 bg-white"
          >
            <option value="">{t("explore.allTypes")}</option>
            <option value="lost">{t("explore.typeLost")}</option>
            <option value="found">{t("explore.typeFound")}</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-xl border border-slate-200 text-xs text-slate-700 bg-white"
          >
            <option value="">{t("common.status")}: {t("common.all")}</option>
            <option value="active">{t("common.status_active")}</option>
            <option value="claim_pending">{t("common.status_claim_pending")}</option>
            <option value="recovered">{t("common.status_recovered")}</option>
            <option value="withdrawn">{t("common.status_withdrawn")}</option>
          </select>

          <select
            value={categoryFilter}
            onChange={(e) => { setCategoryFilter(e.target.value); setPage(1); }}
            className="px-3 py-2 rounded-xl border border-slate-200 text-xs text-slate-700 bg-white"
          >
            <option value="">{t("explore.allCategories")}</option>
            {CATEGORIES.map(c => (
              <option key={c} value={c}>{t(`categories.${c}`, c)}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Reports Table */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">
            {t("common.loading")}...
          </div>
        ) : reports.length === 0 ? (
          <div className="p-12 text-center">
            <EmptyState
              title={t("explore.noItemsFound")}
              description={t("explore.noItemsDesc")}
            />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 font-semibold border-b border-slate-100">
                <tr>
                  <th className="py-3 px-4">{t("myItems.referenceCode")}</th>
                  <th className="py-3 px-4">{t("myItems.item")}</th>
                  <th className="py-3 px-4">{t("common.category")}</th>
                  <th className="py-3 px-4">{t("common.location")}</th>
                  <th className="py-3 px-4">{t("myItems.date")}</th>
                  <th className="py-3 px-4">{t("myItems.status")}</th>
                  <th className="py-3 px-4 text-right">{t("common.actions")}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {reports.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/60 transition">
                    <td className="py-3 px-4 font-mono font-bold text-[11px] text-slate-500">
                      {item.reference_code}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-semibold text-slate-900 line-clamp-1">{item.title}</div>
                      <span className={`text-[10px] font-bold uppercase tracking-wider ${
                        item.report_type === "lost" ? "text-rose-500" : "text-teal-600"
                      }`}>
                        {item.report_type === "lost" ? t("common.lostBelonging") : t("common.foundItem")}
                      </span>
                    </td>
                    <td className="py-3 px-4">{t(`categories.${item.category}`, item.category)}</td>
                    <td className="py-3 px-4">{t(`locations.${item.general_location}`, item.general_location)}</td>
                    <td className="py-3 px-4 text-slate-500">{item.event_date}</td>
                    <td className="py-3 px-4">
                      <StatusBadge status={item.status} />
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      <a
                        href={`/items/${item.id}`}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-[11px] transition"
                      >
                        <Eye className="w-3 h-3" /> {t("common.viewDetails")}
                      </a>
                      <button
                        onClick={() => handleOpenStatusModal(item)}
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 font-semibold text-[11px] transition cursor-pointer"
                      >
                        <Edit className="w-3 h-3" /> {t("common.edit")}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="p-4 border-t border-slate-100 flex justify-between items-center text-xs text-slate-500">
            <span>Page {page} of {totalPages}</span>
            <div className="flex gap-2">
              <button
                disabled={page <= 1}
                onClick={() => setPage(p => Math.max(1, p - 1))}
                className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 disabled:opacity-40"
              >
                ← {t("common.back")}
              </button>
              <button
                disabled={page >= totalPages}
                onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                className="px-3 py-1.5 rounded-lg border border-slate-200 text-slate-700 disabled:opacity-40"
              >
                →
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Edit Status Modal */}
      {selectedReport && (
        <Modal
          isOpen={!!selectedReport}
          onClose={() => setSelectedReport(null)}
          title={`Update Status: ${selectedReport.reference_code}`}
        >
          <form onSubmit={handleUpdateStatus} className="space-y-4">
            {statusError && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs">
                {statusError}
              </div>
            )}
            {statusSuccess && (
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs">
                {statusSuccess}
              </div>
            )}

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                {t("common.status")}
              </label>
              <select
                value={newStatus}
                onChange={(e) => setNewStatus(e.target.value)}
                className="w-full p-2.5 rounded-xl border border-slate-200 text-xs bg-white"
              >
                <option value="active">{t("common.status_active")}</option>
                <option value="claim_pending">{t("common.status_claim_pending")}</option>
                <option value="recovered">{t("common.status_recovered")}</option>
                <option value="withdrawn">{t("common.status_withdrawn")}</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Reason / Internal Admin Note:
              </label>
              <textarea
                rows={3}
                value={statusReason}
                onChange={(e) => setStatusReason(e.target.value)}
                placeholder="Audit log reason for this status modification..."
                className="w-full p-2.5 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setSelectedReport(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 text-xs font-semibold hover:bg-slate-50 cursor-pointer"
              >
                {t("common.cancel")}
              </button>
              <button
                type="submit"
                disabled={statusUpdating}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold disabled:opacity-60 cursor-pointer"
              >
                {statusUpdating ? t("common.loading") : t("common.save")}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default AdminItemsPage;
