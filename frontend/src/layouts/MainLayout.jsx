import React from "react";
import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import BottomNav from "../components/BottomNav";
import EasyModeVoiceAssistant from "../components/EasyModeVoiceAssistant";

export const MainLayout = () => {
  return (
    <div className="min-h-screen flex flex-col bg-slate-100 text-slate-900 selection:bg-blue-600 selection:text-white">
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5 sm:py-8 pb-20 sm:pb-8">
        <Outlet />
      </main>
      <Footer />
      <BottomNav />
      <EasyModeVoiceAssistant />
    </div>
  );
};

export default MainLayout;
