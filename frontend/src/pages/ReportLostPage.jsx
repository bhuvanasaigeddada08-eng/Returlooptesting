import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  HelpCircle, Camera, Upload, AlertCircle, ArrowRight, 
  MapPin, Calendar, Tag, ShieldAlert, CheckCircle2 
} from "lucide-react";
import api from "../services/api";
import { CATEGORIES, CAMPUS_LOCATIONS } from "../utils/constants";

export const ReportLostPage = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: "",
    category: "",
    description: "",
    color: "",
    brand: "",
    general_location: "",
    event_date: new Date().toISOString().split("T")[0],
    identifying_characteristics: ""
  });
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.size > 5 * 1024 * 1024) {
        setErrorMessage("Image size exceeds 5MB limit.");
        return;
      }
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setErrorMessage("");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage("");

    if (!formData.title.trim()) {
      setErrorMessage(t("report.itemTitleLabel"));
      return;
    }
    if (!formData.category) {
      setErrorMessage(t("report.categoryLabel"));
      return;
    }
    if (!formData.description.trim() || formData.description.length < 10) {
      setErrorMessage("Description must be at least 10 characters long.");
      return;
    }
    if (!formData.color.trim()) {
      setErrorMessage("Please specify the main color.");
      return;
    }
    if (!formData.general_location) {
      setErrorMessage(t("report.locationLabel"));
      return;
    }

    try {
      setLoading(true);
      const res = await api.createReport({
        report_type: "lost",
        ...formData
      });

      const reportId = res.report.id;

      // Upload image if selected
      if (selectedFile) {
        try {
          await api.uploadReportImage(reportId, selectedFile);
        } catch (imgErr) {
          console.warn("Report created but image upload encountered an issue:", imgErr);
        }
      }

      navigate(`/items/${reportId}`, { state: { justCreated: true } });
    } catch (err) {
      setErrorMessage(err.message || "Failed to create lost report.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto my-4 sm:my-8">
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-10 shadow-sm">
        <div className="flex items-center gap-3 mb-6 pb-6 border-b border-slate-100">
          <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 border border-rose-100 flex items-center justify-center flex-shrink-0">
            <HelpCircle className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{t("report.lostTitle")}</h1>
            <p className="text-xs text-slate-500">
              {t("report.lostSubtitle")}
            </p>
          </div>
        </div>

        {errorMessage && (
          <div className="p-3.5 mb-6 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>{errorMessage}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Item Title */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              {t("report.itemTitleLabel")}
            </label>
            <input
              type="text"
              name="title"
              required
              value={formData.title}
              onChange={handleChange}
              placeholder={t("report.itemTitlePlaceholder")}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition"
            />
          </div>

          {/* Category & Color */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                {t("report.categoryLabel")}
              </label>
              <select
                name="category"
                required
                value={formData.category}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition bg-white"
              >
                <option value="">{t("explore.allCategories")}</option>
                {CATEGORIES.map(c => (
                  <option key={c} value={c}>{t(`categories.${c}`, c)}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Primary Color <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                name="color"
                required
                value={formData.color}
                onChange={handleChange}
                placeholder="e.g. Blue, Matte Black, Silver"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition"
              />
            </div>
          </div>

          {/* Brand & Date */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Brand or Manufacturer <span className="text-slate-400 font-normal">({t("common.optional")})</span>
              </label>
              <input
                type="text"
                name="brand"
                value={formData.brand}
                onChange={handleChange}
                placeholder="e.g. Apple, Milton, Fastrack, HP"
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                {t("report.dateLabel")}
              </label>
              <input
                type="date"
                name="event_date"
                required
                max={new Date().toISOString().split("T")[0]}
                value={formData.event_date}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition bg-white"
              />
            </div>
          </div>

          {/* Campus Location */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              {t("report.locationLabel")}
            </label>
            <select
              name="general_location"
              required
              value={formData.general_location}
              onChange={handleChange}
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition bg-white"
            >
              <option value="">{t("explore.allLocations")}</option>
              {CAMPUS_LOCATIONS.map(loc => (
                <option key={loc} value={loc}>{t(`locations.${loc}`, loc)}</option>
              ))}
            </select>
          </div>

          {/* Description */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              Description <span className="text-rose-500">*</span>
            </label>
            <textarea
              name="description"
              required
              rows={3}
              value={formData.description}
              onChange={handleChange}
              placeholder="Describe where you think you left it and general appearance..."
              className="w-full px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 transition"
            />
          </div>

          {/* Private Identifying Characteristics */}
          <div className="p-4 rounded-2xl bg-amber-50/60 border border-amber-200/80 space-y-2">
            <div className="flex items-center gap-2 text-xs font-bold text-amber-900">
              <ShieldAlert className="w-4 h-4 text-amber-600" />
              <span>{t("report.privateProofLabel")}</span>
            </div>
            <p className="text-[11px] text-amber-800 leading-relaxed">
              These private details (e.g. unique marks, custom sticker placement, lock screen wallpaper) are stored securely and only accessible by you and verifying security officers.
            </p>
            <textarea
              name="identifying_characteristics"
              rows={2}
              value={formData.identifying_characteristics}
              onChange={handleChange}
              placeholder={t("report.privateProofPlaceholder")}
              className="w-full px-3.5 py-2 rounded-xl border border-amber-300 text-xs focus:outline-none focus:ring-2 focus:ring-amber-500 bg-white"
            />
          </div>

          {/* Photograph Upload */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5">
              {t("report.primaryImageLabel")} <span className="text-slate-400 font-normal">({t("common.optional")})</span>
            </label>
            <div className="flex items-center gap-4">
              <label className="flex-1 border-2 border-dashed border-slate-200 hover:border-rose-400 rounded-2xl p-4 text-center cursor-pointer transition flex flex-col items-center justify-center gap-1.5 bg-slate-50/50 hover:bg-rose-50/20">
                <Camera className="w-6 h-6 text-slate-400" />
                <span className="text-xs font-medium text-slate-600">
                  {selectedFile ? selectedFile.name : t("report.uploadHelp")}
                </span>
                <span className="text-[10px] text-slate-400">PNG, JPG, WEBP up to 5MB</span>
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  onChange={handleFileChange}
                  className="hidden"
                />
              </label>

              {previewUrl && (
                <div className="relative w-20 h-20 rounded-xl overflow-hidden border border-slate-200 flex-shrink-0">
                  <img src={previewUrl} alt="Preview" className="w-full h-full object-cover" />
                  <button
                    type="button"
                    onClick={() => { setSelectedFile(null); setPreviewUrl(null); }}
                    className="absolute top-1 right-1 bg-black/60 text-white rounded-full p-0.5 text-[10px]"
                  >
                    ✕
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-3">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-semibold text-sm transition shadow-sm hover:shadow flex items-center justify-center gap-2 disabled:opacity-60 cursor-pointer"
            >
              {loading ? t("report.submitting") : t("report.submitReportBtn")}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ReportLostPage;
