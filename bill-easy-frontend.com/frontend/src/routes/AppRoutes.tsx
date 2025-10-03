// src/routes/AppRoutes.tsx
import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "../components/layout/MainLayout";
import CustomerLayout from "../components/layout/CustomerLayout";
import InvoiceLayout from "../components/layout/InvoiceLayout";
import PaymentLayout from "../components/layout/PaymentLayout";
import ProductLayout from "../components/layout/ProductLayout";
import CustomerProfileLayout from "../components/layout/CustomerProfileLayout";

import Dashboard from "../pages/Dashboard";
import Customers from "../pages/Customers";
import CustomerProfile from "../pages/CustomerProfile";
import Products from "../pages/Products";
import Invoices from "../pages/Invoices";
import Payments from "../pages/Payments";

const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Main layout for standard pages */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="dashboard" element={<Dashboard />} />
      </Route>

      {/* Product layout for products only */}
      <Route path="/products" element={<ProductLayout />}>
        <Route index element={<Products />} />
      </Route>

      {/* Invoice layout for invoices only */}
      <Route path="/invoices" element={<InvoiceLayout />}>
        <Route index element={<Invoices />} />
      </Route>

      {/* Payment layout for payments only */}
      <Route path="/payments" element={<PaymentLayout />}>
        <Route index element={<Payments />} />
      </Route>

      {/* Customer layout for customer form only */}
      <Route path="/customers" element={<CustomerLayout />}>
        <Route index element={<Customers />} />
      </Route>

      {/* CustomerProfile layout for profile page */}
      <Route path="/customer-profile" element={<CustomerProfileLayout />}>
        <Route index element={<CustomerProfile />} />
      </Route>

      {/* Catch-all: redirect to dashboard */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes;

