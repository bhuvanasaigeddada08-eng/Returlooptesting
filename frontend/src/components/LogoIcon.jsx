import React from "react";

export const LogoIcon = ({ className = "w-9 h-9" }) => {
  return (
    <div className={`${className} rounded-xl overflow-hidden shadow-sm flex items-center justify-center flex-shrink-0 border border-slate-700/60 bg-slate-900`}>
      <svg
        viewBox="0 0 100 100"
        className="w-full h-full"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="rl-nav-grad-1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="50%" stopColor="#06b6d4" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>

          <linearGradient id="rl-nav-grad-2" x1="100%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stopColor="#60a5fa" />
            <stop offset="100%" stopColor="#38bdf8" />
          </linearGradient>

          <filter id="rl-nav-glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Background Canvas */}
        <rect width="100" height="100" rx="24" fill="#0f172a" />
        <rect x="2" y="2" width="96" height="96" rx="22" stroke="white" strokeOpacity="0.12" strokeWidth="2" />

        {/* Outer Loop Orbit */}
        <path
          d="M 28 52 C 28 35, 42 24, 60 24 C 74 24, 82 33, 82 44 C 82 56, 70 64, 52 74 C 40 80, 24 76, 24 64"
          stroke="url(#rl-nav-grad-1)"
          strokeWidth="7.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          filter="url(#rl-nav-glow)"
        />

        {/* Arrow Tip for Returning Flow */}
        <path
          d="M 76 33 L 84 44 L 72 47"
          stroke="url(#rl-nav-grad-1)"
          strokeWidth="6.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        />

        {/* Returning Counter Loop */}
        <path
          d="M 72 48 C 72 65, 58 76, 40 76 C 26 76, 18 67, 18 56 C 18 44, 30 36, 48 26 C 60 20, 76 24, 76 36"
          stroke="url(#rl-nav-grad-2)"
          strokeWidth="7"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray="1.5 2.5"
        />

        {/* Center Recovery Beacon Pin */}
        <circle cx="50" cy="50" r="8" fill="#f59e0b" filter="url(#rl-nav-glow)" />
        <circle cx="50" cy="50" r="3.5" fill="#ffffff" />
      </svg>
    </div>
  );
};

export default LogoIcon;
