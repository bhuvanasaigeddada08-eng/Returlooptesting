import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  ClipboardList, Search, Clock, CheckCircle2, 
  XCircle, AlertCircle, ChevronRight, MapPin, 
  Plus, Bell, User, Filter, Eye, ShieldAlert
} from "lucide-react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import { API_BASE_URL } from "../utils/constants";

export const TrackClaimsPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("all"); // 'all', 'in_progress', 'approved', 'rejected'
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetchClaims();
  }, []);

  const fetchClaims = async () => {
    try {
      setLoading(true);
      const res = await api.getMyClaims();
      setClaims(res.claims || []);
    } catch (err) {
      setErrorMessage(err.message || "Failed to load claims.");
    } finally {
      setLoading(false);
    }
  };

  // Group counts
  const inProgressClaims = claims.filter(c => c.status === "pending");
  const approvedClaims = claims.filter(c => c.status === "approved" || c.status === "handover_completed");
  const rejectedClaims = claims.filter(c => c.status === "rejected" || c.status === "withdrawn");

  const filteredClaims = claims.filter(c => {
    if (activeTab === "in_progress") return c.status === "pending";
    if (activeTab === "approved") return c.status === "approved" || c.status === "handover_completed";
    if (activeTab === "rejected") return c.status === "rejected" || c.status === "withdrawn";
    return true; // 'all'
  });

  const getStatusBadge = (status) => {
    if (status === "approved" || status === "handover_completed") {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 flex items-center gap-1">
          <CheckCircle2 className="w-3 h-3" />
          {status === "handover_completed" ? t("trackClaims.claimFinalized") : t("trackClaims.claimApproved")}
        </span>
      );
    }
    if (status === "rejected") {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-300 flex items-center gap-1">
          <XCircle className="w-3 h-3" />
          {t("trackClaims.claimRejected")}
        </span>
      );
    }
    if (status === "withdrawn") {
      return (
        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-slate-100 text-slate-700 border border-slate-300">
          {t("common.withdrawn")}
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300 flex items-center gap-1">
        <Clock className="w-3 h-3" />
        {t("trackClaims.underVerification")}
      </span>
    );
  };

  return (
    <div className="max-w-md mx-auto py-2 sm:py-6 space-y-4">
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
        {/* Top Header */}
        <div className="px-5 py-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-slate-900 tracking-tight text-base">
              {t("nav.brand")} <span className="text-blue-600">LPU</span>
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Link
              to="/notifications"
              className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition"
              title={t("nav.notifications")}
            >
              <Bell className="w-4 h-4" />
            </Link>
            <Link
              to="/profile"
              className="p-2 rounded-xl text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition"
              title={t("nav.profile")}
            >
              <User className="w-4 h-4" />
            </Link>
          </div>
        </div>

        {/* Navy Hero Card: Track Your Claims */}
        <div className="m-4 p-5 rounded-2xl bg-[#0f172a] text-white shadow-md relative overflow-hidden">
          <div className="relative z-10 flex items-start justify-between">
            <div>
              <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-[10px] font-bold mb-2">
                <ClipboardList className="w-3 h-3" />
                <span>{t("trackClaims.portalTag")}</span>
              </div>
              <h1 className="text-xl font-black tracking-tight text-white">
                {t("trackClaims.title")}
              </h1>
              <p className="text-xs text-slate-300 mt-1 max-w-xs leading-relaxed">
                {t("trackClaims.subtitle")}
              </p>
            </div>
            <div className="w-10 h-10 rounded-2xl bg-white/10 flex items-center justify-center text-white flex-shrink-0">
              <ClipboardList className="w-5 h-5 text-blue-400" />
            </div>
          </div>
        </div>

        {/* Filter Tabs: 4 tabs with counts */}
        <div className="px-4 pb-2">
          <div className="grid grid-cols-4 gap-1 p-1 bg-slate-100 rounded-2xl text-[11px] font-bold">
            <button
              onClick={() => setActiveTab("all")}
              className={`py-2 px-1 rounded-xl transition text-center cursor-pointer ${
                activeTab === "all"
                  ? "bg-white text-slate-900 shadow-xs font-black"
                  : "text-slate-500 hover:text-slate-800"
              }`}
            >
              {t("trackClaims.allTab")} ({claims.length})
            </button>
            <button
              onClick={() => setActiveTab("in_progress")}
              className={`py-2 px-1 rounded-xl transition text-center cursor-pointer ${
                activeTab === "in_progress"
                  ? "bg-white text-amber-700 shadow-xs font-black"
                  : "text-slate-500 hover:text-slate-800"
              }`}
            >
              {t("trackClaims.inProgressTab")} ({inProgressClaims.length})
            </button>
            <button
              onClick={() => setActiveTab("approved")}
              className={`py-2 px-1 rounded-xl transition text-center cursor-pointer ${
                activeTab === "approved"
                  ? "bg-white text-emerald-700 shadow-xs font-black"
                  : "text-slate-500 hover:text-slate-800"
              }`}
            >
              {t("trackClaims.approvedTab")} ({approvedClaims.length})
            </button>
            <button
              onClick={() => setActiveTab("rejected")}
              className={`py-2 px-1 rounded-xl transition text-center cursor-pointer ${
                activeTab === "rejected"
                  ? "bg-white text-rose-700 shadow-xs font-black"
                  : "text-slate-500 hover:text-slate-800"
              }`}
            >
              {t("trackClaims.rejectedTab")} ({rejectedClaims.length})
            </button>
          </div>
        </div>

        {/* Claim Cards List */}
        <div className="p-4 space-y-3 flex-1 min-h-[250px]">
          {loading ? (
            <div className="py-12 flex flex-col items-center justify-center space-y-2">
              <div className="w-8 h-8 border-3 border-slate-900 border-t-transparent rounded-full animate-spin" />
              <p className="text-xs text-slate-400">{t("common.loading")}</p>
            </div>
          ) : filteredClaims.length === 0 ? (
            <div className="py-10 text-center space-y-3 bg-slate-50 rounded-2xl border border-dashed border-slate-200 p-6">
              <ClipboardList className="w-10 h-10 text-slate-300 mx-auto" />
              <h3 className="text-xs font-bold text-slate-700">{t("trackClaims.noClaimsTitle")}</h3>
              <p className="text-[11px] text-slate-400 max-w-xs mx-auto">
                {t("trackClaims.noClaimsDesc")}
              </p>
              <button
                onClick={() => navigate("/explore?type=found")}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 transition cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" />
                {t("trackClaims.browseFoundBtn")}
              </button>
            </div>
          ) : (
            filteredClaims.map((c) => {
              const imageSrc = c.item_primary_image
                ? (c.item_primary_image.startsWith("http") ? c.item_primary_image : `${API_BASE_URL}${c.item_primary_image}`)
                : null;
              
              const formattedDate = c.created_at
                ? new Date(c.created_at).toLocaleDateString("en-IN", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric"
                  })
                : "Recent";

              return (
                <div
                  key={c.id}
                  onClick={() => navigate(`/claims/success/${c.id}`)}
                  className="p-4 rounded-2xl border border-slate-200 bg-white hover:border-slate-300 hover:shadow-xs transition cursor-pointer space-y-3 group"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-14 h-14 rounded-xl bg-slate-100 border border-slate-200 overflow-hidden flex-shrink-0 flex items-center justify-center">
                      {imageSrc ? (
                        <img 
                          src={imageSrc} 
                          alt={c.item_title} 
                          className="w-full h-full object-cover group-hover:scale-105 transition"
                        />
                      ) : (
                        <div className="text-slate-400 font-bold text-xs uppercase">
                          {c.item_category?.slice(0, 3) || "IMG"}
                        </div>
                      )}
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center justify-between gap-1">
                        <h3 className="text-xs font-bold text-slate-900 truncate">
                          {c.item_title}
                        </h3>
                        <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-700 transition flex-shrink-0" />
                      </div>
                      <p className="text-[11px] font-mono text-slate-500 mt-0.5">
                        {t("claimSuccess.claimId")}: <span className="font-bold text-slate-800">{c.reference_code}</span>
                      </p>
                      <p className="text-[10px] font-mono text-slate-400">
                        {t("claimSuccess.itemId")}: {c.item_reference_code || "RL-FND"}
                      </p>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                    <span className="text-slate-500">
                      {t("trackClaims.claimedOn")} {formattedDate}
                    </span>
                    {getStatusBadge(c.status)}
                  </div>
                </div>
              );
            })
          )}

          {/* Info Card: Note */}
          <div className="p-3.5 rounded-2xl bg-blue-50/70 border border-blue-200/80 text-blue-900 text-xs space-y-1">
            <p className="text-[11px] font-medium leading-relaxed">
              <span className="font-bold">{t("trackClaims.noteTitle")}:</span> {t("trackClaims.noteDesc")}
            </p>
          </div>

          {/* Bottom CTA: + Submit New Claim */}
          <div className="pt-2 pb-1">
            <button
              onClick={() => navigate("/explore?type=found")}
              className="w-full py-4 rounded-2xl bg-[#0f172a] hover:bg-slate-800 text-white font-bold text-xs tracking-wide transition shadow-sm hover:shadow flex items-center justify-center gap-2 cursor-pointer"
            >
              <Plus className="w-4 h-4" />
              <span>{t("trackClaims.submitNewClaimBtn")}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrackClaimsPage;
