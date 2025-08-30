import React, { useEffect, useState } from "react";
import axios from "axios";
import CustomerForm from "../components/CustomerForm";

interface Customer {
  id: number;
  name: string;
  email: string;
  phone: string;
}

const Customers: React.FC = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);

  useEffect(() => {
    axios.get("/api/v1/customers").then((res) => setCustomers(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Customers</h1>
      <CustomerForm />
      <ul className="mt-6 space-y-2">
        {customers.map((c) => (
          <li key={c.id} className="border p-2 rounded">
            <p className="font-semibold">{c.name}</p>
            <p>{c.email} | {c.phone}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Customers;
