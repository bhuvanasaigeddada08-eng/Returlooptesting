import React from "react";
import { Link, Outlet, useLocation, Navigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  LayoutDashboard, ShieldAlert, FileCheck2, History, ArrowLeft, Shield
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import Navbar from "../components/Navbar";
import BottomNav from "../components/BottomNav";

export const AdminLayout = () => {
  const { t } = useTranslation();
  const { user, isAdmin, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!isAdmin) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  const navItems = [
    { label: "Overview Metrics", path: "/admin", icon: LayoutDashboard },
    { label: "Item Moderation", path: "/admin/items", icon: ShieldAlert },
    { label: "Claim Reviews", path: "/admin/claims", icon: FileCheck2 },
    { label: "Audit Logs", path: "/admin/audit-logs", icon: History },
  ];

  const isActive = (path) => {
    if (path === "/admin") return location.pathname === "/admin";
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-100/70">
      <Navbar />

      <div className="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4 sm:py-6 pb-20 sm:pb-6 flex-1 flex flex-col">
        {/* Admin top banner */}
        <div className="bg-slate-900 text-white rounded-2xl p-4 sm:p-6 mb-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-blue-600/30 border border-blue-400/30 flex items-center justify-center text-blue-400">
              <Shield className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold">Campus Security & Moderation Hub</h1>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-blue-500/20 text-blue-300 border border-blue-500/30">
                  Admin Active
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-0.5">
                Review claims, inspect reports, audit handovers and maintain campus trust.
              </p>
            </div>
          </div>

          <Link
            to="/explore"
            className="flex items-center gap-1.5 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3.5 py-2 rounded-xl transition border border-slate-700"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Return to Campus View
          </Link>
        </div>

        {/* Tab Navigation */}
        <div className="flex overflow-x-auto gap-2 p-1.5 bg-white rounded-2xl border border-slate-200/80 shadow-sm mb-6 scrollbar-none">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.path);
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold whitespace-nowrap transition ${
                  active
                    ? "bg-slate-900 text-white shadow-sm"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <Outlet />
        </div>
      </div>
      <BottomNav />
    </div>
  );
};

export default AdminLayout;
