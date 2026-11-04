import React, { useState, useEffect } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  MapPin, Calendar, Tag, ShieldCheck, HelpCircle, 
  Sparkles, ArrowLeft, CheckCircle2, AlertTriangle, Shield, Eye, Globe
} from "lucide-react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import StatusBadge from "../components/StatusBadge";
import MatchCard from "../components/MatchCard";
import ConfirmDialog from "../components/ConfirmDialog";
import { API_BASE_URL } from "../utils/constants";
import useContentTranslation from "../utils/useContentTranslation";

export const ItemDetailsPage = () => {
  const { t, i18n } = useTranslation();
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated, isAdmin } = useAuth();

  const [report, setReport] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeImageIndex, setActiveImageIndex] = useState(0);
  const [actionLoading, setActionLoading] = useState(false);
  const [showWithdrawConfirm, setShowWithdrawConfirm] = useState(false);
  const [showRecoverConfirm, setShowRecoverConfirm] = useState(false);
  const [notificationMsg, setNotificationMsg] = useState("");

  const { getTranslated, showOriginal, toggleOriginal, isTranslating } = useContentTranslation(
    report ? {
      title: report.title,
      description: report.description,
      color: report.color,
      brand: report.brand,
      safe_handover_instructions: report.safe_handover_instructions
    } : {}
  );

  const fetchDetails = async () => {
    try {
      setLoading(true);
      const res = await api.getReport(id);
      setReport(res.report);

      // Fetch potential algorithmic matches
      try {
        const matchRes = await api.getMatches(id);
        setMatches(matchRes.matches || []);
      } catch (mErr) {
        console.warn("Matches fetch error:", mErr);
      }
    } catch (err) {
      console.error("Failed to load item:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetails();
  }, [id]);

  const isOwner = user && report && (user.id === report.user_id || isAdmin);
  const isFound = report?.report_type === "found";
  const isLost = report?.report_type === "lost";
  const canClaim = isAuthenticated && isFound && !isOwner && (report.status === "active" || report.status === "claim_pending");

  const handleMarkRecovered = async () => {
    try {
      setActionLoading(true);
      await api.recoverReport(id);
      setShowRecoverConfirm(false);
      setNotificationMsg(t("common.markRecoveredTitle") + " " + t("common.success"));
      fetchDetails();
    } catch (err) {
      alert(err.message || "Failed to update status");
    } finally {
      setActionLoading(false);
    }
  };

  const handleWithdraw = async () => {
    try {
      setActionLoading(true);
      await api.withdrawReport(id);
      setShowWithdrawConfirm(false);
      setNotificationMsg(t("common.withdrawTitle") + " " + t("common.success"));
      fetchDetails();
    } catch (err) {
      alert(err.message || "Failed to withdraw report");
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-[400px] flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!report) {
    return (
      <div className="p-12 text-center bg-white rounded-3xl border border-slate-200">
        <h2 className="text-xl font-bold text-slate-800">{t("common.reportNotFound")}</h2>
        <p className="text-xs text-slate-500 mt-2 mb-4">{t("common.listingRemoved")}</p>
        <Link to="/explore" className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold">
          {t("common.backToListings")}
        </Link>
      </div>
    );
  }

  const images = report.images || [];
  const primaryImageUrl = images.length > 0
    ? (images[activeImageIndex]?.file_path?.startsWith("http")
        ? images[activeImageIndex].file_path
        : `${API_BASE_URL}${images[activeImageIndex]?.file_path}`)
    : (report.primary_image
        ? (report.primary_image.startsWith("http") ? report.primary_image : `${API_BASE_URL}${report.primary_image}`)
        : null);

  const displayTitle = getTranslated("title");
  const displayDescription = getTranslated("description");
  const displayColor = getTranslated("color");
  const displayBrand = getTranslated("brand");
  const displayHandover = getTranslated("safe_handover_instructions");

  return (
    <div className="space-y-10">
      {/* Back button & Translation toggle indicator */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" /> {t("common.backToListings")}
        </button>

        {i18n.language !== "en" && (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-blue-50/80 border border-blue-200 text-xs text-blue-800">
            <Globe className="w-3.5 h-3.5 text-blue-600 animate-spin-slow" />
            <span>
              {isTranslating ? "Translating details..." : showOriginal ? "Showing original English" : "Details translated"}
            </span>
            <button
              type="button"
              onClick={toggleOriginal}
              className="ml-2 font-bold underline hover:text-blue-950 cursor-pointer"
            >
              {showOriginal ? "Show Translated" : "Show Original"}
            </button>
          </div>
        )}
      </div>

      {notificationMsg && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
          <span>{notificationMsg}</span>
        </div>
      )}

      {/* Main Details Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Image Viewer */}
        <div className="lg:col-span-1 space-y-4">
          <div className="h-72 sm:h-80 bg-slate-100 rounded-3xl border border-slate-200 overflow-hidden flex items-center justify-center relative shadow-sm">
            {primaryImageUrl ? (
              <img
                src={primaryImageUrl}
                alt={displayTitle}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="flex flex-col items-center justify-center text-slate-400 gap-2 p-6 text-center">
                {isLost ? (
                  <HelpCircle className="w-16 h-16 stroke-[1.2] text-rose-300" />
                ) : (
                  <ShieldCheck className="w-16 h-16 stroke-[1.2] text-teal-400" />
                )}
                <span className="text-xs font-medium text-slate-400">
                  {t("common.noPhoto")}
                </span>
              </div>
            )}

            <div className="absolute top-3 left-3">
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider text-white shadow-sm border ${
                  isLost ? "bg-rose-500 border-rose-600" : "bg-teal-600 border-teal-700"
                }`}
              >
                {isLost ? t("common.lostBelonging") : t("common.foundItem")}
              </span>
            </div>
          </div>

          {/* Thumbnail strip */}
          {images.length > 1 && (
            <div className="flex gap-2 overflow-x-auto pb-1">
              {images.map((img, idx) => (
                <button
                  key={img.id}
                  onClick={() => setActiveImageIndex(idx)}
                  className={`w-16 h-16 rounded-xl overflow-hidden border-2 flex-shrink-0 transition ${
                    activeImageIndex === idx ? "border-blue-600 scale-95" : "border-slate-200 hover:border-slate-300"
                  }`}
                >
                  <img
                    src={img.file_path.startsWith("http") ? img.file_path : `${API_BASE_URL}${img.file_path}`}
                    alt="Thumbnail"
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          )}

          {/* Privacy safe reporter information badge */}
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 text-xs text-slate-600 space-y-1">
            <span className="font-semibold text-slate-900 block">{t("common.reportedBy")}</span>
            <p>{report.reporter_name}</p>
            <p className="text-[11px] text-slate-400">
              {t("common.privacyProtected")}
            </p>
          </div>
        </div>

        {/* Right 2 Columns: Metadata & Actions */}
        <div className="lg:col-span-2 bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm flex flex-col justify-between space-y-6">
          <div className="space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-100">
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs font-bold text-slate-400 bg-slate-100 px-2.5 py-1 rounded-lg">
                  {report.reference_code}
                </span>
                <span className="text-xs font-semibold text-slate-600">
                  {t(`categories.${report.category}`, report.category)}
                </span>
              </div>
              <StatusBadge status={report.status} />
            </div>

            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              {displayTitle}
            </h1>

            {/* Description */}
            <div className="space-y-1">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">{t("reportFound.descriptionLabel", "Description")}</h4>
              <p className="text-sm text-slate-700 leading-relaxed whitespace-pre-line">
                {displayDescription}
              </p>
            </div>

            {/* Key Attributes Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 pt-4 border-t border-slate-100 text-xs">
              <div className="space-y-1">
                <span className="text-slate-400 block font-medium">{t("report.locationLabel")}</span>
                <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-blue-500" />
                  {t(`locations.${report.general_location}`, report.general_location)}
                </span>
              </div>

              <div className="space-y-1">
                <span className="text-slate-400 block font-medium">{t("report.dateLabel")}</span>
                <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-blue-500" />
                  {report.event_date}
                </span>
              </div>

              <div className="space-y-1">
                <span className="text-slate-400 block font-medium">{t("common.colorLabel")}</span>
                <span className="font-semibold text-slate-900">{displayColor}</span>
              </div>

              {report.brand && (
                <div className="space-y-1">
                  <span className="text-slate-400 block font-medium">{t("common.brandLabel")}</span>
                  <span className="font-semibold text-slate-900">{displayBrand}</span>
                </div>
              )}
            </div>

            {/* Safe Custody / Handover Instructions (Found Items) */}
            {report.safe_handover_instructions && (
              <div className="p-4 rounded-2xl bg-teal-50/70 border border-teal-200/80 text-xs space-y-1">
                <span className="font-bold text-teal-900 flex items-center gap-1.5">
                  <ShieldCheck className="w-4 h-4 text-teal-600" />
                  {t("common.custodyGuidance")}
                </span>
                <p className="text-teal-800 leading-relaxed">
                  {displayHandover}
                </p>
              </div>
            )}

            {/* Private characteristics visible ONLY to owner or admin */}
            {report.identifying_characteristics && (
              <div className="p-4 rounded-2xl bg-amber-50/70 border border-amber-200/80 text-xs space-y-1">
                <span className="font-bold text-amber-900 flex items-center gap-1.5">
                  <Shield className="w-4 h-4 text-amber-600" />
                  {t("common.privateDetailsAdminOnly")}
                </span>
                <p className="text-amber-800 leading-relaxed font-mono">
                  {report.identifying_characteristics}
                </p>
              </div>
            )}
          </div>

          {/* Action Row */}
          <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
            {canClaim ? (
              <Link
                to={`/claims/new/${report.id}`}
                className="w-full sm:w-auto px-6 py-2.5 sm:py-3 rounded-xl bg-teal-600 hover:bg-teal-500 active:scale-98 text-white font-semibold text-sm transition shadow-sm hover:shadow flex items-center justify-center gap-2"
              >
                <ShieldCheck className="w-4 h-4" />
                {t("common.claimThisBelonging")}
              </Link>
            ) : !isAuthenticated && isFound ? (
              <Link
                to="/login"
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-slate-900 text-white font-semibold text-xs hover:bg-slate-800 transition text-center justify-center flex items-center gap-2"
              >
                {t("common.signInToClaim")}
              </Link>
            ) : isOwner ? (
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 w-full sm:w-auto">
                {report.status !== "recovered" && (
                  <button
                    onClick={() => setShowRecoverConfirm(true)}
                    className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-xs transition flex items-center justify-center gap-1.5 shadow-sm active:scale-98 cursor-pointer"
                  >
                    <CheckCircle2 className="w-4 h-4" /> {t("common.markRecovered")}
                  </button>
                )}

                {report.status !== "withdrawn" && report.status !== "recovered" && (
                  <button
                    onClick={() => setShowWithdrawConfirm(true)}
                    className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-slate-300 text-slate-700 hover:bg-slate-50 font-semibold text-xs transition text-center active:scale-98 cursor-pointer"
                  >
                    {t("common.withdrawReport")}
                  </button>
                )}
              </div>
            ) : null}
          </div>
        </div>
      </div>

      {/* Potential Matches Section */}
      <section className="space-y-4 pt-6 border-t border-slate-200">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-brand-600" />
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">
            {t("common.potentialMatches")} ({matches.length})
          </h2>
        </div>
        <p className="text-xs text-slate-500">
          {t("common.heuristicDesc")}
        </p>

        {matches.length === 0 ? (
          <div className="p-8 text-center bg-white rounded-2xl border border-dashed border-slate-200">
            <p className="text-xs text-slate-500">
              {t("common.noMatchesFound")}
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {matches.map((m) => (
              <MatchCard key={m.item.id} match={m} targetType={report.report_type} />
            ))}
          </div>
        )}
      </section>

      {/* Confirmation Dialogs */}
      <ConfirmDialog
        isOpen={showRecoverConfirm}
        onClose={() => setShowRecoverConfirm(false)}
        onConfirm={handleMarkRecovered}
        title={t("common.markRecoveredTitle")}
        message={t("common.markRecoveredMsg")}
        confirmText={t("common.markRecovered")}
        confirmVariant="primary"
        loading={actionLoading}
      />

      <ConfirmDialog
        isOpen={showWithdrawConfirm}
        onClose={() => setShowWithdrawConfirm(false)}
        onConfirm={handleWithdraw}
        title={t("common.withdrawTitle")}
        message={t("common.withdrawMsg")}
        confirmText={t("common.withdrawReport")}
        confirmVariant="danger"
        loading={actionLoading}
      />
    </div>
  );
};

export default ItemDetailsPage;
