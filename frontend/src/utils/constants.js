let rawBase = import.meta.env.VITE_API_BASE_URL;
if (rawBase) {
  rawBase = rawBase.replace(/\/api\/?$/, "").replace(/\/+$/, "");
} else if (typeof window !== "undefined" && !window.location.hostname.includes("localhost")) {
  rawBase = "https://returnloop-backend.onrender.com";
} else {
  rawBase = "";
}

export const API_BASE_URL = rawBase;

export const CATEGORIES = [
  "Electronics",
  "ID & Cards",
  "Bags & Wallets",
  "Keys",
  "Books & Stationery",
  "Clothing & Accessories",
  "Bottles & Tumblers",
  "Other"
];

export const CAMPUS_LOCATIONS = [
  "Block 34",
  "Block 38",
  "Central Library",
  "UniMall",
  "Baldev Raj Mittal Unipolis",
  "Block 14 (Boys Hostel)",
  "Block 28 (Girls Hostel)",
  "Block 55",
  "Block 36",
  "Block 29",
  "Shanti Devi Mittal Auditorium",
  "Food Court / Kiosk Area",
  "Sports Stadium / Complex",
  "Main Gate / Security Post",
  "Other Campus Area"
];

export const STATUS_COLORS = {
  active: {
    bg: "bg-emerald-50 text-emerald-700 border-emerald-200",
    dot: "bg-emerald-500",
    label: "Active"
  },
  claim_pending: {
    bg: "bg-amber-50 text-amber-700 border-amber-200",
    dot: "bg-amber-500",
    label: "Claim Pending"
  },
  recovered: {
    bg: "bg-blue-50 text-blue-700 border-blue-200",
    dot: "bg-blue-500",
    label: "Recovered"
  },
  withdrawn: {
    bg: "bg-slate-100 text-slate-700 border-slate-200",
    dot: "bg-slate-400",
    label: "Withdrawn"
  },
  suspended: {
    bg: "bg-rose-50 text-rose-700 border-rose-200",
    dot: "bg-rose-500",
    label: "Suspended"
  },
  pending: {
    bg: "bg-amber-50 text-amber-700 border-amber-200",
    dot: "bg-amber-500",
    label: "Pending Verification"
  },
  approved: {
    bg: "bg-teal-50 text-teal-700 border-teal-200",
    dot: "bg-teal-500",
    label: "Approved for Handover"
  },
  rejected: {
    bg: "bg-rose-50 text-rose-700 border-rose-200",
    dot: "bg-rose-500",
    label: "Rejected"
  },
  more_info_needed: {
    bg: "bg-purple-50 text-purple-700 border-purple-200",
    dot: "bg-purple-500",
    label: "Additional Info Needed"
  },
  handover_completed: {
    bg: "bg-emerald-50 text-emerald-700 border-emerald-200",
    dot: "bg-emerald-500",
    label: "Handover Completed"
  }
};
