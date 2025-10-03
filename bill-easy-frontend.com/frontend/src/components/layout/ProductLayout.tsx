// src/components/layout/ProductLayout.tsx
import React from "react";
import { Outlet } from "react-router-dom";

const ProductLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
      <div className="w-full max-w-4xl bg-white shadow-md rounded-xl p-8">
        {/* Render Products page here */}
        <Outlet />
      </div>
    </div>
  );
};

export default ProductLayout;

