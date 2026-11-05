import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { Bell, Check, Sparkles, AlertCircle, ShieldCheck } from "lucide-react";
import api from "../services/api";
import { useAuth } from "../context/AuthContext";
import TranslatedText from "./TranslatedText";

export const NotificationBell = () => {
  const { t } = useTranslation();
  const { isAuthenticated } = useAuth();
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  const navigate = useNavigate();

  const fetchNotifications = async () => {
    if (!isAuthenticated) return;
    try {
      const res = await api.getNotifications();
      setNotifications(res.notifications || []);
      setUnreadCount(res.unread_count || 0);
    } catch (err) {
      console.error("Failed to load notifications:", err);
    }
  };

  useEffect(() => {
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000); // 30s poll
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleBellClick = () => {
    // On mobile viewports, navigate directly to the full notifications page
    if (window.innerWidth < 640) {
      navigate("/notifications");
      return;
    }
    setIsOpen(!isOpen);
  };

  const handleNotificationClick = async (notif) => {
    if (!notif.is_read) {
      try {
        await api.markNotificationRead(notif.id);
        setNotifications(prev =>
          prev.map(n => (n.id === notif.id ? { ...n, is_read: true } : n))
        );
        setUnreadCount(prev => Math.max(0, prev - 1));
      } catch (err) {
        console.error(err);
      }
    }
    setIsOpen(false);
    if (notif.link) {
      navigate(notif.link);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.markAllNotificationsRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      setUnreadCount(0);
    } catch (err) {
      console.error(err);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={handleBellClick}
        className="relative p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition focus:outline-none cursor-pointer"
        aria-label={t("nav.notifications") || "Notifications"}
        title={t("nav.notifications") || "Notifications"}
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute top-1 right-1 w-4 h-4 rounded-full bg-rose-500 text-white text-[10px] font-bold flex items-center justify-center animate-pulse">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-xl border border-slate-200 py-2 z-50 animate-in fade-in zoom-in-95 duration-150">
          <div className="px-4 py-2.5 border-b border-slate-100 flex items-center justify-between">
            <span className="font-semibold text-sm text-slate-900">{t("nav.notifications") || "Notifications"}</span>
            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 cursor-pointer"
              >
                <Check className="w-3.5 h-3.5" /> {t("notifications.markAllRead") || "Mark all read"}
              </button>
            )}
          </div>

          <div className="max-h-80 overflow-y-auto divide-y divide-slate-100">
            {notifications.length === 0 ? (
              <div className="p-6 text-center text-xs text-slate-500">
                {t("notifications.empty") || "No notifications right now."}
              </div>
            ) : (
              notifications.slice(0, 8).map(notif => (
                <div
                  key={notif.id}
                  onClick={() => handleNotificationClick(notif)}
                  className={`p-3.5 hover:bg-slate-50 cursor-pointer transition flex gap-3 items-start ${
                    !notif.is_read ? "bg-blue-50/40" : ""
                  }`}
                >
                  <div className="p-2 rounded-xl bg-slate-100 text-slate-600 flex-shrink-0 mt-0.5">
                    {notif.notification_type === "match" ? (
                      <Sparkles className="w-4 h-4 text-blue-600" />
                    ) : notif.notification_type === "claim_update" ? (
                      <ShieldCheck className="w-4 h-4 text-teal-600" />
                    ) : (
                      <AlertCircle className="w-4 h-4 text-blue-600" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-semibold text-slate-900 truncate">
                      <TranslatedText text={notif.title} />
                    </p>
                    <p className="text-xs text-slate-600 line-clamp-2 mt-0.5">
                      <TranslatedText text={notif.message} />
                    </p>
                  </div>
                  {!notif.is_read && (
                    <span className="w-2 h-2 rounded-full bg-blue-600 mt-1 flex-shrink-0" />
                  )}
                </div>
              ))
            )}
          </div>

          <div className="p-2.5 border-t border-slate-100 text-center bg-slate-50/50 rounded-b-2xl">
            <Link
              to="/notifications"
              onClick={() => setIsOpen(false)}
              className="text-xs font-medium text-slate-700 hover:text-blue-600 transition block"
            >
              {t("notifications.viewAll") || "View all notifications →"}
            </Link>
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationBell;
