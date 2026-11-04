import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  ArrowLeft, Lock, ShieldCheck, AlertCircle, 
  CheckCircle2, Info, X
} from "lucide-react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";

export const ClaimItemPage = () => {
  const { t } = useTranslation();
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [ownershipExplanation, setOwnershipExplanation] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [privacyModalOpen, setPrivacyModalOpen] = useState(false);

  useEffect(() => {
    const fetchItem = async () => {
      try {
        setLoading(true);
        const res = await api.getReport(id);
        if (res.report.report_type !== "found") {
          setErrorMessage("Only found items can be claimed.");
        }
        if (res.report.user_id === user?.id) {
          setErrorMessage(t("claim.cannotClaimOwn"));
        }
        setItem(res.report);
      } catch (err) {
        setErrorMessage(err.message || "Failed to load item report.");
      } finally {
        setLoading(false);
      }
    };
    if (id) {
      fetchItem();
    }
  }, [id, user?.id, t]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    const explanation = ownershipExplanation.trim();
    if (!explanation) {
      setErrorMessage(t("claim.emptyProof"));
      return;
    }

    if (explanation.length < 15) {
      setErrorMessage(t("claim.emptyProof"));
      return;
    }

    try {
      setSubmitting(true);
      const res = await api.submitClaim(id, explanation);
      // Navigate directly to Screen 6 (Claim Submitted Successfully)
      navigate(`/claims/success/${res.claim.id}`);
    } catch (err) {
      if (err.message && err.message.toLowerCase().includes("duplicate")) {
        setErrorMessage(t("claim.duplicateClaim"));
      } else {
        setErrorMessage(err.message || t("common.error"));
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-slate-900 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto py-2 sm:py-6">
      {/* Mobile container card matching reference wireframe */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        {/* Screen 5 Header: Cancel | Submit Claim | Privacy */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="text-xs font-semibold text-slate-700 hover:text-slate-900 flex items-center gap-1 transition cursor-pointer"
          >
            ← {t("common.cancel")}
          </button>
          <span className="text-sm font-bold text-slate-900">
            {t("common.submit")}
          </span>
          <button
            type="button"
            onClick={() => setPrivacyModalOpen(true)}
            className="text-xs font-semibold text-slate-700 hover:text-slate-900 transition cursor-pointer"
          >
            {t("common.privacy")}
          </button>
        </div>

        {/* Form Body */}
        <div className="p-5 sm:p-6 space-y-5">
          {/* Heading */}
          <div>
            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight">
              {t("claim.confidentialTitle")}
            </h1>
            <p className="text-xs text-slate-600 mt-0.5">
              {t("claim.claimingItem", { title: item?.title || "Found Item" })}
              {item?.reference_code && (
                <span className="text-slate-400 font-mono text-[11px] ml-1.5">
                  ({item.reference_code})
                </span>
              )}
            </p>
          </div>

          {/* Zero-Leak Guarantee Card */}
          <div className="p-4 rounded-2xl border border-slate-200 bg-white shadow-xs">
            <div className="flex items-center gap-2 mb-1.5">
              <span className="text-base" role="img" aria-label="lock">🔒</span>
              <span className="text-xs font-bold text-slate-900">
                {t("claim.zeroLeakTitle")}
              </span>
            </div>
            <p className="text-[11px] text-slate-600 leading-relaxed">
              {t("claim.zeroLeakDesc")}
            </p>
          </div>

          {/* Error Message */}
          {errorMessage && (
            <div className="p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <div className="flex-1 font-medium">{errorMessage}</div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label 
                htmlFor="proof-textarea"
                className="block text-xs font-bold uppercase tracking-wider text-slate-800 mb-2"
              >
                {t("claim.privateProofLabel")}
              </label>
              <textarea
                id="proof-textarea"
                rows={6}
                required
                value={ownershipExplanation}
                onChange={(e) => setOwnershipExplanation(e.target.value)}
                placeholder={t("claim.privateProofPlaceholder")}
                className="w-full p-4 rounded-2xl border border-slate-300 text-xs sm:text-sm text-slate-800 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:border-slate-900 transition leading-relaxed resize-none shadow-xs"
              />
              <p className="text-[11px] text-slate-400 mt-1.5 flex items-center justify-between">
                <span>{t("claim.proofMinChars")}</span>
                <span>{ownershipExplanation.length} chars</span>
              </p>
            </div>

            {/* Next Step Upon Approval Card */}
            <div className="p-4 rounded-2xl border border-emerald-400 bg-emerald-50/40 text-emerald-950 shadow-xs">
              <h4 className="text-xs font-bold text-emerald-800 mb-1">
                {t("claim.nextStepTitle")}
              </h4>
              <p className="text-[11px] text-emerald-900 leading-relaxed font-medium">
                {t("claim.nextStepDesc", { 
                  location: item?.general_location ? `${item.general_location} Helpdesk` : "Block 34 Helpdesk" 
                })}
              </p>
            </div>

            {/* Bottom Button */}
            <div className="pt-2">
              <button
                type="submit"
                disabled={submitting || (item && item.user_id === user?.id)}
                className="w-full py-4 rounded-2xl bg-[#0f172a] hover:bg-slate-800 active:bg-slate-950 text-white font-bold text-sm tracking-wide transition shadow-md hover:shadow-lg flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {submitting ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    <span>{t("claim.submittingClaim")}</span>
                  </>
                ) : (
                  <span>{t("claim.submitClaimBtn")}</span>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Privacy Guarantee Modal */}
      {privacyModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 space-y-4 shadow-2xl border border-slate-200">
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-emerald-600" />
                <h3 className="font-bold text-slate-900 text-sm">{t("claim.privacyModalTitle")}</h3>
              </div>
              <button 
                onClick={() => setPrivacyModalOpen(false)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            
            <p className="text-xs text-slate-600 leading-relaxed">
              {t("claim.privacyModalDesc")}
            </p>
            <ul className="text-xs text-slate-600 space-y-2 list-disc list-inside">
              <li>{t("claim.privacyPoint1")}</li>
              <li>{t("claim.privacyPoint2")}</li>
              <li>{t("claim.privacyPoint3")}</li>
            </ul>

            <button
              onClick={() => setPrivacyModalOpen(false)}
              className="w-full py-2.5 rounded-xl bg-slate-900 text-white font-bold text-xs cursor-pointer"
            >
              {t("claim.privacyUnderstood")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClaimItemPage;
