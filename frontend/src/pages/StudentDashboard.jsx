import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  PlusCircle, HelpCircle, ShieldCheck, Sparkles, 
  FileText, Bell, CheckCircle2, ArrowRight, Clock, AlertCircle
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import ItemCard from "../components/ItemCard";
import StatusBadge from "../components/StatusBadge";
import EmptyState from "../components/EmptyState";
import { CardSkeleton } from "../components/LoadingSkeleton";

export const StudentDashboard = () => {
  const { t } = useTranslation();
  const { user } = useAuth();
  const [lostReports, setLostReports] = useState([]);
  const [foundReports, setFoundReports] = useState([]);
  const [claims, setClaims] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [lostRes, foundRes, claimsRes, notifRes] = await Promise.all([
          api.getMyReports("lost"),
          api.getMyReports("found"),
          api.getMyClaims(),
          api.getNotifications()
        ]);
        setLostReports(lostRes.reports || []);
        setFoundReports(foundRes.reports || []);
        setClaims(claimsRes.claims || []);
        setNotifications(notifRes.notifications || []);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, []);

  const totalReportsCount = lostReports.length + foundReports.length;
  const activeReportsCount = [...lostReports, ...foundReports].filter(
    r => r.status === "active" || r.status === "claim_pending"
  ).length;
  const recoveredCount = [...lostReports, ...foundReports].filter(
    r => r.status === "recovered"
  ).length;
  const pendingClaimsCount = claims.filter(c => c.status === "pending").length;

  return (
    <div className="space-y-8">
      {/* Welcome & Quick Action Header */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-2">
            <span>{t("nav.dashboard")}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {t("dashboard.welcome", { name: user?.display_name || "Student" })}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {t("dashboard.subtitle")}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link
            to="/report-lost"
            className="px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-xs transition flex items-center gap-2 shadow-sm"
          >
            <HelpCircle className="w-4 h-4" />
            {t("nav.reportLost")}
          </Link>
          <Link
            to="/report-found"
            className="px-4 py-2.5 rounded-xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-xs transition flex items-center gap-2 shadow-sm"
          >
            <ShieldCheck className="w-4 h-4" />
            {t("nav.reportFound")}
          </Link>
        </div>
      </div>

      {/* Real Statistics Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-xs font-medium text-slate-500">{t("dashboard.myLostReports")}</span>
          <p className="text-2xl font-bold text-slate-900">{loading ? "..." : lostReports.length}</p>
          <span className="text-[11px] text-slate-400">{t("nav.brandSub")}</span>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-xs font-medium text-slate-500">{t("dashboard.myFoundReports")}</span>
          <p className="text-2xl font-bold text-teal-600">{loading ? "..." : foundReports.length}</p>
          <span className="text-[11px] text-slate-400">{t("common.active")}</span>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-xs font-medium text-slate-500">{t("dashboard.activeClaims")}</span>
          <p className="text-2xl font-bold text-amber-600">{loading ? "..." : pendingClaimsCount}</p>
          <span className="text-[11px] text-slate-400">{t("common.underVerification")}</span>
        </div>

        <div className="p-5 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-1">
          <span className="text-xs font-medium text-slate-500">{t("common.recovered")}</span>
          <p className="text-2xl font-bold text-emerald-600">{loading ? "..." : recoveredCount}</p>
          <span className="text-[11px] text-slate-400">{t("common.finalized")}</span>
        </div>
      </div>

      {/* Main Grid: Reports & Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: My Lost & Found Reports */}
        <div className="lg:col-span-2 space-y-8">
          {/* Lost Reports Section */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <HelpCircle className="w-5 h-5 text-rose-500" />
                <h2 className="text-lg font-bold text-slate-900">{t("dashboard.myLostReports")}</h2>
                <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-semibold">
                  {lostReports.length}
                </span>
              </div>
              <Link to="/my-reports?tab=lost" className="text-xs font-semibold text-blue-600 hover:text-blue-800">
                {t("dashboard.viewAll")} →
              </Link>
            </div>

            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <CardSkeleton />
                <CardSkeleton />
              </div>
            ) : lostReports.length === 0 ? (
              <div className="p-6 text-center bg-white rounded-2xl border border-dashed border-slate-200">
                <p className="text-xs text-slate-500 mb-3">{t("dashboard.noReports")}</p>
                <Link
                  to="/report-lost"
                  className="px-3.5 py-1.5 rounded-lg bg-slate-900 text-white text-xs font-medium hover:bg-slate-800 transition"
                >
                  {t("home.reportLostBtn")}
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {lostReports.slice(0, 2).map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            )}
          </div>

          {/* Found Reports Section */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-teal-600" />
                <h2 className="text-lg font-bold text-slate-900">{t("dashboard.myFoundReports")}</h2>
                <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 font-semibold">
                  {foundReports.length}
                </span>
              </div>
              <Link to="/my-reports?tab=found" className="text-xs font-semibold text-blue-600 hover:text-blue-800">
                {t("dashboard.viewAll")} →
              </Link>
            </div>

            {loading ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <CardSkeleton />
                <CardSkeleton />
              </div>
            ) : foundReports.length === 0 ? (
              <div className="p-6 text-center bg-white rounded-2xl border border-dashed border-slate-200">
                <p className="text-xs text-slate-500 mb-3">{t("dashboard.noReports")}</p>
                <Link
                  to="/report-found"
                  className="px-3.5 py-1.5 rounded-lg bg-teal-600 text-white text-xs font-medium hover:bg-teal-700 transition"
                >
                  {t("home.reportFoundBtn")}
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {foundReports.slice(0, 2).map((item) => (
                  <ItemCard key={item.id} item={item} />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right Col: Active Claims & Recent Notifications */}
        <div className="space-y-6">
          {/* Claims Overview */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="font-bold text-slate-900 text-sm">{t("dashboard.activeClaims")}</h3>
              <Link to="/my-claims" className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                {t("dashboard.viewAll")}
              </Link>
            </div>

            {claims.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-4">{t("dashboard.noClaims")}</p>
            ) : (
              <div className="divide-y divide-slate-100">
                {claims.slice(0, 3).map((claim) => (
                  <div key={claim.id} className="py-3 first:pt-0 last:pb-0 space-y-1.5">
                    <div className="flex justify-between items-center">
                      <span className="font-mono text-[11px] text-slate-400 font-medium">
                        {claim.reference_code}
                      </span>
                      <StatusBadge status={claim.status} />
                    </div>
                    <Link
                      to={`/claims/success/${claim.id}`}
                      className="font-semibold text-xs text-slate-900 hover:text-blue-600 transition block truncate"
                    >
                      {claim.item_title}
                    </Link>
                    {claim.administrator_reason && (
                      <p className="text-[11px] text-slate-500 bg-slate-50 p-2 rounded-lg italic">
                        {claim.administrator_reason}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Notifications */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-1.5 font-bold text-slate-900 text-sm">
                <Bell className="w-4 h-4 text-blue-600" />
                <span>{t("notifications.title")}</span>
              </div>
              <Link to="/notifications" className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                {t("dashboard.viewAll")}
              </Link>
            </div>

            {notifications.length === 0 ? (
              <p className="text-xs text-slate-500 text-center py-4">{t("notifications.empty")}</p>
            ) : (
              <div className="space-y-3">
                {notifications.slice(0, 4).map((notif) => (
                  <div
                    key={notif.id}
                    className={`p-3 rounded-xl border text-xs transition ${
                      notif.is_read
                        ? "bg-slate-50/50 border-slate-100 text-slate-600"
                        : "bg-blue-50/60 border-blue-200/80 text-slate-800 font-medium"
                    }`}
                  >
                    <p className="font-semibold text-slate-900">{notif.title}</p>
                    <p className="text-[11px] text-slate-600 mt-0.5 line-clamp-2">{notif.message}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
