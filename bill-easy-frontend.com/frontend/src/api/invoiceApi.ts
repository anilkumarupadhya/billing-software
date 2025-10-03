// frontend/src/api/invoiceApi.ts
import axios from "axios";
import { InvoiceCreate, InvoiceUpdate, InvoiceOut } from "../types/invoice";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1/invoices";

export const getInvoices = async () => {
  const res = await axios.get(API_URL);
  return res.data as InvoiceOut[];
};

export const getInvoice = async (id: number) => {
  const res = await axios.get(`${API_URL}/${id}`);
  return res.data as InvoiceOut;
};

export const createInvoice = async (payload: InvoiceCreate) => {
  const res = await axios.post(API_URL, payload);
  return res.data as InvoiceOut;
};

export const updateInvoice = async (id: number, payload: InvoiceUpdate) => {
  const res = await axios.put(`${API_URL}/${id}`, payload);
  return res.data as InvoiceOut;
};

export const deleteInvoice = async (id: number) => {
  await axios.delete(`${API_URL}/${id}`);
};
