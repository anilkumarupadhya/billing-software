// frontend/src/api/paymentApi.ts
import axios from "axios";
import { PaymentCreate, PaymentUpdate, PaymentOut } from "../types/payment";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1/payments";

export const getPayments = async () => {
  const res = await axios.get(API_URL);
  return res.data as PaymentOut[];
};

export const getPayment = async (id: number) => {
  const res = await axios.get(`${API_URL}/${id}`);
  return res.data as PaymentOut;
};

export const createPayment = async (payload: PaymentCreate) => {
  const res = await axios.post(API_URL, payload);
  return res.data as PaymentOut;
};

export const updatePayment = async (id: number, payload: PaymentUpdate) => {
  const res = await axios.put(`${API_URL}/${id}`, payload);
  return res.data as PaymentOut;
};

export const deletePayment = async (id: number) => {
  await axios.delete(`${API_URL}/${id}`);
};
