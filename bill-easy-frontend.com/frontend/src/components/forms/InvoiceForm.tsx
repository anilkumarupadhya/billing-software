import React from "react";

const InvoiceForm: React.FC = () => {
  return (
    <form className="p-4 bg-white shadow-md rounded-md">
      <h2 className="text-lg font-bold mb-4">Create / Edit Invoice</h2>
      <div className="mb-2">
        <label className="block mb-1">Customer</label>
        <input type="text" className="border p-2 w-full" placeholder="Customer Name" />
      </div>
      <div className="mb-2">
        <label className="block mb-1">Amount</label>
        <input type="number" className="border p-2 w-full" placeholder="Total Amount" />
      </div>
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded mt-2">Submit</button>
    </form>
  );
};

export default InvoiceForm;

