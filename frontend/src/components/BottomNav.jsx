import React, { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Search, Plus, FileText, Bell, User, 
  HelpCircle, ShieldCheck, X, Shield, LayoutDashboard 
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export const BottomNav = () => {
  const { t } = useTranslation();
  const location = useLocation();
  const { user, isAuthenticated, isAdmin } = useAuth();
  const [unreadCount, setUnreadCount] = useState(0);
  const [reportSheetOpen, setReportSheetOpen] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) return;
    const fetchUnread = async () => {
      try {
        const res = await api.getNotifications();
        setUnreadCount(res.unread_count || 0);
      } catch (e) {
        // quiet error
      }
    };
    fetchUnread();
    const interval = setInterval(fetchUnread, 30000);
    return () => clearInterval(interval);
  }, [isAuthenticated, location.pathname]);

  const isActive = (path) => {
    if (path === "/explore") return location.pathname === "/explore" || location.pathname === "/";
    if (path === "/my-reports") return location.pathname === "/my-reports";
    if (path === "/notifications") return location.pathname === "/notifications";
    if (path === "/dashboard") return location.pathname === "/dashboard" || location.pathname === "/profile";
    if (path === "/admin") return location.pathname.startsWith("/admin");
    return location.pathname === path;
  };

  return (
    <>
      {/* Bottom Sheet for Fast Mobile Reporting */}
      {reportSheetOpen && (
        <div className="mobile-bottom-nav fixed inset-0 z-50 sm:hidden flex flex-col justify-end">
          {/* Backdrop */}
          <div 
            onClick={() => setReportSheetOpen(false)} 
            className="fixed inset-0 bg-slate-900/60 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
          />

          {/* Action Sheet Card */}
          <div className="relative z-10 bg-white rounded-t-3xl border-t border-slate-200 p-6 space-y-4 shadow-2xl animate-in slide-in-from-bottom duration-250 pb-10">
            <div className="w-12 h-1.5 bg-slate-200 rounded-full mx-auto -mt-2 mb-2" />
            
            <div className="flex items-center justify-between pb-2 border-b border-slate-100">
              <div>
                <h3 className="text-base font-bold text-slate-900">{t("nav.whatToReport")}</h3>
                <p className="text-xs text-slate-500">{t("nav.fileReportSubtitle")}</p>
              </div>
              <button 
                onClick={() => setReportSheetOpen(false)}
                className="p-2 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100"
                aria-label="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-2">
              <Link
                to="/report-lost"
                onClick={() => setReportSheetOpen(false)}
                className="flex flex-col items-center justify-center p-4 rounded-2xl bg-rose-50 border border-rose-200/80 text-rose-700 hover:bg-rose-100 active:scale-98 transition text-center space-y-2"
              >
                <div className="w-12 h-12 rounded-xl bg-rose-600 text-white flex items-center justify-center shadow-md shadow-rose-600/20">
                  <HelpCircle className="w-6 h-6" />
                </div>
                <div>
                  <span className="font-bold text-sm block">{t("nav.reportLost")}</span>
                  <span className="text-[11px] text-rose-600/80">{t("home.step2Title") || "Search & match"}</span>
                </div>
              </Link>

              <Link
                to="/report-found"
                onClick={() => setReportSheetOpen(false)}
                className="flex flex-col items-center justify-center p-4 rounded-2xl bg-teal-50 border border-teal-200/80 text-teal-700 hover:bg-teal-100 active:scale-98 transition text-center space-y-2"
              >
                <div className="w-12 h-12 rounded-xl bg-teal-600 text-white flex items-center justify-center shadow-md shadow-teal-600/20">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <div>
                  <span className="font-bold text-sm block">{t("nav.reportFound")}</span>
                  <span className="text-[11px] text-teal-600/80">{t("home.step3Title") || "Safely deposit"}</span>
                </div>
              </Link>
            </div>
          </div>
        </div>
      )}

      {/* Main Bottom Navigation Bar */}
      <nav 
        className="mobile-bottom-nav fixed bottom-0 left-0 right-0 z-40 sm:hidden bg-white/95 backdrop-blur-md border-t border-slate-200/90 shadow-[0_-4px_25px_rgba(0,0,0,0.06)] select-none"
        style={{ paddingBottom: "max(env(safe-area-inset-bottom, 0px), 6px)" }}
        aria-label="Mobile Navigation"
      >
        <div className="grid grid-cols-5 h-16 items-center px-1">
          {/* 1. Explore Tab */}
          <Link
            to="/explore"
            className={`flex flex-col items-center justify-center py-1 transition ${
              isActive("/explore") ? "text-blue-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <div className="relative">
              <Search className={`w-5 h-5 ${isActive("/explore") ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
              {isActive("/explore") && (
                <span className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-blue-600 rounded-full" />
              )}
            </div>
            <span className="text-[10px] mt-1 tracking-tight">{t("nav.exploreShort")}</span>
          </Link>

          {/* 2. My Reports Tab */}
          <Link
            to={isAuthenticated ? "/my-claims" : "/login"}
            className={`flex flex-col items-center justify-center py-1 transition ${
              isActive("/my-claims") || isActive("/my-reports") ? "text-blue-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <div className="relative">
              <FileText className={`w-5 h-5 ${isActive("/my-claims") || isActive("/my-reports") ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
              {(isActive("/my-claims") || isActive("/my-reports")) && (
                <span className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-blue-600 rounded-full" />
              )}
            </div>
            <span className="text-[10px] mt-1 tracking-tight">{t("nav.myItems")}</span>
          </Link>

          {/* 3. Center Elevated + Report Button */}
          <div className="flex items-center justify-center -mt-5">
            <button
              onClick={() => setReportSheetOpen(true)}
              className="w-[52px] h-[52px] rounded-full bg-gradient-to-tr from-slate-900 via-blue-900 to-blue-600 text-white flex items-center justify-center shadow-lg shadow-blue-900/30 border-4 border-white hover:scale-105 active:scale-95 transition-transform"
              aria-label="Create Report"
            >
              <Plus className="w-6 h-6 stroke-[2.5]" />
            </button>
          </div>

          {/* 4. Notifications Tab */}
          <Link
            to={isAuthenticated ? "/notifications" : "/login"}
            className={`flex flex-col items-center justify-center py-1 transition relative ${
              isActive("/notifications") ? "text-blue-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <div className="relative">
              <Bell className={`w-5 h-5 ${isActive("/notifications") ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1.5 min-w-[16px] h-4 px-1 rounded-full bg-rose-500 text-white text-[9px] font-extrabold flex items-center justify-center border-2 border-white shadow-xs">
                  {unreadCount > 9 ? "9+" : unreadCount}
                </span>
              )}
              {isActive("/notifications") && (
                <span className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-blue-600 rounded-full" />
              )}
            </div>
            <span className="text-[10px] mt-1 tracking-tight">{t("nav.notifications")}</span>
          </Link>

          {/* 5. Account / Dashboard / Admin Tab */}
          <Link
            to={
              !isAuthenticated 
                ? "/login" 
                : isAdmin 
                ? "/admin" 
                : "/dashboard"
            }
            className={`flex flex-col items-center justify-center py-1 transition ${
              isActive(isAdmin ? "/admin" : "/dashboard") ? "text-blue-600 font-bold" : "text-slate-500 hover:text-slate-900"
            }`}
          >
            <div className="relative">
              {isAdmin ? (
                <Shield className={`w-5 h-5 ${isActive("/admin") ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
              ) : isAuthenticated ? (
                <LayoutDashboard className={`w-5 h-5 ${isActive("/dashboard") ? "stroke-[2.5]" : "stroke-[1.8]"}`} />
              ) : (
                <User className="w-5 h-5 stroke-[1.8]" />
              )}
              {(isActive("/dashboard") || isActive("/admin")) && (
                <span className="absolute -bottom-1 left-1/2 -translate-x-1/2 w-1.5 h-1.5 bg-blue-600 rounded-full" />
              )}
            </div>
            <span className="text-[10px] mt-1 tracking-tight">
              {isAdmin ? t("nav.adminPortal") : isAuthenticated ? t("nav.dashboardShort") : t("nav.signIn")}
            </span>
          </Link>
        </div>
      </nav>
    </>
  );
};

export default BottomNav;
