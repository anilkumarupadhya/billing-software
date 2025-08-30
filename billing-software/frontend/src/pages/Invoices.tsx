import React, { useEffect, useState } from "react";
import axios from "axios";
import InvoiceForm from "../components/InvoiceForm";

interface Invoice {
  id: number;
  customer_id: number;
  total: number;
  status: string;
}

const Invoices: React.FC = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);

  useEffect(() => {
    axios.get("/api/v1/invoices").then((res) => setInvoices(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Invoices</h1>
      <InvoiceForm />
      <ul className="mt-6 space-y-2">
        {invoices.map((inv) => (
          <li key={inv.id} className="border p-2 rounded">
            <p className="font-semibold">Invoice #{inv.id}</p>
            <p>Total: ₹{inv.total}</p>
            <p>Status: {inv.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Invoices;
