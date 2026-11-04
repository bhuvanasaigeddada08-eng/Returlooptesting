import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Search, PlusCircle, HelpCircle, ShieldCheck, 
  Sparkles, Lock, ArrowRight, Shield, CheckCircle2, Clock,
  Laptop, CreditCard, Briefcase, Key, BookOpen, Shirt, Coffee, Package,
  Zap, Award, Users, Globe
} from "lucide-react";
import api from "../services/api";
import ItemCard from "../components/ItemCard";
import { CardSkeleton } from "../components/LoadingSkeleton";
import { CATEGORIES } from "../utils/constants";
import { SUPPORTED_LANGUAGES, setAppLanguage } from "../i18n";
import LanguageSelectorModal from "../components/LanguageSelectorModal";

const CATEGORY_META = {
  "Electronics": { icon: Laptop, color: "text-blue-500", bg: "bg-blue-50 hover:bg-blue-100/80 border-blue-100" },
  "ID & Cards": { icon: CreditCard, color: "text-indigo-500", bg: "bg-indigo-50 hover:bg-indigo-100/80 border-indigo-100" },
  "Bags & Wallets": { icon: Briefcase, color: "text-amber-500", bg: "bg-amber-50 hover:bg-amber-100/80 border-amber-100" },
  "Keys": { icon: Key, color: "text-rose-500", bg: "bg-rose-50 hover:bg-rose-100/80 border-rose-100" },
  "Books & Stationery": { icon: BookOpen, color: "text-emerald-500", bg: "bg-emerald-50 hover:bg-emerald-100/80 border-emerald-100" },
  "Clothing & Accessories": { icon: Shirt, color: "text-purple-500", bg: "bg-purple-50 hover:bg-purple-100/80 border-purple-100" },
  "Bottles & Tumblers": { icon: Coffee, color: "text-teal-500", bg: "bg-teal-50 hover:bg-teal-100/80 border-teal-100" },
  "Other": { icon: Package, color: "text-slate-500", bg: "bg-slate-50 hover:bg-slate-100/80 border-slate-200" }
};

