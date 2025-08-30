import React, { useEffect, useState } from "react";
import axios from "axios";
import ProductForm from "../components/ProductForm";

interface Product {
  id: number;
  name: string;
  price: number;
}

const Products: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    axios.get("/api/v1/products").then((res) => setProducts(res.data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Products</h1>
      <ProductForm />
      <ul className="mt-6 space-y-2">
        {products.map((p) => (
          <li key={p.id} className="border p-2 rounded">
            <p className="font-semibold">{p.name}</p>
            <p>₹{p.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Products;
