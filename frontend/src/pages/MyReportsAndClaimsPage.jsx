import React, { useState, useEffect } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  FileText, HelpCircle, ShieldCheck, CheckCircle2, 
  Trash2, Edit3, Eye, AlertCircle, Clock, ShieldAlert 
} from "lucide-react";
import api from "../services/api";
import StatusBadge from "../components/StatusBadge";
import EmptyState from "../components/EmptyState";
import ConfirmDialog from "../components/ConfirmDialog";
import { TableRowSkeleton } from "../components/LoadingSkeleton";
import { API_BASE_URL } from "../utils/constants";
import TranslatedText from "../components/TranslatedText";

export const MyReportsAndClaimsPage = () => {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const initialTab = searchParams.get("tab") || "lost"; // "lost" | "found" | "claims"
  const [activeTab, setActiveTab] = useState(initialTab);

  const [lostReports, setLostReports] = useState([]);
  const [foundReports, setFoundReports] = useState([]);
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modals / action states
  const [selectedReportId, setSelectedReportId] = useState(null);
  const [confirmWithdrawOpen, setConfirmWithdrawOpen] = useState(false);
  const [confirmRecoverOpen, setConfirmRecoverOpen] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [lostRes, foundRes, claimsRes] = await Promise.all([
        api.getMyReports("lost"),
        api.getMyReports("found"),
        api.getMyClaims()
      ]);
      setLostReports(lostRes.reports || []);
      setFoundReports(foundRes.reports || []);
      setClaims(claimsRes.claims || []);
    } catch (err) {
      console.error("Failed to load user records:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setSearchParams({ tab });
  };

  const handleWithdraw = async () => {
    if (!selectedReportId) return;
    try {
      setActionLoading(true);
      await api.withdrawReport(selectedReportId);
      setConfirmWithdrawOpen(false);
      fetchData();
    } catch (err) {
      alert(err.message || "Failed to withdraw");
    } finally {
      setActionLoading(false);
    }
  };

  const handleRecover = async () => {
    if (!selectedReportId) return;
    try {
      setActionLoading(true);
      await api.recoverReport(selectedReportId);
      setConfirmRecoverOpen(false);
      fetchData();
    } catch (err) {
      alert(err.message || "Failed to mark recovered");
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm">
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{t("myItems.title")}</h1>
        <p className="text-xs text-slate-500 mt-1">
          {t("myItems.subtitle")}
        </p>

        {/* Tab Controls */}
        <div className="flex gap-2 pt-6 border-b border-slate-100 overflow-x-auto no-scrollbar">
          <button
            onClick={() => handleTabChange("lost")}
            className={`pb-3 px-4 text-xs font-bold transition border-b-2 flex items-center gap-2 whitespace-nowrap cursor-pointer ${
              activeTab === "lost"
                ? "border-rose-500 text-rose-600"
                : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            <HelpCircle className="w-4 h-4" />
            {t("myItems.tabLost")} ({lostReports.length})
          </button>

          <button
            onClick={() => handleTabChange("found")}
            className={`pb-3 px-4 text-xs font-bold transition border-b-2 flex items-center gap-2 whitespace-nowrap cursor-pointer ${
              activeTab === "found"
                ? "border-teal-600 text-teal-700"
                : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            {t("myItems.tabFound")} ({foundReports.length})
          </button>

          <button
            onClick={() => handleTabChange("claims")}
            className={`pb-3 px-4 text-xs font-bold transition border-b-2 flex items-center gap-2 whitespace-nowrap cursor-pointer ${
              activeTab === "claims"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-slate-500 hover:text-slate-800"
            }`}
          >
            <FileText className="w-4 h-4" />
            {t("myItems.tabClaims")} ({claims.length})
          </button>
        </div>
      </div>

      {/* Tab Content */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm overflow-hidden">
        {loading ? (
          <div className="space-y-4 py-8">
            <div className="h-6 bg-slate-200 rounded w-1/3 animate-pulse" />
            <div className="h-20 bg-slate-100 rounded-xl animate-pulse" />
            <div className="h-20 bg-slate-100 rounded-xl animate-pulse" />
          </div>
        ) : activeTab === "lost" ? (
          lostReports.length === 0 ? (
            <EmptyState
              icon={HelpCircle}
              title={t("myItems.noLost")}
              description={t("explore.noItemsDesc")}
              actionText={t("report.lostTitle")}
              actionLink="/report-lost"
            />
          ) : (
            <div className="divide-y divide-slate-100">
              {lostReports.map((report) => {
                const imgUrl = report.primary_image
                  ? (report.primary_image.startsWith("http") ? report.primary_image : `${API_BASE_URL}${report.primary_image}`)
                  : null;
                return (
                  <div
                    key={report.id}
                    className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 group"
                  >
                    <div className="flex items-center gap-3.5">
                      {/* Photo Thumbnail */}
                      <div className="w-16 h-16 rounded-xl bg-slate-100 overflow-hidden flex-shrink-0 border border-slate-200/80 shadow-sm flex items-center justify-center">
                        {imgUrl ? (
                          <img src={imgUrl} alt={report.title} className="w-full h-full object-cover group-hover:scale-105 transition" />
                        ) : (
                          <HelpCircle className="w-6 h-6 text-rose-300" />
                        )}
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-slate-400">{report.reference_code}</span>
                          <StatusBadge status={report.status} />
                          <span className="text-xs text-slate-400">• {t(`categories.${report.category}`, report.category)}</span>
                        </div>
                        <Link
                          to={`/items/${report.id}`}
                          className="font-bold text-slate-900 text-base hover:text-blue-600 transition block"
                        >
                          <TranslatedText text={report.title} />
                        </Link>
                        <p className="text-xs text-slate-500">
                          {t(`locations.${report.general_location}`, report.general_location)} • {report.event_date}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-center">
                      <Link
                        to={`/items/${report.id}`}
                        className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition text-xs font-semibold flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5" /> {t("common.viewDetails")}
                      </Link>

                      {report.status === "active" && (
                        <>
                          <button
                            onClick={() => {
                              setSelectedReportId(report.id);
                              setConfirmRecoverOpen(true);
                            }}
                            className="px-3 py-1.5 rounded-xl bg-emerald-50 text-emerald-700 hover:bg-emerald-100 text-xs font-semibold transition cursor-pointer"
                          >
                            {t("common.markRecovered")}
                          </button>
                          <button
                            onClick={() => {
                              setSelectedReportId(report.id);
                              setConfirmWithdrawOpen(true);
                            }}
                            className="px-3 py-1.5 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 text-xs font-semibold transition cursor-pointer"
                          >
                            {t("common.withdrawReport")}
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )
        ) : activeTab === "found" ? (
          foundReports.length === 0 ? (
            <EmptyState
              icon={ShieldCheck}
              title={t("myItems.noFound")}
              description={t("explore.noItemsDesc")}
              actionText={t("report.foundTitle")}
              actionLink="/report-found"
            />
          ) : (
            <div className="divide-y divide-slate-100">
              {foundReports.map((report) => {
                const imgUrl = report.primary_image
                  ? (report.primary_image.startsWith("http") ? report.primary_image : `${API_BASE_URL}${report.primary_image}`)
                  : null;
                return (
                  <div
                    key={report.id}
                    className="py-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 group"
                  >
                    <div className="flex items-center gap-3.5">
                      {/* Photo Thumbnail */}
                      <div className="w-16 h-16 rounded-xl bg-slate-100 overflow-hidden flex-shrink-0 border border-slate-200/80 shadow-sm flex items-center justify-center">
                        {imgUrl ? (
                          <img src={imgUrl} alt={report.title} className="w-full h-full object-cover group-hover:scale-105 transition" />
                        ) : (
                          <ShieldCheck className="w-6 h-6 text-teal-400" />
                        )}
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-slate-400">{report.reference_code}</span>
                          <StatusBadge status={report.status} />
                          <span className="text-xs text-slate-400">• {t(`categories.${report.category}`, report.category)}</span>
                        </div>
                        <Link
                          to={`/items/${report.id}`}
                          className="font-bold text-slate-900 text-base hover:text-teal-600 transition block"
                        >
                          <TranslatedText text={report.title} />
                        </Link>
                        <p className="text-xs text-slate-500">
                          {t(`locations.${report.general_location}`, report.general_location)} • {report.event_date}
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 self-end sm:self-center">
                      <Link
                        to={`/items/${report.id}`}
                        className="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition text-xs font-semibold flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5" /> {t("common.viewDetails")}
                      </Link>

                      {report.status === "active" && (
                        <button
                          onClick={() => {
                            setSelectedReportId(report.id);
                            setConfirmWithdrawOpen(true);
                          }}
                          className="px-3 py-1.5 rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 text-xs font-semibold transition cursor-pointer"
                        >
                          {t("common.withdrawReport")}
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )
        ) : (
          /* Claims Tab */
          claims.length === 0 ? (
            <EmptyState
              icon={FileText}
              title={t("myItems.noClaims")}
              description={t("explore.noItemsDesc")}
              actionText={t("explore.title")}
              actionLink="/explore?type=found"
            />
          ) : (
            <div className="divide-y divide-slate-100">
              {claims.map((claim) => (
                <div key={claim.id} className="py-5 space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-slate-400">{claim.reference_code}</span>
                      <StatusBadge status={claim.status} />
                    </div>
                    <span className="text-[11px] text-slate-400">
                      {t("myItems.claimDate")}: {new Date(claim.created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div>
                    <h3 className="font-bold text-slate-900 text-base">
                      <TranslatedText text={claim.item_title} />
                    </h3>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2">
                      <span className="font-semibold text-slate-700">{t("claim.proofLabel")}:</span>{" "}
                      {claim.private_ownership_explanation}
                    </p>
                  </div>

                  {/* Admin feedback / handover notes */}
                  {claim.administrator_reason && (
                    <div className="p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 space-y-1">
                      <span className="font-semibold text-slate-900 block">{t("admin.remarks") || "Security Admin Remarks"}:</span>
                      <p>{claim.administrator_reason}</p>
                    </div>
                  )}

                  {claim.status === "approved" && (
                    <div className="p-3 rounded-xl bg-teal-50 border border-teal-200 text-xs text-teal-900 space-y-1">
                      <span className="font-bold flex items-center gap-1.5">
                        <CheckCircle2 className="w-4 h-4 text-teal-600" />
                        {t("claim.stepNotice")}
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )
        )}
      </div>

      {/* Confirmation Dialogs */}
      <ConfirmDialog
        isOpen={confirmWithdrawOpen}
        onClose={() => setConfirmWithdrawOpen(false)}
        onConfirm={handleWithdraw}
        title={t("common.withdrawTitle")}
        message={t("common.withdrawMsg")}
        confirmText={t("common.withdrawReport")}
        confirmVariant="danger"
        loading={actionLoading}
      />

      <ConfirmDialog
        isOpen={confirmRecoverOpen}
        onClose={() => setConfirmRecoverOpen(false)}
        onConfirm={handleRecover}
        title={t("common.markRecoveredTitle")}
        message={t("common.markRecoveredMsg")}
        confirmText={t("common.markRecovered")}
        confirmVariant="primary"
        loading={actionLoading}
      />
    </div>
  );
};

export default MyReportsAndClaimsPage;
