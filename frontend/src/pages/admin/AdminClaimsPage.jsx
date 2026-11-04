import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { 
  FileCheck2, CheckCircle2, XCircle, HelpCircle, 
  User, Shield, Lock, AlertCircle, Calendar, Handshake 
} from "lucide-react";
import api from "../../services/api";
import StatusBadge from "../../components/StatusBadge";
import Modal from "../../components/Modal";
import EmptyState from "../../components/EmptyState";

export const AdminClaimsPage = () => {
  const { t } = useTranslation();
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");

  // Action Modals State
  const [selectedClaim, setSelectedClaim] = useState(null);
  const [actionType, setActionType] = useState(null); // 'approve' | 'reject' | 'request_info' | 'handover'
  const [actionReason, setActionReason] = useState("");
  const [handoverNotes, setHandoverNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const fetchClaims = async () => {
    try {
      setLoading(true);
      const res = await api.getAdminClaims({ status: statusFilter });
      setClaims(res.claims || []);
    } catch (err) {
      console.error("Failed to load claims:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, [statusFilter]);

  const handleOpenAction = (claim, type) => {
    setSelectedClaim(claim);
    setActionType(type);
    setActionReason("");
    setHandoverNotes("");
    setErrorMsg("");
    setSuccessMsg("");
  };

  const handleActionSubmit = async (e) => {
    e.preventDefault();
    if (!selectedClaim) return;
    setErrorMsg("");

    try {
      setSubmitting(true);
      if (actionType === "approve") {
        await api.approveClaim(selectedClaim.id, actionReason || "Proof verified against item traits.");
        setSuccessMsg("Claim approved! The student has been notified to proceed with physical verification.");
      } else if (actionType === "reject") {
        if (!actionReason.trim()) {
          setErrorMsg("Please supply an explanation for rejecting this claim.");
          setSubmitting(false);
          return;
        }
        await api.rejectClaim(selectedClaim.id, actionReason);
        setSuccessMsg("Claim rejected. The claimant has been informed.");
      } else if (actionType === "request_info") {
        if (!actionReason.trim()) {
          setErrorMsg("Please specify what additional proof is needed.");
          setSubmitting(false);
          return;
        }
        await api.requestClaimInfo(selectedClaim.id, actionReason);
        setSuccessMsg("Information request sent to claimant.");
      } else if (actionType === "handover") {
        await api.completeHandover(selectedClaim.id, handoverNotes || "Handover completed at campus security helpdesk.");
        setSuccessMsg("Item marked as officially handed over and closed.");
      }

      fetchClaims();
      setTimeout(() => {
        if (!errorMsg) {
          setActionType(null);
          setSelectedClaim(null);
        }
      }, 1500);
    } catch (err) {
      setErrorMsg(err.message || "Failed to process claim action.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Filter */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">{t("myItems.tabClaims")} & {t("common.status_handed_over")}</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Audit private ownership explanations, authorize verified claims, and record in-person handovers.
          </p>
        </div>

        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-3.5 py-2 rounded-xl border border-slate-200 bg-white text-xs text-slate-700"
        >
          <option value="">{t("common.all")} {t("myItems.tabClaims")}</option>
          <option value="pending">{t("common.pending")}</option>
          <option value="approved">{t("common.status_approved")}</option>
          <option value="handover_completed">{t("common.status_handed_over")}</option>
          <option value="rejected">{t("common.status_rejected")}</option>
        </select>
      </div>

      {/* Claims Grid */}
      <div className="space-y-4">
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500 bg-white rounded-3xl border border-slate-200">
            {t("common.loading")}...
          </div>
        ) : claims.length === 0 ? (
          <EmptyState
            title={t("myItems.noClaims")}
            description={t("explore.noItemsDesc")}
          />
        ) : (
          claims.map((claim) => (
            <div
              key={claim.id}
              className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4 hover:border-slate-300 transition"
            >
              {/* Header */}
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-slate-400">{claim.reference_code}</span>
                  <StatusBadge status={claim.status} />
                  <span className="text-xs text-slate-400">• Ref: {claim.item_reference_code}</span>
                </div>
                <span className="text-[11px] text-slate-400">
                  {t("myItems.claimDate")}: {new Date(claim.created_at).toLocaleString()}
                </span>
              </div>

              {/* Body */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
                {/* Item & Claimant details */}
                <div className="space-y-3">
                  <div>
                    <span className="text-slate-400 block font-medium">{t("myItems.item")}:</span>
                    <a
                      href={`/items/${claim.item_report_id}`}
                      target="_blank"
                      rel="noreferrer"
                      className="font-bold text-slate-900 text-sm hover:text-blue-600 transition block"
                    >
                      {claim.item_title} ↗
                    </a>
                  </div>

                  <div>
                    <span className="text-slate-400 block font-medium">Claimant:</span>
                    <p className="font-semibold text-slate-800">{claim.claimant_name}</p>
                    <p className="text-slate-500">{claim.claimant_email}</p>
                    {claim.claimant_phone && (
                      <p className="text-slate-500">{claim.claimant_phone}</p>
                    )}
                  </div>
                </div>

                {/* Private ownership explanation submitted */}
                <div className="md:col-span-2 space-y-2 bg-amber-50/50 p-4 rounded-2xl border border-amber-200/60">
                  <span className="font-bold text-amber-900 flex items-center gap-1.5 text-xs">
                    <Lock className="w-3.5 h-3.5 text-amber-600" />
                    {t("claim.proofLabel")}:
                  </span>
                  <p className="text-slate-800 leading-relaxed whitespace-pre-line text-xs font-mono bg-white/70 p-3 rounded-xl border border-amber-100">
                    {claim.private_ownership_explanation}
                  </p>
                </div>
              </div>

              {/* Action Buttons Row */}
              <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-end gap-2">
                {claim.status === "pending" && (
                  <>
                    <button
                      onClick={() => handleOpenAction(claim, "approve")}
                      className="px-3.5 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition flex items-center gap-1.5 cursor-pointer"
                    >
                      <CheckCircle2 className="w-4 h-4" /> {t("common.status_approved")}
                    </button>
                    <button
                      onClick={() => handleOpenAction(claim, "reject")}
                      className="px-3.5 py-2 rounded-xl bg-rose-50 text-rose-700 hover:bg-rose-100 text-xs font-semibold transition flex items-center gap-1.5 cursor-pointer"
                    >
                      <XCircle className="w-4 h-4" /> {t("common.status_rejected")}
                    </button>
                  </>
                )}

                {claim.status === "approved" && (
                  <button
                    onClick={() => handleOpenAction(claim, "handover")}
                    className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center gap-1.5 shadow-sm cursor-pointer"
                  >
                    <Handshake className="w-4 h-4" /> Complete Physical Handover
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      {/* Action Modal */}
      {actionType && (
        <Modal
          isOpen={!!actionType}
          onClose={() => setActionType(null)}
          title={`Process Claim: ${actionType.toUpperCase()}`}
        >
          <form onSubmit={handleActionSubmit} className="space-y-4">
            {errorMsg && (
              <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs">
                {errorMsg}
              </div>
            )}
            {successMsg && (
              <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs">
                {successMsg}
              </div>
            )}

            {actionType === "handover" ? (
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Physical Verification Notes / Student ID Checked:
                </label>
                <textarea
                  rows={3}
                  value={handoverNotes}
                  onChange={(e) => setHandoverNotes(e.target.value)}
                  placeholder="Record ID verification details, date, and collecting student signature confirmation..."
                  className="w-full p-3 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            ) : (
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Decision Notes / Reason to Claimant:
                </label>
                <textarea
                  rows={3}
                  value={actionReason}
                  onChange={(e) => setActionReason(e.target.value)}
                  placeholder="Enter audit remarks or instructions for the student..."
                  className="w-full p-3 rounded-xl border border-slate-200 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            )}

            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={() => setActionType(null)}
                className="px-4 py-2 rounded-xl border border-slate-200 text-slate-600 text-xs font-semibold hover:bg-slate-50 cursor-pointer"
              >
                {t("common.cancel")}
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold disabled:opacity-60 cursor-pointer"
              >
                {submitting ? t("common.loading") : t("common.submit")}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  );
};

export default AdminClaimsPage;
