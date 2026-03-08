import type { User } from "@/types";
import { apiFetch } from "./client";

export async function login(email: string, password: string) {
  const data = await apiFetch<{ access_token: string; refresh_token: string }>(
    "/api/v1/auth/login",
    {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }
  );
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);
  return data;
}

export async function logout() {
  const refresh_token = localStorage.getItem("refresh_token");
  if (refresh_token) {
    await apiFetch("/api/v1/auth/logout", {
      method: "POST",
      body: JSON.stringify({ refresh_token }),
    }).catch(() => {});
  }
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}

export async function getMe(): Promise<User> {
  return apiFetch<User>("/api/v1/auth/me");
}
