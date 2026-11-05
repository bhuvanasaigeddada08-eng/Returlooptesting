import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { 
  Bell, Check, Sparkles, AlertCircle, ShieldCheck, 
  Trash2, Filter, CheckCircle2 
} from "lucide-react";
import api from "../services/api";
import EmptyState from "../components/EmptyState";
import TranslatedText from "../components/TranslatedText";

export const NotificationsPage = () => {
  const { t } = useTranslation();
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterUnreadOnly, setFilterUnreadOnly] = useState(false);
  const navigate = useNavigate();

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      const res = await api.getNotifications();
      setNotifications(res.notifications || []);
    } catch (err) {
      console.error("Failed to load notifications:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  const handleMarkAsRead = async (id, e) => {
    e.stopPropagation();
    try {
      await api.markNotificationRead(id);
      setNotifications(prev =>
        prev.map(n => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleMarkAllRead = async () => {
    try {
      await api.markAllNotificationsRead();
      setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleNotificationClick = async (notif) => {
    if (!notif.is_read) {
      try {
        await api.markNotificationRead(notif.id);
      } catch (e) {}
    }
    if (notif.link) {
      navigate(notif.link);
    }
  };

  const displayedNotifications = filterUnreadOnly
    ? notifications.filter(n => !n.is_read)
    : notifications;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-sm flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-blue-600" />
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">{t("notifications.title") || "Campus Notifications"}</h1>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            {t("notifications.subtitle") || "Stay updated on matches, claim status updates, and security alerts."}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setFilterUnreadOnly(!filterUnreadOnly)}
            className={`px-3 py-1.5 rounded-xl border text-xs font-semibold transition cursor-pointer ${
              filterUnreadOnly
                ? "bg-slate-900 text-white border-slate-900"
                : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
            }`}
          >
            {filterUnreadOnly ? (t("notifications.filterUnread") || "Unread Only") : (t("notifications.allUpdates") || "All Notifications")}
          </button>

          {notifications.some(n => !n.is_read) && (
            <button
              onClick={handleMarkAllRead}
              className="px-3.5 py-1.5 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 border border-blue-200 text-xs font-semibold transition flex items-center gap-1.5 cursor-pointer"
            >
              <Check className="w-4 h-4" /> {t("notifications.markAllRead") || "Mark all read"}
            </button>
          )}
        </div>
      </div>

      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-8 space-y-4">
            <div className="h-16 bg-slate-100 rounded-2xl animate-pulse" />
            <div className="h-16 bg-slate-100 rounded-2xl animate-pulse" />
          </div>
        ) : displayedNotifications.length === 0 ? (
          <div className="p-12 text-center">
            <EmptyState
              icon={Bell}
              title={filterUnreadOnly ? (t("notifications.noUnread") || "No unread alerts") : (t("notifications.empty") || "No notifications yet")}
              description={t("notifications.emptyDesc") || "You will receive real-time alerts when matches are found or security reviews your claim."}
            />
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {displayedNotifications.map((notif) => (
              <div
                key={notif.id}
                onClick={() => handleNotificationClick(notif)}
                className={`p-5 flex items-start justify-between gap-4 cursor-pointer transition ${
                  !notif.is_read ? "bg-blue-50/50 hover:bg-blue-50/80" : "hover:bg-slate-50"
                }`}
              >
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                    {notif.notification_type === "match" ? (
                      <Sparkles className="w-5 h-5 text-blue-600" />
                    ) : notif.notification_type === "claim_update" ? (
                      <ShieldCheck className="w-5 h-5 text-teal-600" />
                    ) : (
                      <AlertCircle className="w-5 h-5 text-blue-600" />
                    )}
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-bold text-slate-900 text-sm">
                        <TranslatedText text={notif.title} />
                      </h4>
                      {!notif.is_read && (
                        <span className="w-2 h-2 rounded-full bg-blue-600" />
                      )}
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed max-w-lg">
                      <TranslatedText text={notif.message} />
                    </p>
                    <span className="text-[11px] text-slate-400 block pt-1">
                      {new Date(notif.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                {!notif.is_read && (
                  <button
                    onClick={(e) => handleMarkAsRead(notif.id, e)}
                    className="p-1.5 rounded-lg hover:bg-blue-100 text-blue-600 transition text-xs font-semibold cursor-pointer"
                    title={t("notifications.markAsRead") || "Mark as read"}
                  >
                    <CheckCircle2 className="w-4 h-4" />
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default NotificationsPage;
