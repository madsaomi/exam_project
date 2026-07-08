/* ============================================================
   API CONFIG
   Поменяй BASE_URL на адрес твоего Django-бэкенда.
   ============================================================ */
const API_BASE_URL = window.API_BASE_URL || "/api";

const ENDPOINTS = {
  register: "/auth/register/",
  login: "/auth/login/",
  refresh: "/auth/refresh/",
  categories: "/menu/categories/",
  dishes: "/menu/dishes/",
  news: "/news/",
  contact: "/contact/",
  about: "/about/",
};

/* ---------- token storage ---------- */
const Auth = {
  getAccess() { return localStorage.getItem("access_token"); },
  getRefresh() { return localStorage.getItem("refresh_token"); },
  set(access, refresh) {
    if (access) localStorage.setItem("access_token", access);
    if (refresh) localStorage.setItem("refresh_token", refresh);
  },
  clear() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  },
  isLoggedIn() { return !!this.getAccess(); },
};

/* ---------- core request helper ---------- */
async function apiRequest(path, { method = "GET", body = null, auth = false, isRetry = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth && Auth.getAccess()) {
    headers["Authorization"] = `Bearer ${Auth.getAccess()}`;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : null,
    });
  } catch (networkErr) {
    throw new Error("Не удалось соединиться с сервером. Проверь, что бэкенд запущен.");
  }

  // Handle expired access token
  if (response.status === 401 && auth && !isRetry && Auth.getRefresh()) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      return apiRequest(path, { method, body, auth, isRetry: true });
    }
  }

  let data = null;
  const text = await response.text();
  try { data = text ? JSON.parse(text) : null; } catch (e) { data = text; }

  if (!response.ok) {
    const message = (data && (data.detail || data.message)) ||
      (data && typeof data === "object" ? Object.values(data).flat().join(" ") : "Ошибка запроса");
    const err = new Error(message || `Ошибка ${response.status}`);
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}

async function refreshAccessToken() {
  try {
    const data = await apiRequest(ENDPOINTS.refresh, {
      method: "POST",
      body: { refresh: Auth.getRefresh() },
    });
    if (data && data.access) {
      Auth.set(data.access, null);
      return true;
    }
  } catch (e) { /* fall through */ }
  Auth.clear();
  return false;
}

/* ---------- helpers to normalize DRF paginated / plain list responses ---------- */
function toList(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}

/* ---------- pick the first defined field among candidates ---------- */
function pick(obj, keys, fallback = "") {
  for (const k of keys) {
    if (obj && obj[k] !== undefined && obj[k] !== null && obj[k] !== "") return obj[k];
  }
  return fallback;
}

function resolveImage(obj, fallbackSeed) {
  const raw = pick(obj, ["image", "photo", "picture", "cover", "thumbnail"], "");
  if (!raw) return `https://picsum.photos/seed/${encodeURIComponent(fallbackSeed)}/500/380`;
  if (/^https?:\/\//i.test(raw)) return raw;
  // relative media path returned by Django
  const origin = API_BASE_URL.replace(/\/api\/?$/, "");
  return `${origin}${raw.startsWith("/") ? "" : "/"}${raw}`;
}

/* ---------- API namespaces ---------- */
const MenuAPI = {
  categories: () => apiRequest(ENDPOINTS.categories).then(toList),
  dishes: (categoryId) => {
    const qs = categoryId ? `?category=${encodeURIComponent(categoryId)}` : "";
    return apiRequest(`${ENDPOINTS.dishes}${qs}`).then(toList);
  },
};

const NewsAPI = {
  list: () => apiRequest(ENDPOINTS.news).then(toList),
  detail: (id) => apiRequest(`${ENDPOINTS.news}${id}/`),
};

const AboutAPI = {
  get: () => apiRequest(ENDPOINTS.about),
};

const ContactAPI = {
  send: (payload) => apiRequest(ENDPOINTS.contact, { method: "POST", body: payload }),
};

const AuthAPI = {
  register: (payload) => apiRequest(ENDPOINTS.register, { method: "POST", body: payload }),
  login: (payload) => apiRequest(ENDPOINTS.login, { method: "POST", body: payload }),
};
