import React, { useEffect, useState } from "react";
import axios from "axios";
import PaymentForm from "../components/PaymentForm";

interface Payment {
  id: number;
  invoice_id: number;
  amount: number;
  method: string;
}

const Payments: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);

  useEffect(() => {
    axios.get("/api/v1/payments").then((res) => setPayments(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Payments</h1>
      <PaymentForm />
      <ul className="mt-6 space-y-2">
        {payments.map((pay) => (
          <li key={pay.id} className="border p-2 rounded">
            <p>Invoice #{pay.invoice_id}</p>
            <p>Amount: ₹{pay.amount} ({pay.method})</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Payments;
