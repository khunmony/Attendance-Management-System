// Shared helper for calling the FastAPI backend.
export const API_URL = "http://localhost:8000/api/v1";

export function getToken() {
  return sessionStorage.getItem("token");
}

export async function apiFetch(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body && !(options.body instanceof URLSearchParams)) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export async function login(email, password) {
  const body = new URLSearchParams({ username: email, password });
  const data = await apiFetch("/auth/login", { method: "POST", body });
  sessionStorage.setItem("token", data.access_token);
  return data;
}
