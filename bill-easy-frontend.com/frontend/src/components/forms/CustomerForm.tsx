// src/components/forms/CustomerForm.tsx
import React, { useState } from "react";
import axios from "axios";

interface CustomerFormProps {
  setCustomers?: React.Dispatch<React.SetStateAction<any[]>>;
}

const CustomerForm: React.FC<CustomerFormProps> = ({ setCustomers }) => {
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    gst_no: "",
    shipping_address: "",
    billing_address: "",
    eway: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await axios.post("/api/v1/customers", form);
      if (setCustomers) setCustomers((prev) => [...prev, res.data]);

      setForm({
        name: "",
        email: "",
        phone: "",
        gst_no: "",
        shipping_address: "",
        billing_address: "",
        eway: "",
      });
    } catch (err) {
      console.error("Error creating customer", err);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow-lg rounded-lg p-8 max-w-3xl mx-auto"
    >
      <h2 className="text-2xl font-bold mb-6 text-center">Customer Form</h2>

      {/* Name, Email */}
      <div className="flex flex-col md:flex-row md:items-center mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium">
          Name*
        </label>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          required
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      <div className="flex flex-col md:flex-row md:items-center mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium">Email</label>
        <input
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Phone, GST */}
      <div className="flex flex-col md:flex-row md:items-center mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium">Phone*</label>
        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          required
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      <div className="flex flex-col md:flex-row md:items-center mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium">GST No</label>
        <input
          name="gst_no"
          value={form.gst_no}
          onChange={handleChange}
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Shipping Address */}
      <div className="flex flex-col md:flex-row md:items-start mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium mt-1">
          Shipping Address*
        </label>
        <textarea
          name="shipping_address"
          value={form.shipping_address}
          onChange={handleChange}
          required
          rows={3}
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Billing Address */}
      <div className="flex flex-col md:flex-row md:items-start mb-4 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium mt-1">
          Billing Address*
        </label>
        <textarea
          name="billing_address"
          value={form.billing_address}
          onChange={handleChange}
          required
          rows={3}
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* E-Way */}
      <div className="flex flex-col md:flex-row md:items-center mb-6 gap-4">
        <label className="w-full md:w-1/3 text-gray-700 font-medium">E-Way</label>
        <input
          name="eway"
          value={form.eway}
          onChange={handleChange}
          className="w-full md:w-2/3 border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
      </div>

      {/* Submit Button */}
      <div className="text-center">
        <button
          type="submit"
          className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition"
        >
          Submit
        </button>
      </div>
    </form>
  );
};

export default CustomerForm;

