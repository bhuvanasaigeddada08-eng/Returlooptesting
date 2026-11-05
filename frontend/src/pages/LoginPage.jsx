import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Eye, EyeOff, Lock, Mail, ArrowRight, ShieldCheck, 
  AlertCircle, Info, Sparkles 
} from "lucide-react";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";

export const LoginPage = () => {
  const { t } = useTranslation();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [googleConfig, setGoogleConfig] = useState({ enabled: false, client_id: null });

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/dashboard";

  useEffect(() => {
    const checkGoogleOAuth = async () => {
      try {
        const res = await api.getGoogleConfig();
        setGoogleConfig(res);
      } catch (e) {
        setGoogleConfig({ enabled: false, client_id: null });
      }
    };
    checkGoogleOAuth();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    if (!email || !password) {
      setErrorMessage(t("auth.fillAllFields"));
      return;
    }

    try {
      setLoading(true);
      const res = await login(email, password);
      if (res.user?.must_change_password) {
        navigate("/profile", { state: { mustChange: true } });
      } else if (res.user?.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/explore");
      }
    } catch (err) {
      if (err.message && err.message.toLowerCase().includes("failed to fetch")) {
        const host = window.location.hostname || "";
        const isLocal = host === "localhost" || host === "127.0.0.1" || /^172\./.test(host) || /^192\.168\./.test(host) || /^10\./.test(host);
        if (isLocal) {
          setErrorMessage("Cannot connect to local backend. Please ensure 'START_SERVERS.bat' is running on your laptop (Flask port 5000).");
        } else {
          setErrorMessage("Cloud server is waking up (takes ~30-40s on Render free tier). Please wait a moment and click Sign In again.");
        }
      } else {
        setErrorMessage(err.message || t("auth.invalidCredentials"));
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDemoFill = (role) => {
    if (role === "admin") {
      setEmail("admin@returnloop.lpu.in");
      setPassword("AdminPass123!");
    } else {
      setEmail("aarav.sharma@lpu.in");
      setPassword("StudentPass123!");
    }
  };

  return (
    <div className="max-w-md mx-auto my-6 sm:my-12">
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-sm">
        <div className="text-center space-y-1 mb-6">
          <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center mx-auto mb-3">
            <Lock className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900 tracking-tight">{t("auth.signInTitle")}</h2>
          <p className="text-xs text-slate-500">
            {t("auth.signInSubtitle")}
          </p>
        </div>

        {errorMessage && (
          <div className="p-3.5 mb-6 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              {t("auth.emailLabel")}
            </label>
            <div className="relative">
              <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder={t("auth.emailPlaceholder")}
                className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              {t("auth.passwordLabel")}
            </label>
            <div className="relative">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-10 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-sm transition shadow-sm hover:shadow flex items-center justify-center gap-2 mt-2 disabled:opacity-60 cursor-pointer"
          >
            {loading ? t("common.loading") : t("auth.signInBtn")}
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Optional Google Sign-In Integration Section */}
        <div className="mt-6 pt-5 border-t border-slate-100">
          <div className="relative flex justify-center text-xs uppercase mb-3">
            <span className="bg-white px-2 text-slate-400 font-semibold tracking-wider text-[10px]">
              {t("auth.googleSignIn")}
            </span>
          </div>

          {googleConfig.enabled ? (
            <button
              type="button"
              className="w-full py-2.5 px-4 rounded-xl border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center justify-center gap-2 transition"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24">
                <path
                  fill="#4285F4"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="#34A853"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="#FBBC05"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                />
                <path
                  fill="#EA4335"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                />
              </svg>
              <span>{t("auth.googleSignIn")}</span>
            </button>
          ) : (
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 text-center space-y-1">
              <div className="flex items-center justify-center gap-1.5 text-xs font-semibold text-slate-600">
                <svg className="w-3.5 h-3.5 opacity-50" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                </svg>
                <span>{t("auth.googleSignIn")}</span>
              </div>
              <p className="text-[11px] text-slate-500 leading-normal">
                {t("auth.googleDesc")}
              </p>
            </div>
          )}
        </div>

        {/* Demo Fast-Fill Buttons for easy evaluation */}
        <div className="mt-6 pt-5 border-t border-slate-100">
          <p className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 text-center mb-3">
            {t("auth.quickDemo")}
          </p>
          <div className="grid grid-cols-2 gap-2">
            <button
              type="button"
              onClick={() => handleDemoFill("student")}
              className="px-3 py-2 text-xs font-medium bg-slate-50 hover:bg-slate-100 border border-slate-200 rounded-xl text-slate-700 text-center transition cursor-pointer"
            >
              {t("auth.demoStudent")}
            </button>
            <button
              type="button"
              onClick={() => handleDemoFill("admin")}
              className="px-3 py-2 text-xs font-medium bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-xl text-blue-700 text-center transition cursor-pointer"
            >
              {t("auth.demoAdmin")}
            </button>
          </div>
        </div>

        <div className="mt-6 text-center text-xs text-slate-500">
          {t("auth.noAccount")}{" "}
          <Link to="/register" className="font-semibold text-blue-600 hover:text-blue-800">
            {t("auth.registerHere")}
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
