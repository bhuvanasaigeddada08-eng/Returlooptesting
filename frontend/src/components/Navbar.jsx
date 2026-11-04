import React, { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Search, PlusCircle, HelpCircle, ShieldCheck, 
  User, LogOut, Menu, X, LayoutDashboard, Bell, FileText, Globe
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import NotificationBell from "./NotificationBell";
import LogoIcon from "./LogoIcon";
import LanguageSelector from "./LanguageSelector";
import { SUPPORTED_LANGUAGES, setAppLanguage } from "../i18n";

export const Navbar = () => {
  const { t } = useTranslation();
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    setProfileDropdownOpen(false);
    setMobileMenuOpen(false);
    navigate("/");
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="sticky top-0 z-40 w-full glass-nav border-b border-slate-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group">
          <LogoIcon className="w-9 h-9 group-hover:scale-105 transition" />
          <div className="flex flex-col">
            <div className="flex items-center gap-1.5">
              <span className="font-extrabold text-slate-900 tracking-tight text-lg">
                {t("nav.brand")}<span className="text-blue-600"> LPU</span>
              </span>
              <span className="px-1.5 py-0.5 rounded bg-blue-100 text-blue-800 text-[10px] font-bold uppercase tracking-wider">
                LPU
              </span>
            </div>
            <span className="text-[10px] font-medium text-slate-400 hidden sm:inline -mt-0.5">
              {t("nav.brandSub")}
            </span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden sm:flex items-center gap-1">
          <Link
            to="/explore"
            className={`px-2.5 lg:px-3.5 py-2 rounded-xl text-xs lg:text-sm font-medium transition flex items-center gap-1.5 ${
              isActive("/explore")
                ? "bg-slate-900 text-white shadow-sm"
                : "text-slate-600 hover:text-slate-900 hover:bg-slate-100/70"
            }`}
          >
            <Search className="w-4 h-4" />
            <span className="hidden md:inline">{t("nav.explore")}</span>
            <span className="md:hidden">{t("nav.exploreShort")}</span>
          </Link>

          <Link
            to="/report-lost"
            className={`px-2.5 lg:px-3.5 py-2 rounded-xl text-xs lg:text-sm font-medium transition flex items-center gap-1.5 ${
              isActive("/report-lost")
                ? "bg-rose-600 text-white shadow-sm"
                : "text-slate-600 hover:text-rose-600 hover:bg-rose-50/70"
            }`}
          >
            <HelpCircle className="w-4 h-4" />
            <span className="hidden md:inline">{t("nav.reportLost")}</span>
            <span className="md:hidden">{t("nav.lostShort")}</span>
          </Link>

          <Link
            to="/report-found"
            className={`px-2.5 lg:px-3.5 py-2 rounded-xl text-xs lg:text-sm font-medium transition flex items-center gap-1.5 ${
              isActive("/report-found")
                ? "bg-teal-600 text-white shadow-sm"
                : "text-slate-600 hover:text-teal-600 hover:bg-teal-50/70"
            }`}
          >
            <ShieldCheck className="w-4 h-4" />
            <span className="hidden md:inline">{t("nav.reportFound")}</span>
            <span className="md:hidden">{t("nav.foundShort")}</span>
          </Link>

          {isAuthenticated && (
            <Link
              to="/dashboard"
              className={`px-2.5 lg:px-3.5 py-2 rounded-xl text-xs lg:text-sm font-medium transition flex items-center gap-1.5 ${
                isActive("/dashboard")
                  ? "bg-slate-900 text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-100/70"
              }`}
            >
              <LayoutDashboard className="w-4 h-4" />
              <span className="hidden md:inline">{t("nav.dashboard")}</span>
              <span className="md:hidden">{t("nav.dashboardShort")}</span>
            </Link>
          )}

          {isAdmin && (
            <Link
              to="/admin"
              className={`px-2.5 lg:px-3 py-1.5 rounded-xl text-[11px] lg:text-xs font-bold uppercase tracking-wider transition flex items-center gap-1 ml-1 border ${
                location.pathname.startsWith("/admin")
                  ? "bg-blue-600 text-white border-blue-700 shadow-sm"
                  : "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100"
              }`}
            >
              {t("nav.adminPortal")}
            </Link>
          )}
        </nav>

        {/* Right side icons & user profile */}
        <div className="hidden sm:flex items-center gap-2">
          {/* Language Selector in Header */}
          <LanguageSelector variant="pill" />

          {isAuthenticated ? (
            <>
              <NotificationBell />

              {/* Profile dropdown */}
              <div className="relative ml-1">
                <button
                  onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
                  className="flex items-center gap-2.5 p-1.5 pr-3 rounded-full border border-slate-200 bg-white hover:bg-slate-50 transition cursor-pointer"
                >
                  <div className="w-8 h-8 rounded-full bg-slate-900 text-white text-xs font-bold flex items-center justify-center">
                    {user?.display_name?.charAt(0).toUpperCase() || "U"}
                  </div>
                  <span className="text-xs font-semibold text-slate-700 max-w-[100px] truncate">
                    {user?.display_name?.split(" ")[0]}
                  </span>
                </button>

                {profileDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-slate-200 py-2 z-50 animate-in fade-in zoom-in-95 duration-150">
                    <div className="px-4 py-2 border-b border-slate-100">
                      <p className="text-xs font-bold text-slate-900 truncate">{user?.display_name}</p>
                      <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
                      <span className="inline-block mt-1 px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider bg-slate-100 text-slate-600">
                        {user?.role}
                      </span>
                    </div>

                    <Link
                      to="/dashboard"
                      onClick={() => setProfileDropdownOpen(false)}
                      className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 transition"
                    >
                      <LayoutDashboard className="w-4 h-4 text-slate-400" />
                      {t("nav.dashboard")}
                    </Link>

                    <Link
                      to="/my-claims"
                      onClick={() => setProfileDropdownOpen(false)}
                      className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 transition"
                    >
                      <FileText className="w-4 h-4 text-slate-400" />
                      {t("nav.myClaims")}
                    </Link>

                    <Link
                      to="/profile"
                      onClick={() => setProfileDropdownOpen(false)}
                      className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-slate-50 transition"
                    >
                      <User className="w-4 h-4 text-slate-400" />
                      {t("nav.profile")}
                    </Link>

                    {isAdmin && (
                      <Link
                        to="/admin"
                        onClick={() => setProfileDropdownOpen(false)}
                        className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-blue-700 bg-blue-50/50 hover:bg-blue-100/60 transition"
                      >
                        <ShieldCheck className="w-4 h-4 text-blue-600" />
                        {t("nav.adminPortal")}
                      </Link>
                    )}

                    <div className="pt-1 mt-1 border-t border-slate-100">
                      <button
                        onClick={handleLogout}
                        className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-rose-600 hover:bg-rose-50 w-full text-left transition cursor-pointer"
                      >
                        <LogOut className="w-4 h-4 text-rose-500" />
                        {t("nav.signOut")}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-4 py-2 rounded-xl text-xs font-semibold text-slate-700 hover:text-slate-900 hover:bg-slate-100 transition"
              >
                {t("nav.signIn")}
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 transition shadow-sm hover:shadow"
              >
                {t("nav.register")}
              </Link>
            </div>
          )}
        </div>

        {/* Mobile header controls */}
        <div className="flex sm:hidden items-center gap-2">
          <LanguageSelector variant="compact" />
          {isAuthenticated && <NotificationBell />}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition cursor-pointer"
            aria-label="Toggle Menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="sm:hidden border-t border-slate-200/80 bg-white/95 backdrop-blur-md px-4 pt-3 pb-6 space-y-2 animate-in slide-in-from-top duration-200">
          <Link
            to="/explore"
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-100"
          >
            <Search className="w-4 h-4 text-slate-400" /> {t("nav.explore")}
          </Link>
          <Link
            to="/report-lost"
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-rose-600 hover:bg-rose-50"
          >
            <HelpCircle className="w-4 h-4 text-rose-500" /> {t("nav.reportLost")}
          </Link>
          <Link
            to="/report-found"
            onClick={() => setMobileMenuOpen(false)}
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-teal-600 hover:bg-teal-50"
          >
            <ShieldCheck className="w-4 h-4 text-teal-500" /> {t("nav.reportFound")}
          </Link>

          {isAuthenticated ? (
            <>
              <Link
                to="/dashboard"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                <LayoutDashboard className="w-4 h-4 text-slate-400" /> {t("nav.dashboard")}
              </Link>
              <Link
                to="/my-claims"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                <FileText className="w-4 h-4 text-slate-400" /> {t("nav.myClaims")}
              </Link>
              <Link
                to="/profile"
                onClick={() => setMobileMenuOpen(false)}
                className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-100"
              >
                <User className="w-4 h-4 text-slate-400" /> {t("nav.profile")}
              </Link>
              {isAdmin && (
                <Link
                  to="/admin"
                  onClick={() => setMobileMenuOpen(false)}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-bold text-blue-700 bg-blue-50 hover:bg-blue-100"
                >
                  <ShieldCheck className="w-4 h-4 text-blue-600" /> {t("nav.adminPortal")}
                </Link>
              )}
              <div className="pt-2 border-t border-slate-100">
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-rose-600 hover:bg-rose-50 w-full text-left cursor-pointer"
                >
                  <LogOut className="w-4 h-4 text-rose-500" /> {t("nav.signOut")}
                </button>
              </div>
            </>
          ) : (
            <div className="pt-3 border-t border-slate-100 flex flex-col gap-2">
              <Link
                to="/login"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full py-2.5 text-center rounded-xl text-sm font-medium border border-slate-200 text-slate-700"
              >
                {t("nav.signIn")}
              </Link>
              <Link
                to="/register"
                onClick={() => setMobileMenuOpen(false)}
                className="w-full py-2.5 text-center rounded-xl text-sm font-medium bg-slate-900 text-white"
              >
                {t("nav.register")}
              </Link>
            </div>
          )}
          {/* Mobile Language Selector Grid */}
          <div className="pt-3 pb-1 border-t border-slate-100">
            <div className="text-[11px] font-bold text-slate-500 uppercase tracking-wider px-1 mb-2 flex items-center gap-1.5">
              <Globe className="w-3.5 h-3.5 text-blue-600" />
              <span>{t("home.selectLanguagePrompt") || "Choose Language / భాష"}</span>
            </div>
            <div className="grid grid-cols-2 gap-1.5">
              {SUPPORTED_LANGUAGES.map((lang) => {
                const active = (t && typeof t === "function" ? false : false) || (window.localStorage.getItem("returnloop_language") === lang.code) || (document.documentElement.lang === lang.code);
                return (
                  <button
                    key={lang.code}
                    type="button"
                    onClick={() => {
                      setAppLanguage(lang.code);
                      setMobileMenuOpen(false);
                    }}
                    className="px-2.5 py-1.5 rounded-xl text-xs font-bold flex items-center justify-between border border-slate-200 bg-white hover:bg-blue-50 text-slate-800 hover:text-blue-700 transition cursor-pointer"
                  >
                    <span className="flex items-center gap-1.5">
                      <span>{lang.flag}</span>
                      <span>{lang.nativeName}</span>
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
