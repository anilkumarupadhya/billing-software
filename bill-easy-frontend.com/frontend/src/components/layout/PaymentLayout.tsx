// src/components/layout/PaymentLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";

const PaymentLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <div className="w-full max-w-4xl bg-white shadow-md rounded-xl p-8">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Payments</h1>
        {/* This renders the Payments page */}
        <Outlet />
      </div>
    </div>
  );
};

export default PaymentLayout;

