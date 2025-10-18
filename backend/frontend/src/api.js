const API_BASE = import.meta.env.VITE_API_BASE || "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let payload = null;
  try {
    const text = await response.clone().text();
    if (text) {
      payload = JSON.parse(text);
    }
  } catch (_) {
    payload = null;
  }

  if (!response.ok && response.status !== 204) {
    const message =
      payload?.detail ??
      response.statusText ??
      "Не удалось выполнить запрос к серверу";
    throw new Error(
      Array.isArray(message)
        ? message.map((item) => item.msg || item.detail).join(", ")
        : message,
    );
  }

  return { status: response.status, data: payload };
}

export async function registerAccount(body) {
  return request("/register", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function login(body) {
  return request("/auth", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function chooseRole(body) {
  return request("/authentication", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function storeToken(tokenResponse) {
  sessionStorage.setItem("auth_token", tokenResponse.access_token);
  sessionStorage.setItem("auth_role", String(tokenResponse.role));
}

export function clearToken() {
  sessionStorage.removeItem("auth_token");
  sessionStorage.removeItem("auth_role");
}

export const ROLE_OPTIONS = [
  { code: 2, label: "HR" },
  { code: 3, label: "Университет" },
  { code: 4, label: "Студент" },
];

export function roleLabel(code) {
  return ROLE_OPTIONS.find((item) => item.code === code)?.label || `Роль ${code}`;
}


