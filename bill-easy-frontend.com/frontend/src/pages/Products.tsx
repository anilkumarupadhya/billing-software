// src/pages/Products.tsx
import React, { useState } from "react";

interface Product {
  id: number;
  name: string;
  sku: string;
  category: string;
  price: number;
  tax: number;
  stock: number;
}

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [form, setForm] = useState<Omit<Product, "id">>({
    name: "",
    sku: "",
    category: "",
    price: 0,
    tax: 0,
    stock: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm({
      ...form,
      [name]: name === "price" || name === "tax" || name === "stock" ? Number(value) : value,
    });
  };

  const addProduct = () => {
    if (!form.name || !form.sku) return;
    setProducts([...products, { ...form, id: Date.now() }]);
    setForm({ name: "", sku: "", category: "", price: 0, tax: 0, stock: 0 });
  };

  const deleteProduct = (id: number) => {
    setProducts(products.filter((p) => p.id !== id));
  };

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-2xl font-bold text-gray-800">Products</h1>

      {/* Product Form */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Add New Product</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Product Name"
            className="border rounded p-2"
          />
          <input
            type="text"
            name="sku"
            value={form.sku}
            onChange={handleChange}
            placeholder="SKU"
            className="border rounded p-2"
          />
          <input
            type="text"
            name="category"
            value={form.category}
            onChange={handleChange}
            placeholder="Category"
            className="border rounded p-2"
          />
          <input
            type="number"
            name="price"
            value={form.price}
            onChange={handleChange}
            placeholder="Price"
            className="border rounded p-2"
          />
          <input
            type="number"
            name="tax"
            value={form.tax}
            onChange={handleChange}
            placeholder="Tax %"
            className="border rounded p-2"
          />
          <input
            type="number"
            name="stock"
            value={form.stock}
            onChange={handleChange}
            placeholder="Stock Qty"
            className="border rounded p-2"
          />
        </div>
        <button
          onClick={addProduct}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + Add Product
        </button>
      </div>

      {/* Product Table */}
      <div className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-lg font-semibold mb-4">Product List</h2>
        {products.length === 0 ? (
          <p className="text-gray-500">No products added yet.</p>
        ) : (
          <table className="w-full border-collapse border">
            <thead>
              <tr className="bg-gray-100">
                <th className="border p-2 text-left">Name</th>
                <th className="border p-2">SKU</th>
                <th className="border p-2">Category</th>
                <th className="border p-2">Price</th>
                <th className="border p-2">Tax %</th>
                <th className="border p-2">Stock</th>
                <th className="border p-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
                <tr key={p.id} className="text-center">
                  <td className="border p-2 text-left">{p.name}</td>
                  <td className="border p-2">{p.sku}</td>
                  <td className="border p-2">{p.category}</td>
                  <td className="border p-2">₹{p.price}</td>
                  <td className="border p-2">{p.tax}%</td>
                  <td className="border p-2">{p.stock}</td>
                  <td className="border p-2">
                    <button
                      onClick={() => deleteProduct(p.id)}
                      className="text-red-600 hover:underline"
                    >
                      ✕ Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default Products;

