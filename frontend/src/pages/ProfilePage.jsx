import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  User, Lock, Mail, Phone, Bell, Shield, 
  CheckCircle2, AlertCircle, KeyRound, LogOut, Globe, Check
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import { SUPPORTED_LANGUAGES, setAppLanguage, getCurrentLanguage } from "../i18n";

export const ProfilePage = () => {
  const { t, i18n } = useTranslation();
  const { user, refreshUser, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const mustChangeInitial = location.state?.mustChange || user?.must_change_password;

  // Profile Form state
  const [displayName, setDisplayName] = useState(user?.display_name || "");
  const [phone, setPhone] = useState(user?.phone || "");
  const [selectedLanguage, setSelectedLanguage] = useState(i18n.language || "en");
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSuccess, setProfileSuccess] = useState("");
  const [profileError, setProfileError] = useState("");

  // Password Change state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordSuccess, setPasswordSuccess] = useState("");
  const [passwordError, setPasswordError] = useState("");

  // Notification Preferences
  const [matchAlerts, setMatchAlerts] = useState(true);
  const [claimUpdates, setClaimUpdates] = useState(true);

  useEffect(() => {
    if (user) {
      setDisplayName(user.display_name || "");
      setPhone(user.phone || "");
      if (user.notification_preferences) {
        setMatchAlerts(user.notification_preferences.match_alerts ?? true);
        setClaimUpdates(user.notification_preferences.claim_updates ?? true);
        if (user.notification_preferences.language) {
          setSelectedLanguage(user.notification_preferences.language);
          setAppLanguage(user.notification_preferences.language);
        }
      }
    }
  }, [user]);

  const handleLanguageSelect = (langCode) => {
    setSelectedLanguage(langCode);
    setAppLanguage(langCode);
  };

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setProfileSuccess("");
    setProfileError("");

    try {
      setProfileLoading(true);
      await api.updateProfile({
        display_name: displayName.trim(),
        phone: phone.trim() || undefined,
        notification_preferences: {
          match_alerts: matchAlerts,
          claim_updates: claimUpdates,
          language: selectedLanguage
        }
      });
      await refreshUser();
      setProfileSuccess(t("common.success"));
    } catch (err) {
      setProfileError(err.message || t("common.error"));
    } finally {
      setProfileLoading(false);
    }
  };

  const handlePasswordSubmit = async (e) => {
    e.preventDefault();
    setPasswordSuccess("");
    setPasswordError("");

    if (!currentPassword) {
      setPasswordError("Current password is required.");
      return;
    }
    if (newPassword.length < 6) {
      setPasswordError(t("auth.passwordTooShort"));
      return;
    }
    if (newPassword !== confirmPassword) {
      setPasswordError(t("auth.passwordsDoNotMatch"));
      return;
    }

    try {
      setPasswordLoading(true);
      await api.changePassword(currentPassword, newPassword);
      await refreshUser();
      setPasswordSuccess(t("common.success"));
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setPasswordError(err.message || t("common.error"));
    } finally {
      setPasswordLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <div className="max-w-3xl mx-auto space-y-8">
      {/* Page Header */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            {t("profile.title")}
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {t("profile.subtitle")}
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-xl text-xs font-semibold text-rose-600 bg-rose-50 hover:bg-rose-100 transition flex items-center gap-1.5 cursor-pointer"
        >
          <LogOut className="w-4 h-4" /> {t("nav.signOut")}
        </button>
      </div>

      {/* Language Preference Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
          <Globe className="w-5 h-5 text-blue-600" />
          <div>
            <h3 className="font-bold text-slate-900 text-sm">
              {t("profile.languageSection")}
            </h3>
            <p className="text-xs text-slate-500">
              {t("profile.languageHelp")}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
          {SUPPORTED_LANGUAGES.map((lang) => {
            const isSelected = i18n.language === lang.code;
            return (
              <button
                key={lang.code}
                type="button"
                onClick={() => handleLanguageSelect(lang.code)}
                className={`p-3 rounded-2xl border text-left transition flex flex-col justify-between gap-2 cursor-pointer ${
                  isSelected
                    ? "bg-blue-50/80 border-blue-500 text-blue-900 ring-2 ring-blue-500/20 shadow-xs"
                    : "bg-slate-50/60 border-slate-200 hover:border-slate-300 hover:bg-slate-100/60 text-slate-700"
                }`}
              >
                <div className="flex items-center justify-between w-full">
                  <span className="text-xl" role="img" aria-label={lang.name}>{lang.flag}</span>
                  {isSelected && (
                    <div className="w-5 h-5 rounded-full bg-blue-600 text-white flex items-center justify-center">
                      <Check className="w-3 h-3 stroke-[3]" />
                    </div>
                  )}
                </div>
                <div>
                  <span className="font-extrabold text-sm block text-slate-900">{lang.nativeName}</span>
                  <span className="text-[10px] text-slate-500 font-medium">{lang.name}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Initial Admin Password Change Banner */}
      {mustChangeInitial && (
        <div className="p-4 rounded-2xl bg-amber-50 border border-amber-300 text-xs text-amber-900 space-y-1">
          <div className="flex items-center gap-2 font-bold text-amber-950">
            <KeyRound className="w-5 h-5 text-amber-700" />
            <span>Mandatory Initial Password Change Required</span>
          </div>
          <p className="leading-relaxed">
            As a development security safeguard, you must update your temporary initial credentials before continuing regular administration activities.
          </p>
        </div>
      )}

      {/* Grid: Profile Info & Password Change */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Profile Card */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <User className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-slate-900 text-sm">{t("profile.personalInfo")}</h3>
          </div>

          {profileSuccess && (
            <div className="p-3 rounded-xl bg-emerald-50 text-emerald-800 text-xs flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
              <span>{profileSuccess}</span>
            </div>
          )}

          {profileError && (
            <div className="p-3 rounded-xl bg-rose-50 text-rose-800 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
              <span>{profileError}</span>
            </div>
          )}

          <form onSubmit={handleProfileSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.fullName")}
              </label>
              <input
                type="text"
                required
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.email")}
              </label>
              <input
                type="email"
                disabled
                value={user?.email || ""}
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-500 text-sm cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.phone")}
              </label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+91 98765 43210"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Notification preferences */}
            <div className="pt-2 border-t border-slate-100 space-y-2">
              <span className="font-semibold text-slate-700 block">{t("profile.notificationsSection")}</span>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={matchAlerts}
                  onChange={(e) => setMatchAlerts(e.target.checked)}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span className="text-slate-600">{t("profile.matchAlerts")}</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={claimUpdates}
                  onChange={(e) => setClaimUpdates(e.target.checked)}
                  className="rounded text-blue-600 focus:ring-blue-500"
                />
                <span className="text-slate-600">{t("profile.claimUpdates")}</span>
              </label>
            </div>

            <button
              type="submit"
              disabled={profileLoading}
              className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs transition cursor-pointer"
            >
              {profileLoading ? t("common.loading") : t("profile.updateBtn")}
            </button>
          </form>
        </div>

        {/* Password Card */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
            <Lock className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-slate-900 text-sm">{t("profile.changePassword")}</h3>
          </div>

          {passwordSuccess && (
            <div className="p-3 rounded-xl bg-emerald-50 text-emerald-800 text-xs flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
              <span>{passwordSuccess}</span>
            </div>
          )}

          {passwordError && (
            <div className="p-3 rounded-xl bg-rose-50 text-rose-800 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
              <span>{passwordError}</span>
            </div>
          )}

          <form onSubmit={handlePasswordSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.currentPassword")}
              </label>
              <input
                type="password"
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.newPassword")}
              </label>
              <input
                type="password"
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block font-semibold text-slate-700 mb-1">
                {t("profile.confirmNewPassword")}
              </label>
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              disabled={passwordLoading}
              className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition cursor-pointer"
            >
              {passwordLoading ? t("common.loading") : t("profile.changePassword")}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
