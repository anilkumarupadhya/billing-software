// src/components/layout/CustomerLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";

const CustomerLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-4xl bg-white shadow-lg rounded-lg p-8">
        <Outlet />
      </div>
    </div>
  );
};

export default CustomerLayout;

