// src/components/layout/InvoiceLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";

const InvoiceLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <main className="bg-white p-6 rounded-lg shadow-md w-full max-w-4xl">
        <Outlet />
      </main>
    </div>
  );
};

export default InvoiceLayout;

