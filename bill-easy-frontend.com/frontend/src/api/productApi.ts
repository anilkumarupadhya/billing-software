// frontend/src/api/productApi.ts
import axios from "axios";
import { ProductCreate, ProductUpdate, ProductOut } from "../types/product";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1/products";

export const getProducts = async () => {
  const res = await axios.get(API_URL);
  return res.data as ProductOut[];
};

export const getProduct = async (id: number) => {
  const res = await axios.get(`${API_URL}/${id}`);
  return res.data as ProductOut;
};

export const createProduct = async (payload: ProductCreate) => {
  const res = await axios.post(API_URL, payload);
  return res.data as ProductOut;
};

export const updateProduct = async (id: number, payload: ProductUpdate) => {
  const res = await axios.put(`${API_URL}/${id}`, payload);
  return res.data as ProductOut;
};

export const deleteProduct = async (id: number) => {
  await axios.delete(`${API_URL}/${id}`);
};
