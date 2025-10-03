// src/components/layout/CustomerProfileLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";

const CustomerProfileLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex justify-center items-start p-6">
      <div className="w-full max-w-4xl bg-white shadow-lg rounded-xl p-8">
        {/* Page content will be rendered here */}
        <Outlet />
      </div>
    </div>
  );
};

export default CustomerProfileLayout;

