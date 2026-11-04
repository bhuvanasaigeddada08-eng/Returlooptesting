import React from "react";
import { AlertTriangle } from "lucide-react";
import Modal from "./Modal";

export const ConfirmDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = "Are you sure?",
  message = "This action cannot be undone. Please confirm to proceed.",
  confirmText = "Confirm",
  confirmVariant = "danger", // 'danger' | 'primary'
  loading = false
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} title={title} maxWidth="max-w-md">
      <div className="flex gap-4">
        <div className={`w-12 h-12 rounded-xl flex-shrink-0 flex items-center justify-center ${
          confirmVariant === "danger" ? "bg-rose-50 text-rose-600 border border-rose-200" : "bg-blue-50 text-blue-600 border border-blue-200"
        }`}>
          <AlertTriangle className="w-6 h-6" />
        </div>
        <div className="flex-1">
          <p className="text-sm text-slate-600 leading-relaxed">{message}</p>
        </div>
      </div>

      <div className="flex flex-col-reverse sm:flex-row justify-end gap-2.5 sm:gap-3 mt-6 pt-4 border-t border-slate-100">
        <button
          type="button"
          onClick={onClose}
          disabled={loading}
          className="w-full sm:w-auto px-4 py-2.5 rounded-xl border border-slate-200 text-sm font-medium text-slate-700 hover:bg-slate-50 transition text-center"
        >
          Cancel
        </button>
        <button
          type="button"
          onClick={onConfirm}
          disabled={loading}
          className={`w-full sm:w-auto justify-center px-4 py-2.5 rounded-xl text-sm font-medium text-white transition flex items-center gap-2 ${
            confirmVariant === "danger"
              ? "bg-rose-600 hover:bg-rose-700 disabled:bg-rose-400"
              : "bg-slate-900 hover:bg-slate-800 disabled:bg-slate-400"
          }`}
        >
          {loading ? "Processing..." : confirmText}
        </button>
      </div>
    </Modal>
  );
};

export default ConfirmDialog;
