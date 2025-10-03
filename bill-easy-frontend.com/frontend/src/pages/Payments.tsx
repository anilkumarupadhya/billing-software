// src/pages/Payments.tsx
import React, { useState } from "react";

interface Payment {
  id: number;
  invoiceNo: string;
  customer: string;
  amount: number;
  status: "Paid" | "Pending" | "Overdue";
  date: string;
}

const Payments: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([
    {
      id: 1,
      invoiceNo: "INV-1001",
      customer: "ABC Traders",
      amount: 25000,
      status: "Pending",
      date: "2025-09-28",
    },
    {
      id: 2,
      invoiceNo: "INV-1002",
      customer: "XYZ Wholesalers",
      amount: 18000,
      status: "Paid",
      date: "2025-09-20",
    },
    {
      id: 3,
      invoiceNo: "INV-1003",
      customer: "Global Supplies",
      amount: 32000,
      status: "Overdue",
      date: "2025-09-10",
    },
  ]);

  const totalDue = payments
    .filter((p) => p.status === "Pending" || p.status === "Overdue")
    .reduce((acc, p) => acc + p.amount, 0);

  const totalPaid = payments
    .filter((p) => p.status === "Paid")
    .reduce((acc, p) => acc + p.amount, 0);

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-bold">Payments</h2>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl shadow text-center">
          <h3 className="text-gray-500">Total Due</h3>
          <p className="text-xl font-bold text-red-500">₹{totalDue.toLocaleString()}</p>
        </div>
        <div className="bg-white p-4 rounded-xl shadow text-center">
          <h3 className="text-gray-500">Total Paid</h3>
          <p className="text-xl font-bold text-green-600">₹{totalPaid.toLocaleString()}</p>
        </div>
        <div className="bg-white p-4 rounded-xl shadow text-center">
          <h3 className="text-gray-500">Transactions</h3>
          <p className="text-xl font-bold">{payments.length}</p>
        </div>
      </div>

      {/* Outstanding Payments */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h3 className="text-lg font-semibold mb-3">Outstanding Invoices</h3>
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 border">Invoice No</th>
              <th className="p-2 border">Customer</th>
              <th className="p-2 border">Amount</th>
              <th className="p-2 border">Status</th>
              <th className="p-2 border">Date</th>
              <th className="p-2 border">Action</th>
            </tr>
          </thead>
          <tbody>
            {payments.map((p) => (
              <tr key={p.id}>
                <td className="p-2 border">{p.invoiceNo}</td>
                <td className="p-2 border">{p.customer}</td>
                <td className="p-2 border">₹{p.amount.toLocaleString()}</td>
                <td
                  className={`p-2 border font-semibold ${
                    p.status === "Paid"
                      ? "text-green-600"
                      : p.status === "Overdue"
                      ? "text-red-600"
                      : "text-yellow-600"
                  }`}
                >
                  {p.status}
                </td>
                <td className="p-2 border">{p.date}</td>
                <td className="p-2 border text-center">
                  {p.status !== "Paid" ? (
                    <button className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">
                      Pay Now
                    </button>
                  ) : (
                    "-"
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add Payment (Manual Entry) */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h3 className="text-lg font-semibold mb-3">Record a Payment</h3>
        <form className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            placeholder="Invoice No"
            className="border p-2 rounded"
            required
          />
          <input
            type="number"
            placeholder="Amount"
            className="border p-2 rounded"
            required
          />
          <select className="border p-2 rounded">
            <option>Cash</option>
            <option>Bank Transfer</option>
            <option>Credit</option>
            <option>UPI</option>
          </select>
          <button
            type="submit"
            className="col-span-1 md:col-span-3 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Save Payment
          </button>
        </form>
      </div>
    </div>
  );
};

export default Payments;

