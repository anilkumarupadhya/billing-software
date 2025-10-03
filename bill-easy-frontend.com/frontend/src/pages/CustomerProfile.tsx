// src/pages/CustomerProfile.tsx
import React from "react";

const CustomerProfile: React.FC = () => {
  // Example customer data (later this will come from API/backend)
  const customer = {
    name: "Ravi Traders",
    email: "ravi.traders@example.com",
    phone: "+91 9876543210",
    address: "12 Market Street, Delhi",
    gst: "07ABCDE1234F1Z5",
    outstandingBalance: 12500,
  };

  const invoices = [
    { id: "INV-1001", date: "2025-09-15", total: 5000, status: "Paid" },
    { id: "INV-1002", date: "2025-09-20", total: 7500, status: "Pending" },
  ];

  const payments = [
    { id: "PAY-2001", date: "2025-09-18", amount: 5000, method: "Bank Transfer" },
  ];

  return (
    <div className="space-y-8">
      {/* Customer Header */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-bold mb-2">{customer.name}</h2>
        <p className="text-gray-600">{customer.email}</p>
        <p className="text-gray-600">{customer.phone}</p>
        <p className="text-gray-600">{customer.address}</p>
        <p className="text-gray-600">GST: {customer.gst}</p>
        <div className="mt-4">
          <span className="text-lg font-semibold">
            Outstanding Balance: ₹{customer.outstandingBalance.toLocaleString()}
          </span>
        </div>
      </div>

      {/* Invoices Section */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">Invoices</h3>
        {invoices.length === 0 ? (
          <p className="text-gray-500">No invoices found.</p>
        ) : (
          <table className="w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border">Invoice ID</th>
                <th className="p-2 border">Date</th>
                <th className="p-2 border">Total</th>
                <th className="p-2 border">Status</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv) => (
                <tr key={inv.id} className="text-center">
                  <td className="p-2 border">{inv.id}</td>
                  <td className="p-2 border">{inv.date}</td>
                  <td className="p-2 border">₹{inv.total.toLocaleString()}</td>
                  <td
                    className={`p-2 border font-medium ${
                      inv.status === "Paid" ? "text-green-600" : "text-orange-600"
                    }`}
                  >
                    {inv.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Payments Section */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h3 className="text-xl font-semibold mb-4">Payments</h3>
        {payments.length === 0 ? (
          <p className="text-gray-500">No payments found.</p>
        ) : (
          <table className="w-full border">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border">Payment ID</th>
                <th className="p-2 border">Date</th>
                <th className="p-2 border">Amount</th>
                <th className="p-2 border">Method</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((pay) => (
                <tr key={pay.id} className="text-center">
                  <td className="p-2 border">{pay.id}</td>
                  <td className="p-2 border">{pay.date}</td>
                  <td className="p-2 border">₹{pay.amount.toLocaleString()}</td>
                  <td className="p-2 border">{pay.method}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default CustomerProfile;

