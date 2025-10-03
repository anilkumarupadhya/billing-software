// frontend/src/api/customerApi.ts
import axios from "axios";
import { CustomerCreate, CustomerUpdate, CustomerOut } from "../types/customer";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1/customers";

export const getCustomers = async (page = 1, pageSize = 25, q?: string) => {
  const params: Record<string, any> = { page, page_size: pageSize };
  if (q) params.q = q;
  const res = await axios.get(API_URL, { params });
  return res.data as { total: number; items: CustomerOut[] };
};

export const getCustomer = async (id: number) => {
  const res = await axios.get(`${API_URL}/${id}`);
  return res.data as CustomerOut;
};

export const createCustomer = async (payload: CustomerCreate) => {
  const res = await axios.post(API_URL, payload);
  return res.data as CustomerOut;
};

export const updateCustomer = async (id: number, payload: CustomerUpdate) => {
  const res = await axios.put(`${API_URL}/${id}`, payload);
  return res.data as CustomerOut;
};

export const deleteCustomer = async (id: number) => {
  await axios.delete(`${API_URL}/${id}`);
};
