// src/components/forms/InvoiceForm.tsx
import React, { useState } from "react";

interface ProductLine {
  id: number;
  product: string;
  quantity: number;
  price: number;
  tax: number; // percentage
}

const InvoiceForm: React.FC = () => {
  const [customer, setCustomer] = useState("");
  const [invoiceDate, setInvoiceDate] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("Cash");
  const [notes, setNotes] = useState("");
  const [products, setProducts] = useState<ProductLine[]>([
    { id: 1, product: "", quantity: 1, price: 0, tax: 0 },
  ]);

  // ➕ Add new product row
  const addProduct = () => {
    setProducts([
      ...products,
      { id: Date.now(), product: "", quantity: 1, price: 0, tax: 0 },
    ]);
  };

  // ❌ Remove product row
  const removeProduct = (id: number) => {
    setProducts(products.filter((p) => p.id !== id));
  };

  // 🔄 Handle product change
  const handleProductChange = (
    id: number,
    field: keyof ProductLine,
    value: string | number
  ) => {
    setProducts(
      products.map((p) =>
        p.id === id ? { ...p, [field]: value } : p
      )
    );
  };

  // 🧮 Calculate totals
  const subtotal = products.reduce(
    (acc, p) => acc + p.quantity * p.price,
    0
  );
  const totalTax = products.reduce(
    (acc, p) => acc + (p.quantity * p.price * p.tax) / 100,
    0
  );
  const grandTotal = subtotal + totalTax;

  // 💾 Submit
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const invoiceData = {
      customer,
      invoiceDate,
      dueDate,
      paymentMethod,
      notes,
      products,
      subtotal,
      totalTax,
      grandTotal,
    };
    console.log("Invoice Submitted:", invoiceData);

    // Reset form after save
    setCustomer("");
    setInvoiceDate("");
    setDueDate("");
    setPaymentMethod("Cash");
    setNotes("");
    setProducts([{ id: 1, product: "", quantity: 1, price: 0, tax: 0 }]);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-lg shadow-md space-y-6"
    >
      <h2 className="text-xl font-bold">Create / Edit Invoice</h2>

      {/* Customer */}
      <div>
        <label className="block text-gray-700 font-medium mb-1">Customer</label>
        <input
          type="text"
          value={customer}
          onChange={(e) => setCustomer(e.target.value)}
          placeholder="Select or enter customer"
          className="w-full border p-2 rounded"
          required
        />
      </div>

      {/* Dates */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 font-medium mb-1">
            Invoice Date
          </label>
          <input
            type="date"
            value={invoiceDate}
            onChange={(e) => setInvoiceDate(e.target.value)}
            className="w-full border p-2 rounded"
            required
          />
        </div>
        <div>
          <label className="block text-gray-700 font-medium mb-1">
            Due Date
          </label>
          <input
            type="date"
            value={dueDate}
            onChange={(e) => setDueDate(e.target.value)}
            className="w-full border p-2 rounded"
          />
        </div>
      </div>

      {/* Products Table */}
      <div>
        <label className="block text-gray-700 font-medium mb-2">
          Products / Services
        </label>
        <table className="w-full border">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2 border">Product</th>
              <th className="p-2 border">Qty</th>
              <th className="p-2 border">Price</th>
              <th className="p-2 border">Tax %</th>
              <th className="p-2 border">Line Total</th>
              <th className="p-2 border">Action</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                <td className="p-2 border">
                  <input
                    type="text"
                    value={p.product}
                    onChange={(e) =>
                      handleProductChange(p.id, "product", e.target.value)
                    }
                    placeholder="Product/Service"
                    className="w-full border p-1 rounded"
                    required
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={p.quantity}
                    onChange={(e) =>
                      handleProductChange(p.id, "quantity", Number(e.target.value))
                    }
                    min="1"
                    className="w-full border p-1 rounded"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={p.price}
                    onChange={(e) =>
                      handleProductChange(p.id, "price", Number(e.target.value))
                    }
                    min="0"
                    className="w-full border p-1 rounded"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={p.tax}
                    onChange={(e) =>
                      handleProductChange(p.id, "tax", Number(e.target.value))
                    }
                    min="0"
                    className="w-full border p-1 rounded"
                  />
                </td>
                <td className="p-2 border">
                  ₹{(p.quantity * p.price * (1 + p.tax / 100)).toFixed(2)}
                </td>
                <td className="p-2 border text-center">
                  <button
                    type="button"
                    onClick={() => removeProduct(p.id)}
                    className="text-red-500"
                  >
                    ✕
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <button
          type="button"
          onClick={addProduct}
          className="mt-2 bg-green-500 text-white px-3 py-1 rounded"
        >
          + Add Product
        </button>
      </div>

      {/* Totals */}
      <div className="text-right space-y-1">
        <p>Subtotal: ₹{subtotal.toFixed(2)}</p>
        <p>Tax: ₹{totalTax.toFixed(2)}</p>
        <p className="font-bold text-lg">Grand Total: ₹{grandTotal.toFixed(2)}</p>
      </div>

      {/* Payment Method */}
      <div>
        <label className="block text-gray-700 font-medium mb-1">
          Payment Method
        </label>
        <select
          value={paymentMethod}
          onChange={(e) => setPaymentMethod(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option>Cash</option>
          <option>Bank Transfer</option>
          <option>Credit</option>
          <option>UPI</option>
        </select>
      </div>

      {/* Notes */}
      <div>
        <label className="block text-gray-700 font-medium mb-1">Notes</label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="Additional notes"
          rows={3}
          className="w-full border p-2 rounded"
        ></textarea>
      </div>

      {/* Submit */}
      <div className="text-center">
        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Save Invoice
        </button>
      </div>
    </form>
  );
};

export default InvoiceForm;

