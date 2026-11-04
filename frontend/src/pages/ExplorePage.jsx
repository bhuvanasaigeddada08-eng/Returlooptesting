import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Search, Filter, SlidersHorizontal, Grid, List, 
  MapPin, Calendar, Tag, RefreshCw, X, Sparkles 
} from "lucide-react";
import api from "../services/api";
import ItemCard from "../components/ItemCard";
import StatusBadge from "../components/StatusBadge";
import EmptyState from "../components/EmptyState";
import { CardSkeleton } from "../components/LoadingSkeleton";
import { CATEGORIES, CAMPUS_LOCATIONS } from "../utils/constants";

export const ExplorePage = () => {
  const { t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState("grid"); // "grid" | "list"
  const [pagination, setPagination] = useState({ page: 1, pages: 1, total: 0 });

  // Filters state initialized from URL search params
  const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "");
  const [selectedCategory, setSelectedCategory] = useState(searchParams.get("category") || "");
  const [selectedType, setSelectedType] = useState(searchParams.get("type") || ""); // "lost", "found", or ""
  const [selectedLocation, setSelectedLocation] = useState(searchParams.get("location") || "");
  const [sortBy, setSortBy] = useState(searchParams.get("sort") || "newest");
  const [currentPage, setCurrentPage] = useState(parseInt(searchParams.get("page") || "1", 10));

  const fetchReports = async () => {
    try {
      setLoading(true);
      const res = await api.getReports({
        q: searchQuery,
        category: selectedCategory,
        type: selectedType,
        location: selectedLocation,
        sort: sortBy,
        page: currentPage,
        per_page: 12
      });
      setReports(res.reports || []);
      setPagination({
        page: res.page || 1,
        pages: res.pages || 1,
        total: res.total || 0
      });
    } catch (err) {
      console.error("Failed to load items:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, [searchQuery, selectedCategory, selectedType, selectedLocation, sortBy, currentPage]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    setCurrentPage(1);
    const params = {};
    if (searchQuery) params.q = searchQuery;
    if (selectedCategory) params.category = selectedCategory;
    if (selectedType) params.type = selectedType;
    if (selectedLocation) params.location = selectedLocation;
    setSearchParams(params);
  };

  const handleResetFilters = () => {
    setSearchQuery("");
    setSelectedCategory("");
    setSelectedType("");
    setSelectedLocation("");
    setSortBy("newest");
    setCurrentPage(1);
    setSearchParams({});
  };

  const hasActiveFilters = searchQuery || selectedCategory || selectedType || selectedLocation;

  return (
    <div className="space-y-6">
      {/* Top Banner & Search - Premium Dark Campus Theme */}
      <section 
        className="relative rounded-3xl overflow-hidden bg-gradient-to-br from-slate-850 via-slate-800 to-slate-900 text-white p-6 sm:p-8 shadow-xl border border-slate-700/70 space-y-5"
        style={{ backgroundColor: "#1e293b" }}
      >
        <div className="absolute inset-0 bg-[radial-gradient(rgba(255,255,255,0.08)_1px,transparent_1px)] [background-size:20px_20px] pointer-events-none opacity-60" />
        <div className="absolute -top-24 -right-24 w-80 h-80 bg-sky-500/15 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-indigo-500/15 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-5">
          {/* Header Row with Badge & View Mode */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="space-y-1.5">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-700/60 border border-slate-600/70 text-sky-300 text-xs font-semibold backdrop-blur-sm shadow-xs">
                <Sparkles className="w-3.5 h-3.5 text-amber-400 animate-pulse" />
                <span>{t("home.heroBadge")}</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
                {t("explore.title")}
              </h1>
              <p className="text-xs sm:text-sm text-slate-300">
                {t("explore.subtitle")}
              </p>
            </div>

            <div className="flex items-center gap-2 self-end sm:self-center">
              <button
                onClick={() => setViewMode("grid")}
                className={`p-2.5 rounded-xl border text-xs font-medium transition cursor-pointer ${
                  viewMode === "grid"
                    ? "bg-sky-500 text-slate-950 font-bold border-sky-400 shadow-md shadow-sky-950/20"
                    : "bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white"
                }`}
                aria-label="Grid View"
              >
                <Grid className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`p-2.5 rounded-xl border text-xs font-medium transition cursor-pointer ${
                  viewMode === "list"
                    ? "bg-sky-500 text-slate-950 font-bold border-sky-400 shadow-md shadow-sky-950/20"
                    : "bg-slate-800/80 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white"
                }`}
                aria-label="List View"
              >
                <List className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Search Input Form */}
          <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-2.5">
            <div className="relative flex-1">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder={t("explore.searchPlaceholder")}
                className="w-full pl-10 pr-4 py-3 rounded-xl bg-slate-900/90 border border-slate-700 text-white placeholder-slate-400 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-sky-400 focus:border-sky-400 transition shadow-inner"
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

          {/* Category Quick-Pills */}
          <div className="overflow-x-auto no-scrollbar flex items-center gap-2 py-1 -mx-2 px-2">
            <button
              type="button"
              onClick={() => { setSelectedCategory(""); setCurrentPage(1); }}
              className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition flex-shrink-0 cursor-pointer ${
                selectedCategory === ""
                  ? "bg-sky-400 text-slate-950 font-bold shadow-md shadow-sky-900/30"
                  : "bg-slate-800/90 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/80"
              }`}
            >
              {t("explore.allCategories")}
            </button>
            {CATEGORIES.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => { setSelectedCategory(cat === selectedCategory ? "" : cat); setCurrentPage(1); }}
                className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition flex-shrink-0 cursor-pointer ${
                  selectedCategory === cat
                    ? "bg-sky-400 text-slate-950 font-bold shadow-md shadow-sky-900/30"
                    : "bg-slate-800/90 text-slate-300 hover:bg-slate-700 hover:text-white border border-slate-700/80"
                }`}
              >
                {t(`categories.${cat}`, cat)}
              </button>
            ))}
          </div>

          {/* Desktop Filter Bar */}
          <div className="hidden md:flex flex-wrap items-center gap-3 pt-3 text-xs border-t border-slate-700/70">
            {/* Lost / Found Type Filter */}
            <div className="flex items-center rounded-xl border border-slate-700/90 p-0.5 bg-slate-900/80">
              <button
                type="button"
                onClick={() => { setSelectedType(""); setCurrentPage(1); }}
                className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
                  selectedType === "" ? "bg-slate-800 text-white font-bold shadow-xs" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t("explore.allTypes")}
              </button>
              <button
                type="button"
                onClick={() => { setSelectedType("lost"); setCurrentPage(1); }}
                className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
                  selectedType === "lost" ? "bg-rose-600 text-white font-bold shadow-xs" : "text-slate-400 hover:text-rose-300"
                }`}
              >
                {t("explore.typeLost")}
              </button>
              <button
                type="button"
                onClick={() => { setSelectedType("found"); setCurrentPage(1); }}
                className={`px-3 py-1.5 rounded-lg font-medium transition cursor-pointer ${
                  selectedType === "found" ? "bg-emerald-600 text-white font-bold shadow-xs" : "text-slate-400 hover:text-emerald-300"
                }`}
              >
                {t("explore.typeFound")}
              </button>
            </div>

            {/* Campus Location Dropdown */}
            <select
              value={selectedLocation}
              onChange={(e) => { setSelectedLocation(e.target.value); setCurrentPage(1); }}
              className="px-3 py-2 rounded-xl border border-slate-700 bg-slate-900/90 text-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-400"
            >
              <option value="" className="bg-slate-900 text-slate-200">{t("explore.allLocations")}</option>
              {CAMPUS_LOCATIONS.map(loc => (
                <option key={loc} value={loc} className="bg-slate-900 text-slate-200">
                  {t(`locations.${loc}`, loc)}
                </option>
              ))}
            </select>

            {/* Sort By */}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-3 py-2 rounded-xl border border-slate-700 bg-slate-900/90 text-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-400 ml-auto"
            >
              <option value="newest" className="bg-slate-900 text-slate-200">{t("explore.sortBy")}: {t("explore.latest")}</option>
              <option value="oldest" className="bg-slate-900 text-slate-200">{t("explore.sortBy")}: {t("explore.oldest")}</option>
            </select>

            {/* Reset Filters */}
            {hasActiveFilters && (
              <button
                onClick={handleResetFilters}
                className="flex items-center gap-1 px-3 py-1.5 text-rose-400 hover:text-rose-300 font-semibold transition cursor-pointer"
              >
                <X className="w-3.5 h-3.5" /> {t("explore.clearFilters")}
              </button>
            )}
          </div>

          {/* Mobile Filter Bar */}
          <div className="md:hidden flex flex-col gap-2.5 pt-3 text-xs border-t border-slate-700/70">
            <div className="flex items-center rounded-xl border border-slate-700/90 p-0.5 bg-slate-900/80 w-full">
              <button
                type="button"
                onClick={() => { setSelectedType(""); setCurrentPage(1); }}
                className={`flex-1 py-1.5 rounded-lg font-medium text-center transition ${
                  selectedType === "" ? "bg-slate-800 text-white font-bold shadow-xs" : "text-slate-400"
                }`}
              >
                {t("common.all")}
              </button>
              <button
                type="button"
                onClick={() => { setSelectedType("lost"); setCurrentPage(1); }}
                className={`flex-1 py-1.5 rounded-lg font-medium text-center transition ${
                  selectedType === "lost" ? "bg-rose-600 text-white font-bold shadow-xs" : "text-slate-400"
                }`}
              >
                {t("explore.typeLost")}
              </button>
              <button
                type="button"
                onClick={() => { setSelectedType("found"); setCurrentPage(1); }}
                className={`flex-1 py-1.5 rounded-lg font-medium text-center transition ${
                  selectedType === "found" ? "bg-emerald-600 text-white font-bold shadow-xs" : "text-slate-400"
                }`}
              >
                {t("explore.typeFound")}
              </button>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <select
                value={selectedLocation}
                onChange={(e) => { setSelectedLocation(e.target.value); setCurrentPage(1); }}
                className="w-full px-3 py-2 rounded-xl border border-slate-700 bg-slate-900/90 text-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-400"
              >
                <option value="" className="bg-slate-900 text-slate-200">{t("explore.allLocations")}</option>
                {CAMPUS_LOCATIONS.map(loc => (
                  <option key={loc} value={loc} className="bg-slate-900 text-slate-200">
                    {t(`locations.${loc}`, loc)}
                  </option>
                ))}
              </select>

              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-3 py-2 rounded-xl border border-slate-700 bg-slate-900/90 text-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-400"
              >
                <option value="newest" className="bg-slate-900 text-slate-200">{t("explore.latest")}</option>
                <option value="oldest" className="bg-slate-900 text-slate-200">{t("explore.oldest")}</option>
              </select>
            </div>

            {hasActiveFilters && (
              <button
                onClick={handleResetFilters}
                className="self-start flex items-center gap-1 px-2 py-1 text-rose-400 hover:text-rose-300 font-semibold transition text-xs"
              >
                <X className="w-3.5 h-3.5" /> {t("explore.clearFilters")}
              </button>
            )}
          </div>
        </div>
      </section>

      {/* Results Header */}
      <div className="flex justify-between items-center text-xs text-slate-500 px-1">
        <span>
          {t("explore.showingResults", { count: reports.length })} ({t("common.all")}: {pagination.total})
        </span>
      </div>

      {/* Items Grid / List View */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      ) : reports.length === 0 ? (
        <EmptyState
          title={t("explore.noItemsFound")}
          description={t("explore.noItemsDesc")}
          actionText={t("explore.clearFilters")}
          onAction={handleResetFilters}
        />
      ) : viewMode === "grid" ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((item) => (
            <ItemCard key={item.id} item={item} />
          ))}
        </div>
      ) : (
        /* List View */
        <div className="bg-white rounded-3xl border border-slate-200/80 divide-y divide-slate-100 overflow-hidden shadow-sm">
          {reports.map((item) => {
            const isLost = item.report_type === "lost";
            return (
              <div
                key={item.id}
                className="p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 hover:bg-slate-50/70 transition"
              >
                <div className="flex items-start gap-4">
                  <span
                    className={`px-2.5 py-1 rounded-lg text-xs font-bold uppercase tracking-wider ${
                      isLost ? "bg-rose-100 text-rose-700" : "bg-teal-100 text-teal-700"
                    }`}
                  >
                    {isLost ? t("nav.lostShort") : t("nav.foundShort")}
                  </span>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-mono text-xs text-slate-400">{item.reference_code}</span>
                      <span className="text-xs text-slate-500">• {t(`categories.${item.category}`, item.category)}</span>
                    </div>
                    <h3 className="font-semibold text-slate-900 text-base">{item.title}</h3>
                    <div className="flex items-center gap-4 text-xs text-slate-500 mt-1">
                      <span className="flex items-center gap-1">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                        {t(`locations.${item.general_location}`, item.general_location)}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5 text-slate-400" />
                        {item.event_date}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
                  <StatusBadge status={item.status} />
                  <a
                    href={`/items/${item.id}`}
                    className="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-semibold hover:bg-slate-800 transition"
                  >
                    {t("common.viewDetails")}
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Pagination Controls */}
      {pagination.pages > 1 && (
        <div className="flex justify-center items-center gap-2 pt-6">
          <button
            disabled={pagination.page <= 1}
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            className="px-3.5 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40 transition cursor-pointer"
          >
            ← {t("common.back")}
          </button>
          <span className="text-xs font-medium text-slate-600 px-3">
            {pagination.page} / {pagination.pages}
          </span>
          <button
            disabled={pagination.page >= pagination.pages}
            onClick={() => setCurrentPage(prev => Math.min(pagination.pages, prev + 1))}
            className="px-3.5 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-40 transition cursor-pointer"
          >
            →
          </button>
        </div>
      )}
    </div>
  );
};

export default ExplorePage;
