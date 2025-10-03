// frontend/src/api/userApi.ts
import axios from "axios";
import { UserCreate, UserUpdate, UserOut } from "../types/user";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1/users";

export const login = async (email: string, password: string) => {
  const res = await axios.post(`${API_URL}/login`, { email, password });
  return res.data as { access_token: string; token_type: string };
};

export const getUsers = async () => {
  const res = await axios.get(API_URL);
  return res.data as UserOut[];
};

export const createUser = async (payload: UserCreate) => {
  const res = await axios.post(API_URL, payload);
  return res.data as UserOut;
};

export const updateUser = async (id: number, payload: UserUpdate) => {
  const res = await axios.put(`${API_URL}/${id}`, payload);
  return res.data as UserOut;
};

export const deleteUser = async (id: number) => {
  await axios.delete(`${API_URL}/${id}`);
};
