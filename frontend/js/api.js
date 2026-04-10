/**
 * VaultPass API Client
 * Funciona tanto sirviendo el frontend desde FastAPI como abriendo los HTML con Live Server.
 */

const IS_BACKEND_ORIGIN = ['127.0.0.1:8000', 'localhost:8000'].includes(window.location.host);
const BASE_URL = IS_BACKEND_ORIGIN ? window.location.origin : 'http://127.0.0.1:8000';
const FRONTEND_MODE = window.location.protocol === 'file:' || !IS_BACKEND_ORIGIN;

export const APP_ROUTES = {
  login: FRONTEND_MODE ? './login.html' : '/',
  dashboard: FRONTEND_MODE ? './dashboard.html' : '/dashboard',
  vault: FRONTEND_MODE ? './vault.html' : '/vault',
};

function redirectTo(path) {
  window.location.href = path;
}

function getToken() {
  return localStorage.getItem('vp_token');
}

function authHeaders(includeJson = true) {
  const token = getToken();
  return {
    ...(includeJson ? { 'Content-Type': 'application/json' } : {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function request(method, path, body = null) {
  const opts = { method, headers: authHeaders(body !== null) };
  if (body !== null) opts.body = JSON.stringify(body);

  const res = await fetch(`${BASE_URL}${path}`, opts);
  const data = await res.json().catch(() => ({}));

  if (res.status === 401) {
    const isLoginRequest = path === '/api/auth/login';
    if (!isLoginRequest) {
      clearSession();
      redirectTo(APP_ROUTES.login);
    }
  }

  if (!res.ok) {
    const msg = data.detail || `Error ${res.status}`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data;
}

function saveSession(data) {
  localStorage.setItem('vp_token', data.access_token);
  localStorage.setItem('vp_user', JSON.stringify({ name: data.user_name, email: data.user_email }));
  localStorage.setItem('vp_expires', String(Date.now() + data.expires_in * 1000));
}

function clearSession() {
  localStorage.removeItem('vp_token');
  localStorage.removeItem('vp_user');
  localStorage.removeItem('vp_expires');
}

export async function apiLogin(email, password) {
  const data = await request('POST', '/api/auth/login', { email, password });
  saveSession(data);
  return data;
}

export function logout() {
  clearSession();
  redirectTo(APP_ROUTES.login);
}

export function requireAuth() {
  const token = getToken();
  const expires = localStorage.getItem('vp_expires');
  if (!token || (expires && Date.now() > Number(expires))) {
    clearSession();
    redirectTo(APP_ROUTES.login);
    return false;
  }
  return true;
}

export function getCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem('vp_user')) || {};
  } catch {
    return {};
  }
}

export async function apiGetDashboard() {
  return request('GET', '/api/vault/dashboard');
}

export async function apiListItems(params = {}) {
  const q = new URLSearchParams();
  if (params.search) q.set('search', params.search);
  if (params.category) q.set('category', params.category);
  if (params.favorites) q.set('favorites', 'true');
  return request('GET', `/api/vault/items?${q.toString()}`);
}

export async function apiGetItem(id) {
  return request('GET', `/api/vault/items/${id}`);
}

export async function apiCreateItem(data) {
  return request('POST', '/api/vault/items', data);
}

export async function apiUpdateItem(id, data) {
  return request('PUT', `/api/vault/items/${id}`, data);
}

export async function apiDeleteItem(id) {
  return request('DELETE', `/api/vault/items/${id}`);
}

export async function apiExport() {
  const token = getToken();
  const res = await fetch(`${BASE_URL}/api/vault/export`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Error al exportar');
  return res.json();
}
