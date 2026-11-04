import React, { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  CheckCircle2, ArrowRight, ShieldCheck, MapPin, 
  Calendar, User, Mail, Phone, Hash, Clock, AlertCircle, Sparkles
} from "lucide-react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import { API_BASE_URL } from "../utils/constants";

export const ClaimSuccessPage = () => {
  const { t } = useTranslation();
  const { claimId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [claim, setClaim] = useState(null);
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const fetchClaimData = async () => {
      try {
        setLoading(true);
        const res = await api.getClaim(claimId);
        setClaim(res.claim);
        setItem(res.item);
      } catch (err) {
        setErrorMessage(err.message || "Failed to load claim details.");
      } finally {
        setLoading(false);
      }
    };
    if (claimId) {
      fetchClaimData();
    }
  }, [claimId]);

  if (loading) {
    return (
      <div className="min-h-[500px] flex items-center justify-center">
        <div className="w-10 h-10 border-4 border-slate-900 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (errorMessage || !claim) {
    return (
      <div className="max-w-md mx-auto py-10 px-4 text-center">
        <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm space-y-4">
          <AlertCircle className="w-12 h-12 text-rose-500 mx-auto" />
          <h2 className="text-lg font-bold text-slate-900">{t("common.error")}</h2>
          <p className="text-xs text-slate-500">{errorMessage || "Claim not found."}</p>
          <Link
            to="/my-claims"
            className="inline-block px-5 py-2.5 rounded-xl bg-slate-900 text-white font-bold text-xs"
          >
            {t("claimSuccess.myClaimsBtn")}
          </Link>
        </div>
      </div>
    );
  }

  // Determine current timeline status
  let activeStep = 2; // Default for 'pending' is Under Verification
  if (claim.status === "approved") {
    activeStep = 3;
  } else if (claim.status === "handover_completed") {
    activeStep = 4;
  } else if (claim.status === "rejected") {
    activeStep = -1; // rejected
  }

  // Format date
  const formattedDate = claim.created_at
    ? new Date(claim.created_at).toLocaleDateString("en-IN", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      })
    : "Recently submitted";

  const itemImage = item?.primary_image || claim.item_primary_image;
  const imageSrc = itemImage 
    ? (itemImage.startsWith("http") ? itemImage : `${API_BASE_URL}${itemImage}`)
    : null;

  const claimantName = claim.claimant_name || user?.display_name || "Student";
  const claimantEmail = claim.claimant_email || user?.email || "";
  const claimantPhone = claim.claimant_phone || user?.phone || "+91 98765 43210";
  const studentId = claim.claimant_student_id || user?.student_id || "12204918";

  return (
    <div className="max-w-md mx-auto py-2 sm:py-6">
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        {/* Screen 6 Header */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <button
            type="button"
            onClick={() => navigate("/my-claims")}
            className="text-xs font-semibold text-slate-700 hover:text-slate-900 transition cursor-pointer"
          >
            ← {t("nav.myClaims")}
          </button>
          <span className="text-sm font-bold text-slate-900">
            {t("common.confirmation")}
          </span>
          <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full font-mono">
            {t("common.active")}
          </span>
        </div>

        {/* Content Body */}
        <div className="p-5 sm:p-6 space-y-5">
          {/* Success Banner */}
          <div className="text-center space-y-2 pt-2">
            <div className="relative inline-block">
              <div className="w-20 h-20 rounded-full bg-emerald-50 border-2 border-emerald-400 flex items-center justify-center mx-auto text-emerald-600 shadow-xs">
                <CheckCircle2 className="w-12 h-12" />
              </div>
              <Sparkles className="w-5 h-5 text-amber-500 absolute -top-1 -right-1 animate-pulse" />
            </div>

            <h1 className="text-xl font-extrabold text-slate-900 tracking-tight pt-1">
              {t("claimSuccess.title")}
            </h1>
            <p className="text-xs text-slate-600 leading-relaxed max-w-xs mx-auto">
              {t("claimSuccess.subtitle")}
            </p>
          </div>

          {/* Claim Details Card */}
          <div className="rounded-2xl border border-slate-200 bg-slate-50/50 p-4 space-y-3">
            <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
                {t("claimSuccess.claimId")}
              </span>
              <span className="font-mono font-extrabold text-slate-900 text-sm">
                {claim.reference_code}
              </span>
            </div>

            {/* Item Info row */}
            <div className="flex items-center gap-3">
              <div className="w-14 h-14 rounded-xl bg-slate-200 border border-slate-200 overflow-hidden flex-shrink-0 flex items-center justify-center">
                {imageSrc ? (
                  <img 
                    src={imageSrc} 
                    alt={claim.item_title} 
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-slate-400 font-bold text-xs uppercase">
                    {claim.item_category?.slice(0, 3) || "IMG"}
                  </div>
                )}
              </div>
              <div className="min-w-0 flex-1">
                <h3 className="text-xs font-bold text-slate-900 truncate">
                  {claim.item_title}
                </h3>
                <p className="text-[11px] font-mono text-slate-500">
                  {t("claimSuccess.itemId")}: {claim.item_reference_code || "RL-FND-LPU"}
                </p>
                <p className="text-[11px] text-slate-500 flex items-center gap-1 mt-0.5 truncate">
                  <MapPin className="w-3 h-3 text-slate-400 flex-shrink-0" />
                  <span>{claim.item_location || item?.general_location || "Block 34 Helpdesk"}</span>
                </p>
              </div>
            </div>

            {/* Submission timestamp */}
            <div className="pt-2 border-t border-slate-200/60 flex items-center justify-between text-[11px]">
              <span className="text-slate-500 flex items-center gap-1">
                <Clock className="w-3 h-3 text-slate-400" /> {t("claimSuccess.submittedOn")}:
              </span>
              <span className="font-semibold text-slate-800">{formattedDate}</span>
            </div>
          </div>

          {/* Claimant Information Card */}
          <div className="rounded-2xl border border-slate-200 bg-white p-4 space-y-2.5">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800 mb-1 flex items-center gap-1.5">
              <User className="w-3.5 h-3.5 text-slate-500" />
              {t("claimSuccess.claimantInfo")}
            </h4>
            
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div>
                <span className="text-[10px] text-slate-400 block">{t("claimSuccess.studentName")}</span>
                <span className="font-bold text-slate-800 truncate block">{claimantName}</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-400 block">{t("claimSuccess.studentId")}</span>
                <span className="font-mono font-bold text-slate-800 block">{studentId}</span>
              </div>
              <div className="col-span-2">
                <span className="text-[10px] text-slate-400 block">{t("claimSuccess.email")}</span>
                <span className="font-semibold text-slate-700 truncate block">{claimantEmail}</span>
              </div>
              <div className="col-span-2">
                <span className="text-[10px] text-slate-400 block">{t("claimSuccess.phone")}</span>
                <span className="font-semibold text-slate-700 block">{claimantPhone}</span>
              </div>
            </div>
          </div>

          {/* Verification Status Timeline */}
          <div className="rounded-2xl border border-slate-200 bg-white p-4 space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800 flex items-center justify-between">
              <span>{t("claimSuccess.verificationStatus")}</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full font-bold uppercase bg-amber-50 text-amber-700 border border-amber-200">
                {claim.status === "approved" ? t("common.approved") : claim.status === "rejected" ? t("common.rejected") : t("common.underVerification")}
              </span>
            </h4>

            {/* 4-Stage Timeline */}
            <div className="relative pl-6 space-y-4 pt-1">
              <div className="absolute left-2.5 top-2 bottom-2 w-0.5 bg-slate-200" />

              {/* Step 1: Claim Submitted */}
              <div className="relative flex items-start gap-2.5">
                <div className="absolute -left-6 top-0.5 w-5 h-5 rounded-full bg-emerald-500 text-white flex items-center justify-center text-[10px] font-bold z-10">
                  ✓
                </div>
                <div>
                  <h5 className="text-xs font-bold text-slate-900">{t("claimSuccess.step1")}</h5>
                  <p className="text-[11px] text-slate-500">{t("claimSuccess.step1Desc")}</p>
                </div>
              </div>

              {/* Step 2: Under Verification */}
              <div className="relative flex items-start gap-2.5">
                <div className={`absolute -left-6 top-0.5 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold z-10 ${
                  activeStep >= 2 ? "bg-amber-500 text-white ring-4 ring-amber-100" : "bg-slate-300 text-slate-600"
                }`}>
                  {activeStep > 2 ? "✓" : "2"}
                </div>
                <div>
                  <h5 className={`text-xs font-bold ${activeStep >= 2 ? "text-amber-800" : "text-slate-500"}`}>
                    {t("claimSuccess.step2")}
                  </h5>
                  <p className="text-[11px] text-slate-500">{t("claimSuccess.step2Desc")}</p>
                </div>
              </div>

              {/* Step 3: Security Approval */}
              <div className="relative flex items-start gap-2.5">
                <div className={`absolute -left-6 top-0.5 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold z-10 ${
                  activeStep >= 3 ? "bg-emerald-500 text-white" : "bg-slate-200 text-slate-500"
                }`}>
                  {activeStep > 3 ? "✓" : "3"}
                </div>
                <div>
                  <h5 className={`text-xs font-bold ${activeStep >= 3 ? "text-slate-900" : "text-slate-500"}`}>
                    {t("claimSuccess.step3")}
                  </h5>
                  <p className="text-[11px] text-slate-400">{t("claimSuccess.step3Desc")}</p>
                </div>
              </div>

              {/* Step 4: Claim Finalized */}
              <div className="relative flex items-start gap-2.5">
                <div className={`absolute -left-6 top-0.5 w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold z-10 ${
                  activeStep >= 4 ? "bg-emerald-500 text-white" : "bg-slate-200 text-slate-500"
                }`}>
                  4
                </div>
                <div>
                  <h5 className={`text-xs font-bold ${activeStep >= 4 ? "text-slate-900" : "text-slate-500"}`}>
                    {t("claimSuccess.step4")}
                  </h5>
                  <p className="text-[11px] text-slate-400">{t("claimSuccess.step4Desc")}</p>
                </div>
              </div>
            </div>
          </div>

          {/* What's Next Card */}
          <div className="p-4 rounded-2xl bg-blue-50/70 border border-blue-200 text-xs text-blue-950 space-y-1">
            <h4 className="font-bold text-blue-900 flex items-center gap-1.5">
              <span role="img" aria-label="info">ℹ️</span> {t("claimSuccess.whatsNext")}
            </h4>
            <p className="text-[11px] text-blue-800 leading-relaxed font-medium">
              {t("claimSuccess.whatsNextDesc")}
            </p>
          </div>

          {/* Action Buttons */}
          <div className="space-y-2.5 pt-1">
            <button
              onClick={() => navigate("/my-claims")}
              className="w-full py-3.5 rounded-2xl bg-[#0f172a] hover:bg-slate-800 text-white font-bold text-xs tracking-wide transition shadow-sm hover:shadow flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>{t("claimSuccess.myClaimsBtn")}</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={() => navigate("/my-claims")}
              className="w-full py-3.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold text-xs tracking-wide transition border border-slate-200 flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>{t("claimSuccess.trackStatusBtn")}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClaimSuccessPage;
