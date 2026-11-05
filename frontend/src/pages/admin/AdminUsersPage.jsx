import React, { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { 
  Users, UserPlus, Search, Filter, Shield, User, 
  Trash2, Edit3, CheckCircle2, XCircle, AlertCircle, 
  RefreshCw, Key, Phone, Mail, Hash
} from "lucide-react";
import api from "../../services/api";
import { useAuth } from "../../context/AuthContext";
import Modal from "../../components/Modal";
import ConfirmDialog from "../../components/ConfirmDialog";
import EmptyState from "../../components/EmptyState";
import { TableRowSkeleton } from "../../components/LoadingSkeleton";

export const AdminUsersPage = () => {
  const { t } = useTranslation();
  const { user: currentAdmin } = useAuth();

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [roleFilter, setRoleFilter] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [totalCount, setTotalCount] = useState(0);

  // Modals state
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  // Form states
  const [formData, setFormData] = useState({
    display_name: "",
    email: "",
    phone: "",
    password: "",
    role: "student",
    is_active: true
  });
  const [formLoading, setFormLoading] = useState(false);
  const [formError, setFormError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const res = await api.getAdminUsers({
        q: searchQuery,
        role: roleFilter,
        page,
        per_page: 15
      });
      setUsers(res.users || []);
      setTotalPages(res.pages || 1);
      setTotalCount(res.total || 0);
    } catch (err) {
      console.error("Failed to load users:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [searchQuery, roleFilter, page]);

  const handleOpenCreate = () => {
    setFormData({
      display_name: "",
      email: "",
      phone: "",
      password: "",
      role: "student",
      is_active: true
    });
    setFormError("");
    setCreateModalOpen(true);
  };

  const handleOpenEdit = (user) => {
    setSelectedUser(user);
    setFormData({
      display_name: user.display_name || "",
      email: user.email || "",
      phone: user.phone || "",
      password: "", // empty means leave unchanged
      role: user.role || "student",
      is_active: user.is_active !== false
    });
    setFormError("");
    setEditModalOpen(true);
  };

  const handleOpenDelete = (user) => {
    setSelectedUser(user);
    setDeleteDialogOpen(true);
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    if (!formData.display_name.trim() || !formData.email.trim() || !formData.password) {
      setFormError("Please provide full name, email, and password.");
      return;
    }
    if (formData.password.length < 6) {
      setFormError("Password must be at least 6 characters.");
      return;
    }

    try {
      setFormLoading(true);
      const res = await api.createAdminUser(formData);
      setCreateModalOpen(false);
      setSuccessMessage(res.message || "Account created successfully.");
      setTimeout(() => setSuccessMessage(""), 4000);
      fetchUsers();
    } catch (err) {
      setFormError(err.message || "Failed to create account.");
    } finally {
      setFormLoading(false);
    }
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setFormError("");
    if (!formData.display_name.trim() || !formData.email.trim()) {
      setFormError("Please provide full name and email.");
      return;
    }

    try {
      setFormLoading(true);
      const payload = {
        display_name: formData.display_name.trim(),
        email: formData.email.trim(),
        phone: formData.phone.trim(),
        role: formData.role,
        is_active: formData.is_active
      };
      if (formData.password) {
        payload.password = formData.password;
      }
      const res = await api.updateAdminUser(selectedUser.id, payload);
      setEditModalOpen(false);
      setSuccessMessage(res.message || "Account updated successfully.");
      setTimeout(() => setSuccessMessage(""), 4000);
      fetchUsers();
    } catch (err) {
      setFormError(err.message || "Failed to update account.");
    } finally {
      setFormLoading(false);
    }
  };

  const handleDeleteConfirm = async () => {
    if (!selectedUser) return;
    try {
      setFormLoading(true);
      const res = await api.deleteAdminUser(selectedUser.id);
      setDeleteDialogOpen(false);
      setSuccessMessage(res.message || "Account removed.");
      setTimeout(() => setSuccessMessage(""), 4000);
      fetchUsers();
    } catch (err) {
      alert(err.message || "Failed to remove account.");
    } finally {
      setFormLoading(false);
    }
  };

  const adminCount = users.filter(u => u.role === "admin").length;
  const studentCount = users.filter(u => u.role === "student").length;

  return (
    <div className="space-y-6">
      {/* Top Banner & Metric Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Registered</span>
            <h3 className="text-2xl font-black text-slate-900 mt-1">{totalCount}</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-700 flex items-center justify-center font-bold">
            <Users className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-blue-600 uppercase tracking-wider">Campus Admins</span>
            <h3 className="text-2xl font-black text-blue-900 mt-1">{adminCount}</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 border border-blue-100 flex items-center justify-center">
            <Shield className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold text-teal-600 uppercase tracking-wider">Active Students</span>
            <h3 className="text-2xl font-black text-teal-900 mt-1">{studentCount}</h3>
          </div>
          <div className="w-12 h-12 rounded-2xl bg-teal-50 text-teal-600 border border-teal-100 flex items-center justify-center">
            <User className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Success Notification Alert */}
      {successMessage && (
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-sm font-semibold flex items-center gap-2.5 shadow-xs animate-in fade-in duration-200">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      {/* Control / Search / Action Bar */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-5 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row justify-between items-stretch sm:items-center gap-3">
          {/* Search box */}
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by student name, email, or registration ID..."
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                setPage(1);
              }}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-blue-600 bg-slate-50/50"
            />
          </div>

          {/* Role Filter & Add Button */}
          <div className="flex items-center gap-2">
            <select
              value={roleFilter}
              onChange={(e) => {
                setRoleFilter(e.target.value);
                setPage(1);
              }}
              className="px-3.5 py-2.5 rounded-xl border border-slate-200 text-xs font-semibold bg-white text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
            >
              <option value="">All Roles</option>
              <option value="student">Students Only</option>
              <option value="admin">Campus Admins</option>
            </select>

            <button
              onClick={fetchUsers}
              className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition cursor-pointer"
              title="Refresh"
            >
              <RefreshCw className="w-4 h-4" />
            </button>

            <button
              onClick={handleOpenCreate}
              className="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-sm cursor-pointer whitespace-nowrap"
            >
              <UserPlus className="w-4 h-4" />
              <span>Add Account</span>
            </button>
          </div>
        </div>
      </div>

      {/* Users Table / List */}
      <div className="bg-white rounded-3xl border border-slate-200/80 shadow-sm overflow-hidden">
        {loading ? (
          <div className="p-6 space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <TableRowSkeleton key={i} />
            ))}
          </div>
        ) : users.length === 0 ? (
          <div className="p-12 text-center">
            <EmptyState
              icon={Users}
              title="No Accounts Found"
              description="No user accounts match your current search or filter criteria."
              actionText="Add New Account"
              onAction={handleOpenCreate}
            />
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200/80 text-slate-500 font-bold uppercase tracking-wider">
                  <th className="py-3.5 px-4 sm:px-6">User & Identity</th>
                  <th className="py-3.5 px-4">Role & Status</th>
                  <th className="py-3.5 px-4 hidden md:table-cell">Contact & Reg ID</th>
                  <th className="py-3.5 px-4 hidden sm:table-cell">Activity</th>
                  <th className="py-3.5 px-4 sm:px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {users.map((u) => {
                  const isCurrentSelf = currentAdmin?.id === u.id;
                  const isAdminRole = u.role === "admin";
                  return (
                    <tr key={u.id} className="hover:bg-slate-50/70 transition">
                      {/* Name & Email */}
                      <td className="py-4 px-4 sm:px-6">
                        <div className="flex items-center gap-3">
                          <div className={`w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-sm flex-shrink-0 shadow-xs ${
                            isAdminRole 
                              ? "bg-blue-600 text-white" 
                              : "bg-slate-100 text-slate-700 border border-slate-200"
                          }`}>
                            {u.display_name?.charAt(0).toUpperCase() || "U"}
                          </div>
                          <div className="min-w-0">
                            <div className="flex items-center gap-2">
                              <span className="font-bold text-slate-900 text-sm truncate">{u.display_name}</span>
                              {isCurrentSelf && (
                                <span className="px-1.5 py-0.2 rounded text-[9px] font-extrabold bg-blue-100 text-blue-800 uppercase">
                                  You
                                </span>
                              )}
                            </div>
                            <span className="text-slate-500 text-[11px] truncate block">{u.email}</span>
                          </div>
                        </div>
                      </td>

                      {/* Role & Status */}
                      <td className="py-4 px-4">
                        <div className="space-y-1">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                            isAdminRole
                              ? "bg-blue-50 text-blue-700 border border-blue-200"
                              : "bg-slate-100 text-slate-700 border border-slate-200"
                          }`}>
                            {isAdminRole ? <Shield className="w-3 h-3 text-blue-600" /> : <User className="w-3 h-3 text-slate-500" />}
                            {isAdminRole ? "Campus Admin" : "Student"}
                          </span>

                          <div className="flex items-center gap-1.5 text-[11px]">
                            {u.is_active ? (
                              <span className="text-emerald-600 font-semibold flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" /> Active
                              </span>
                            ) : (
                              <span className="text-rose-600 font-semibold flex items-center gap-1">
                                <span className="w-1.5 h-1.5 rounded-full bg-rose-500" /> Suspended
                              </span>
                            )}
                          </div>
                        </div>
                      </td>

                      {/* Contact & Reg ID */}
                      <td className="py-4 px-4 hidden md:table-cell text-slate-600">
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-1 font-mono text-[11px] text-slate-700 font-semibold">
                            <Hash className="w-3 h-3 text-slate-400" />
                            <span>{u.student_id || "N/A"}</span>
                          </div>
                          <div className="flex items-center gap-1 text-[11px] text-slate-500">
                            <Phone className="w-3 h-3 text-slate-400" />
                            <span>{u.phone || "No phone"}</span>
                          </div>
                        </div>
                      </td>

                      {/* Activity */}
                      <td className="py-4 px-4 hidden sm:table-cell text-slate-500">
                        <div className="text-[11px]">
                          <span>{u.reports_count || 0} Reports</span>
                          <span className="mx-1">•</span>
                          <span>{u.claims_count || 0} Claims</span>
                        </div>
                      </td>

                      {/* Actions */}
                      <td className="py-4 px-4 sm:px-6 text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <button
                            onClick={() => handleOpenEdit(u)}
                            className="px-3 py-1.5 rounded-xl border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 font-semibold transition flex items-center gap-1 cursor-pointer"
                            title="Edit Account Details"
                          >
                            <Edit3 className="w-3.5 h-3.5 text-blue-600" />
                            <span>Edit</span>
                          </button>

                          <button
                            onClick={() => handleOpenDelete(u)}
                            disabled={isCurrentSelf}
                            className={`p-1.5 rounded-xl border transition cursor-pointer ${
                              isCurrentSelf
                                ? "opacity-30 border-slate-100 text-slate-300 cursor-not-allowed"
                                : "border-slate-200 hover:border-rose-200 bg-white hover:bg-rose-50 text-slate-400 hover:text-rose-600"
                            }`}
                            title={isCurrentSelf ? "Cannot delete yourself" : "Remove Account"}
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* CREATE USER MODAL */}
      <Modal
        isOpen={createModalOpen}
        onClose={() => setCreateModalOpen(false)}
        title="Add New Account"
        maxWidth="max-w-md"
      >
        <form onSubmit={handleCreateSubmit} className="space-y-4">
          {formError && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{formError}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Account Role / Permissions <span className="text-rose-500">*</span>
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, role: "student" }))}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
                  formData.role === "student"
                    ? "bg-teal-50 border-teal-500 text-teal-800 ring-1 ring-teal-500"
                    : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                }`}
              >
                <User className="w-3.5 h-3.5" />
                Student
              </button>
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, role: "admin" }))}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
                  formData.role === "admin"
                    ? "bg-blue-50 border-blue-500 text-blue-800 ring-1 ring-blue-500"
                    : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                }`}
              >
                <Shield className="w-3.5 h-3.5" />
                Campus Admin
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Full Name <span className="text-rose-500">*</span>
            </label>
            <input
              type="text"
              required
              value={formData.display_name}
              onChange={(e) => setFormData(prev => ({ ...prev, display_name: e.target.value }))}
              placeholder="e.g. Ramesh Kumar"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address <span className="text-rose-500">*</span>
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              placeholder="e.g. ramesh@lpu.in"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
              placeholder="e.g. +91 98765 43210"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Temporary / Default Password <span className="text-rose-500">*</span>
            </label>
            <input
              type="password"
              required
              value={formData.password}
              onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
              placeholder="Minimum 6 characters"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setCreateModalOpen(false)}
              className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={formLoading}
              className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition shadow-sm cursor-pointer disabled:opacity-50"
            >
              {formLoading ? "Creating Account..." : "Create Account"}
            </button>
          </div>
        </form>
      </Modal>

      {/* EDIT USER MODAL */}
      <Modal
        isOpen={editModalOpen}
        onClose={() => setEditModalOpen(false)}
        title={`Edit Account: ${selectedUser?.display_name || ""}`}
        maxWidth="max-w-md"
      >
        <form onSubmit={handleEditSubmit} className="space-y-4">
          {formError && (
            <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{formError}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Account Role
            </label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, role: "student" }))}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
                  formData.role === "student"
                    ? "bg-teal-50 border-teal-500 text-teal-800 ring-1 ring-teal-500"
                    : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                }`}
              >
                <User className="w-3.5 h-3.5" />
                Student
              </button>
              <button
                type="button"
                onClick={() => setFormData(prev => ({ ...prev, role: "admin" }))}
                className={`py-2 px-3 rounded-xl border text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
                  formData.role === "admin"
                    ? "bg-blue-50 border-blue-500 text-blue-800 ring-1 ring-blue-500"
                    : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                }`}
              >
                <Shield className="w-3.5 h-3.5" />
                Campus Admin
              </button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Full Name
            </label>
            <input
              type="text"
              required
              value={formData.display_name}
              onChange={(e) => setFormData(prev => ({ ...prev, display_name: e.target.value }))}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Phone Number
            </label>
            <input
              type="tel"
              value={formData.phone}
              onChange={(e) => setFormData(prev => ({ ...prev, phone: e.target.value }))}
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Change / Reset Password <span className="text-slate-400 font-normal">(leave blank to keep unchanged)</span>
            </label>
            <input
              type="password"
              value={formData.password}
              onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
              placeholder="Enter new password if resetting"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Account Status
            </label>
            <div className="flex items-center gap-3">
              <label className="flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-700">
                <input
                  type="radio"
                  name="is_active"
                  checked={formData.is_active === true}
                  onChange={() => setFormData(prev => ({ ...prev, is_active: true }))}
                  className="text-blue-600"
                />
                Active
              </label>
              <label className="flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-700">
                <input
                  type="radio"
                  name="is_active"
                  checked={formData.is_active === false}
                  onChange={() => setFormData(prev => ({ ...prev, is_active: false }))}
                  className="text-rose-600"
                />
                Suspended / Inactive
              </label>
            </div>
          </div>

          <div className="flex justify-end gap-2 pt-4 border-t border-slate-100">
            <button
              type="button"
              onClick={() => setEditModalOpen(false)}
              className="px-4 py-2 rounded-xl border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={formLoading}
              className="px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold transition shadow-sm cursor-pointer disabled:opacity-50"
            >
              {formLoading ? "Saving Changes..." : "Save Changes"}
            </button>
          </div>
        </form>
      </Modal>

      {/* DELETE CONFIRM DIALOG */}
      <ConfirmDialog
        isOpen={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
        onConfirm={handleDeleteConfirm}
        title="Remove User Account"
        message={`Are you sure you want to permanently remove the account for "${selectedUser?.display_name}" (${selectedUser?.email})? All associated reports, claims, and activity records will be deleted.`}
        confirmText="Yes, Remove Account"
        confirmVariant="danger"
        loading={formLoading}
      />
    </div>
  );
};

export default AdminUsersPage;

