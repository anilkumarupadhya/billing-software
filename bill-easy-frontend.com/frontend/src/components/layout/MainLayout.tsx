// src/components/layout/MainLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";

const MainLayout: React.FC = () => {
  return (
    <div
      className="min-h-screen flex bg-center bg-no-repeat bg-cover"
      style={{ backgroundImage: "url('/images/k-mitch-hodge-U1qm4IP44Rw-unsplash.jpg')" }}
    >
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-col flex-1 bg-white/70 backdrop-blur-sm min-h-screen">
        <Header />
        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default MainLayout;

