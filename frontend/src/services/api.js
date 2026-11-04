import { API_BASE_URL } from "../utils/constants";

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  getToken() {
    return localStorage.getItem("returnloop_token");
  }

  setToken(token) {
    if (token) {
      localStorage.setItem("returnloop_token", token);
    } else {
      localStorage.removeItem("returnloop_token");
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = options.headers || {};

    const token = this.getToken();
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data.error || (data.errors ? data.errors.join(", ") : "Request failed");
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  }

  // Auth endpoints
  async register(data) {
    const res = await this.request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data)
    });
    if (res.token) this.setToken(res.token);
    return res;
  }

  async login(email, password) {
    const res = await this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    if (res.token) this.setToken(res.token);
    return res;
  }

  async getGoogleConfig() {
    return this.request("/api/auth/google/config");
  }

  async loginWithGoogle(credential) {
    const res = await this.request("/api/auth/google", {
      method: "POST",
      body: JSON.stringify({ credential })
    });
    if (res.token) this.setToken(res.token);
    return res;
  }

  async logout() {
    try {
      await this.request("/api/auth/logout", { method: "POST" });
    } finally {
      this.setToken(null);
    }
  }

  async getMe() {
    return this.request("/api/auth/me");
  }

  async changePassword(current_password, new_password) {
    return this.request("/api/auth/change-password", {
      method: "POST",
      body: JSON.stringify({ current_password, new_password })
    });
  }

  async updateProfile(profileData) {
    return this.request("/api/auth/profile", {
      method: "PATCH",
      body: JSON.stringify(profileData)
    });
  }

  // Reports
  async getReports(params = {}) {
    const query = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== "") {
        query.append(key, params[key]);
      }
    });
    return this.request(`/api/reports?${query.toString()}`);
  }

  async getMyReports(type = "") {
    return this.request(`/api/reports/my${type ? `?type=${type}` : ""}`);
  }

  async getReport(id) {
    return this.request(`/api/reports/${id}`);
  }

  async createReport(reportData) {
    return this.request("/api/reports", {
      method: "POST",
      body: JSON.stringify(reportData)
    });
  }

  async updateReport(id, reportData) {
    return this.request(`/api/reports/${id}`, {
      method: "PATCH",
      body: JSON.stringify(reportData)
    });
  }

  async recoverReport(id) {
    return this.request(`/api/reports/${id}/recover`, {
      method: "POST"
    });
  }

  async withdrawReport(id) {
    return this.request(`/api/reports/${id}/withdraw`, {
      method: "POST"
    });
  }

  async uploadReportImage(reportId, file) {
    const formData = new FormData();
    formData.append("file", file);
    return this.request(`/api/reports/${reportId}/images`, {
      method: "POST",
      body: formData
    });
  }

  async deleteReportImage(imageId) {
    return this.request(`/api/reports/images/${imageId}`, {
      method: "DELETE"
    });
  }

  // Matches
  async getMatches(reportId) {
    return this.request(`/api/matches/${reportId}`);
  }

  // Claims
  async submitClaim(reportId, explanation) {
    return this.request(`/api/claims/${reportId}`, {
      method: "POST",
      body: JSON.stringify({ private_ownership_explanation: explanation })
    });
  }

  async getMyClaims() {
    return this.request("/api/claims/my");
  }

  async getClaim(id) {
    return this.request(`/api/claims/${id}`);
  }

  async withdrawClaim(id) {
    return this.request(`/api/claims/${id}/withdraw`, {
      method: "POST"
    });
  }

  // Notifications
  async getNotifications() {
    return this.request("/api/notifications");
  }

  async markNotificationRead(id) {
    return this.request(`/api/notifications/${id}/read`, {
      method: "POST"
    });
  }

  async markAllNotificationsRead() {
    return this.request("/api/notifications/read-all", {
      method: "POST"
    });
  }

  // Admin
  async getAdminDashboard() {
    return this.request("/api/admin/dashboard");
  }

  async getAdminReports(params = {}) {
    const query = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== "") {
        query.append(key, params[key]);
      }
    });
    return this.request(`/api/admin/reports?${query.toString()}`);
  }

  async updateAdminReportStatus(id, status, reason = "") {
    return this.request(`/api/admin/reports/${id}/status`, {
      method: "PATCH",
      body: JSON.stringify({ status, reason })
    });
  }

  async getAdminClaims(params = {}) {
    const query = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== "") {
        query.append(key, params[key]);
      }
    });
    return this.request(`/api/admin/claims?${query.toString()}`);
  }

  async approveClaim(id, reason = "") {
    return this.request(`/api/admin/claims/${id}/approve`, {
      method: "POST",
      body: JSON.stringify({ reason })
    });
  }

  async rejectClaim(id, reason) {
    return this.request(`/api/admin/claims/${id}/reject`, {
      method: "POST",
      body: JSON.stringify({ reason })
    });
  }

  async requestMoreInfo(id, message) {
    return this.request(`/api/admin/claims/${id}/request-information`, {
      method: "POST",
      body: JSON.stringify({ message })
    });
  }

  async recordHandover(id, notes) {
    return this.request(`/api/admin/claims/${id}/handover`, {
      method: "POST",
      body: JSON.stringify({ notes })
    });
  }

  async getAuditLogs(page = 1) {
    return this.request(`/api/admin/audit-logs?page=${page}`);
  }

  async translateTexts(texts, targetLang) {
    if (!targetLang || targetLang === "en" || !texts || texts.length === 0) return {};
    try {
      const res = await this.request("/api/translate", {
        method: "POST",
        body: JSON.stringify({ texts, target_lang: targetLang })
      });
      return res.translations || {};
    } catch (err) {
      console.warn("Translation service warning:", err);
      return {};
    }
  }
}

export const api = new ApiService();
export default api;
