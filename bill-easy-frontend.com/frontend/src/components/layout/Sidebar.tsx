// src/components/layout/Sidebar.tsx
import React from "react";
import { Link } from "react-router-dom";

const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 h-screen bg-gradient-to-b from-blue-500 to-blue-700 text-white flex flex-col p-6">
      {/* Logo / Title */}
      <h2 className="text-2xl font-bold mb-8">BillEasy</h2>

      {/* MAIN NAV */}
      <nav className="flex flex-col space-y-4">
        {/* Main Section */}
        <p className="text-sm text-blue-200 uppercase tracking-wide">Main</p>
        <Link to="/dashboard" className="hover:bg-blue-600 rounded-md px-4 py-2">
          Dashboard
        </Link>

        {/* Customer Management Section */}
        <p className="text-sm text-blue-200 uppercase mt-6 tracking-wide">
          Customer Management
        </p>
        <ul className="ml-4 space-y-1">
          <li>
            <Link to="/customers" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Customers
            </Link>
          </li>
          <li>
            <Link to="/customer-profile" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Customer Profile
            </Link>
          </li>
        </ul>

        {/* Billing Section */}
        <p className="text-sm text-blue-200 uppercase mt-6 tracking-wide">
          Billing
        </p>
        <ul className="ml-4 space-y-1">
          <li>
            <Link to="/products" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Products
            </Link>
          </li>
          <li>
            <Link to="/invoices" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Invoices
            </Link>
          </li>
          <li>
            <Link to="/payments" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Payments
            </Link>
          </li>
        </ul>
      </nav>

      {/* SETTINGS / SUPPORT */}
      <div className="mt-auto pt-8 border-t border-blue-400">
        <p className="text-sm text-blue-200 uppercase tracking-wide">Settings</p>
        <ul className="ml-4 mt-2 space-y-1">
          <li>
            <Link to="/settings" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Settings
            </Link>
          </li>
          <li>
            <Link to="/support" className="block hover:bg-blue-600 rounded-md px-4 py-2">
              Support
            </Link>
          </li>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;