export const LandingPage = () => {
  const { t, i18n } = useTranslation();
  const [recentReports, setRecentReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [langModalOpen, setLangModalOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchRecent = async () => {
      try {
        const res = await api.getReports({ per_page: 6, sort: "newest" });
        setRecentReports(res.reports || []);
      } catch (err) {
        console.error("Failed to load recent reports:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecent();
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/explore?q=${encodeURIComponent(searchQuery.trim())}`);
    } else {
      navigate("/explore");
    }
  };

  return (
    <div className="space-y-12 sm:space-y-20 pb-12">
      {/* Homepage Native Multi-Language Selector Bar */}
      <section className="bg-white rounded-2xl border border-slate-200/90 p-3 sm:p-4 shadow-xs">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
            <Globe className="w-4 h-4 text-blue-600" />
            <span>{t("home.selectLanguagePrompt")}:</span>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-1.5">
            {SUPPORTED_LANGUAGES.map((lang) => {
              const active = i18n.language === lang.code;
              return (
                <button
                  key={lang.code}
                  type="button"
                  onClick={() => setAppLanguage(lang.code)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer ${
                    active
                      ? "bg-blue-600 text-white shadow-xs"
                      : "bg-slate-100 hover:bg-slate-200 text-slate-700"
                  }`}
                >
                  <span className="text-sm" role="img" aria-hidden="true">{lang.flag}</span>
                  <span>{lang.nativeName}</span>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* Hero Section */}
      <section className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-slate-850 via-slate-800 to-slate-900 text-white p-6 sm:p-10 lg:p-12 shadow-xl border border-slate-700/70" style={{ backgroundColor: "#1e293b" }}>
        <div className="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:20px_20px] pointer-events-none opacity-60" />
        <div className="absolute -top-24 -right-24 w-96 h-96 bg-sky-500/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-80 h-80 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          {/* Left Column: Heading, Search & Primary Actions */}
          <div className="lg:col-span-7 space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-700/60 border border-slate-600/70 text-sky-300 text-xs font-semibold backdrop-blur-sm shadow-xs">
              <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
              <span>{t("home.heroBadge")}</span>
            </div>

            <h1 className="text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight leading-tight text-white">
              {t("home.heroTitle")}
            </h1>

            <p className="text-slate-300 text-xs sm:text-sm lg:text-base leading-relaxed max-w-xl font-normal">
              {t("home.heroSubtitle")}
            </p>

            {/* Quick Search Bar */}
            <form onSubmit={handleSearchSubmit} className="pt-1 flex flex-col sm:flex-row gap-2.5 max-w-xl">
              <div className="relative flex-1">
                <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder={t("explore.searchPlaceholder")}
                  className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/80 border border-slate-700 text-white placeholder-slate-400 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-sky-400 transition shadow-inner"
                />
              </div>
              <button
                type="submit"
                className="px-6 py-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs sm:text-sm transition shadow-md shadow-sky-950/20 flex items-center justify-center gap-2 cursor-pointer active:scale-95 whitespace-nowrap"
              >
                <Search className="w-4 h-4 text-slate-950" />
                <span>{t("common.search")}</span>
              </button>
            </form>

            {/* Primary Action Buttons */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 pt-1">
              <Link
                to="/report-lost"
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-sm active:scale-95 text-center"
              >
                <HelpCircle className="w-4 h-4" />
                <span>{t("home.reportLostBtn")}</span>
              </Link>
              <Link
                to="/report-found"
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm transition flex items-center justify-center gap-2 shadow-sm active:scale-95 text-center"
              >
                <ShieldCheck className="w-4 h-4" />
                <span>{t("home.reportFoundBtn")}</span>
              </Link>
              <Link
                to="/explore"
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-slate-700/70 hover:bg-slate-700 border border-slate-600 text-slate-200 font-semibold text-xs sm:text-sm transition flex items-center justify-center gap-1.5 text-center"
              >
                <span>{t("home.exploreBtn")}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            {/* Stats Bar */}
            <div className="grid grid-cols-3 gap-3 sm:gap-4 pt-4 border-t border-slate-700/80 max-w-lg">
              <div className="space-y-0.5">
                <span className="text-xl sm:text-2xl font-black text-white">100%</span>
                <p className="text-[11px] text-slate-400">Free Campus Registry</p>
              </div>
              <div className="space-y-0.5">
                <span className="text-xl sm:text-2xl font-black text-sky-400">7 Languages</span>
                <p className="text-[11px] text-slate-400">Complete Multilingual</p>
              </div>
              <div className="space-y-0.5">
                <span className="text-xl sm:text-2xl font-black text-emerald-400">Verified</span>
                <p className="text-[11px] text-slate-400">{t("common.finalized")}</p>
              </div>
            </div>
          </div>

          {/* Right Column: Visual Protocol Highlights */}
          <div className="lg:col-span-5 hidden lg:flex flex-col gap-3">
            <div className="p-6 rounded-2xl bg-slate-900/60 backdrop-blur-md border border-slate-700/80 shadow-md space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-700/60">
                <div className="flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
                  <span className="text-xs font-bold uppercase tracking-wider text-slate-300">Active Campus Protocol</span>
                </div>
                <span className="text-[10px] px-2.5 py-0.5 rounded-full bg-slate-800 font-bold text-sky-300 border border-slate-700">
                  LPU Network
                </span>
              </div>

              {/* Protocol Highlights */}
              <div className="space-y-3">
                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 shadow-xs flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-blue-500/20 text-sky-300 flex items-center justify-center font-bold text-xs shrink-0">
                    01
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{t("home.step1Title")}</h4>
                    <p className="text-[11px] text-slate-400">{t("home.step1Desc")}</p>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 shadow-xs flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-300 flex items-center justify-center font-bold text-xs shrink-0">
                    02
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{t("home.step2Title")}</h4>
                    <p className="text-[11px] text-slate-400">{t("home.step2Desc")}</p>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-slate-800/80 border border-slate-700/60 shadow-xs flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center font-bold text-xs shrink-0">
                    03
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{t("home.step3Title")}</h4>
                    <p className="text-[11px] text-slate-400">{t("home.step3Desc")}</p>
                  </div>
                </div>
              </div>

              <div className="pt-2 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-700/60">
                <span>Free community system</span>
                <span className="font-bold text-sky-300 bg-slate-800 px-2.5 py-0.5 rounded border border-slate-700">₹0 Cost Protocol</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Category Grid */}
      <section className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
              <Zap className="w-3.5 h-3.5" />
              <span>{t("common.category")}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
              {t("explore.allCategories")}
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Select a category to filter active reports across university blocks.
            </p>
          </div>
          <Link to="/explore" className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1 group">
            {t("common.all")} <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {CATEGORIES.map((cat) => {
            const meta = CATEGORY_META[cat] || CATEGORY_META["Other"];
            const Icon = meta.icon;
            const translatedCat = t(`categories.${cat}`, cat);
            return (
              <Link
                key={cat}
                to={`/explore?category=${encodeURIComponent(cat)}`}
                className={`p-5 rounded-2xl border ${meta.bg} transition-all duration-200 hover:-translate-y-1 hover:shadow-md flex flex-col items-center text-center gap-3 group`}
              >
                <div className={`w-12 h-12 rounded-xl bg-white shadow-sm flex items-center justify-center ${meta.color} group-hover:scale-110 transition-transform`}>
                  <Icon className="w-6 h-6" />
                </div>
                <div>
                  <span className="font-bold text-slate-800 group-hover:text-blue-600 transition text-sm block">
                    {translatedCat}
                  </span>
                  <span className="text-[11px] text-slate-500 font-medium">{t("nav.brandSub")}</span>
                </div>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Recently Reported Items */}
      <section className="space-y-6">
        <div className="flex justify-between items-end">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-blue-600 mb-1">
              <Clock className="w-3.5 h-3.5" />
              <span>{t("dashboard.recentItems")}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
              {t("dashboard.recentItems")}
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Real items recently logged across Central Library, UniMall, and Academic Blocks.
            </p>
          </div>
          <Link to="/explore" className="text-xs font-bold text-blue-600 hover:text-blue-800 flex items-center gap-1 group">
            {t("dashboard.viewAll")} ({recentReports.length}) <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {Array.from({ length: 6 }).map((_, i) => (
              <CardSkeleton key={i} />
            ))}
          </div>
        ) : recentReports.length === 0 ? (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-slate-300">
            <p className="text-sm font-medium text-slate-500">{t("dashboard.noReports")}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentReports.map((item) => (
              <ItemCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </section>

      {/* How It Works */}
      <section className="space-y-8 bg-slate-50/80 rounded-3xl p-8 sm:p-12 border border-slate-200/80">
        <div className="text-center max-w-2xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-blue-600">Verification Lifecycle</span>
          <h2 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            {t("home.howItWorksTitle")}
          </h2>
          <p className="text-xs sm:text-sm text-slate-600">
            {t("home.howItWorksSubtitle")}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-3 hover:shadow-md transition">
            <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center font-bold text-sm border border-rose-100">
              01
            </div>
            <h3 className="font-bold text-slate-900 text-base">{t("home.step1Title")}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t("home.step1Desc")}
            </p>
          </div>

          <div className="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-3 hover:shadow-md transition">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-sm border border-blue-100">
              02
            </div>
            <h3 className="font-bold text-slate-900 text-base">{t("home.step2Title")}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t("home.step2Desc")}
            </p>
          </div>

          <div className="p-6 bg-white rounded-2xl border border-slate-200/80 shadow-sm space-y-3 hover:shadow-md transition">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center font-bold text-sm border border-teal-100">
              03
            </div>
            <h3 className="font-bold text-slate-900 text-base">{t("home.step3Title")}</h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {t("home.step3Desc")}
            </p>
          </div>
        </div>
      </section>

      {/* Privacy Guarantee Card */}
      <section className="rounded-3xl p-6 sm:p-8 bg-gradient-to-r from-blue-900 to-indigo-950 text-white shadow-lg border border-blue-800/60 flex flex-col sm:flex-row gap-6 items-start sm:items-center justify-between">
        <div className="space-y-2 max-w-2xl">
          <div className="flex items-center gap-2 text-white font-bold text-base">
            <Shield className="w-5 h-5 text-blue-400" />
            <span>{t("home.secureTitle")}</span>
          </div>
          <p className="text-xs text-slate-300 leading-relaxed">
            {t("home.secureDesc")}
          </p>
        </div>
        <div className="flex-shrink-0">
          <Link
            to="/explore"
            className="px-6 py-3 rounded-xl bg-white text-slate-900 font-bold text-xs hover:bg-slate-100 transition shadow-sm block text-center"
          >
            {t("home.exploreBtn")}
          </Link>
        </div>
      </section>

      <LanguageSelectorModal isOpen={langModalOpen} onClose={() => setLangModalOpen(false)} />
    </div>
  );
};

export default LandingPage;
