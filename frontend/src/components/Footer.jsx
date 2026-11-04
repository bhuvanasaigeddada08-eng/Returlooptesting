import React from "react";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Shield, Lock, MapPin, Phone, Heart } from "lucide-react";
import LogoIcon from "./LogoIcon";

export const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-slate-900 text-slate-400 text-xs border-t border-slate-800 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2">
              <LogoIcon className="w-8 h-8" />
              <span className="font-bold text-white text-base tracking-tight">
                ReturnLoop <span className="text-blue-400">LPU</span>
              </span>
            </div>
            <p className="text-slate-400 leading-relaxed text-xs">
              {t("footer.brandDesc")}
            </p>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-amber-500/10 border border-amber-500/20 text-amber-400 text-[11px]">
              <span>{t("footer.studentPrototype")}</span>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-2">
            <h4 className="font-semibold text-white text-sm">{t("footer.quickLinks")}</h4>
            <ul className="space-y-1.5">
              <li>
                <Link to="/explore" className="hover:text-white transition">{t("footer.exploreLink")}</Link>
              </li>
              <li>
                <Link to="/report-lost" className="hover:text-white transition">{t("footer.reportLostLink")}</Link>
              </li>
              <li>
                <Link to="/report-found" className="hover:text-white transition">{t("footer.reportFoundLink")}</Link>
              </li>
              <li>
                <Link to="/dashboard" className="hover:text-white transition">{t("footer.dashboardLink")}</Link>
              </li>
            </ul>
          </div>

          {/* Campus Recovery Helpdesk */}
          <div className="space-y-2">
            <h4 className="font-semibold text-white text-sm">{t("footer.securityHelpdesk")}</h4>
            <ul className="space-y-1.5 text-slate-400">
              <li className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                <span>{t("footer.securityAddress")}</span>
              </li>
              <li className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-blue-400 flex-shrink-0" />
                <span>{t("footer.intercom")}</span>
              </li>
              <li className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>{t("footer.hours")}</span>
              </li>
            </ul>
          </div>

          {/* Privacy & Ethics */}
          <div className="space-y-2">
            <h4 className="font-semibold text-white text-sm">{t("footer.privacySection")}</h4>
            <p className="text-slate-400 text-xs leading-relaxed">
              {t("footer.privacyNote")}
            </p>
            <div className="flex items-center gap-2 text-slate-300 text-xs pt-1">
              <Lock className="w-3.5 h-3.5 text-teal-400" />
              <span>Role-Based Access Control</span>
            </div>
          </div>
        </div>

        {/* Bottom Disclaimer */}
        <div className="pt-8 border-t border-slate-800 text-center flex flex-col sm:flex-row items-center justify-between gap-4 text-slate-500 text-[11px]">
          <p>
            © {new Date().getFullYear()} {t("footer.copyright")}
          </p>
          <p className="flex items-center gap-1">
            Engineered with <Heart className="w-3 h-3 text-rose-500 fill-rose-500" /> for LPU Campus Community
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
