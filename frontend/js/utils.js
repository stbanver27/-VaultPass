/**
 * VaultPass Utilities
 */

// ─── Password Generator ────────────────────────────────────────────────────

export function generatePassword(opts = {}) {
  const {
    length = 16,
    uppercase = true,
    lowercase = true,
    numbers = true,
    symbols = true,
  } = opts;

  const sets = [];
  if (uppercase) sets.push('ABCDEFGHIJKLMNOPQRSTUVWXYZ');
  if (lowercase) sets.push('abcdefghijklmnopqrstuvwxyz');
  if (numbers)   sets.push('0123456789');
  if (symbols)   sets.push('!@#$%^&*()_+-=[]{}|;:,.<>?');

  if (!sets.length) return '';

  const pool = sets.join('');
  const arr = new Uint8Array(length);
  crypto.getRandomValues(arr);

  // Ensure at least one char from each set
  let result = sets.map(s => {
    const i = new Uint8Array(1);
    crypto.getRandomValues(i);
    return s[i[0] % s.length];
  });

  for (let i = result.length; i < length; i++) {
    result.push(pool[arr[i] % pool.length]);
  }

  // Shuffle
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }

  return result.join('');
}

// ─── Password Strength ─────────────────────────────────────────────────────

export function passwordStrength(password) {
  if (!password) return { score: 0, label: '', color: '' };

  let score = 0;
  if (password.length >= 8)  score++;
  if (password.length >= 12) score++;
  if (password.length >= 16) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  const levels = [
    { min: 0, label: 'Muy débil',  color: '#ef4444' },
    { min: 2, label: 'Débil',      color: '#f97316' },
    { min: 4, label: 'Regular',    color: '#eab308' },
    { min: 5, label: 'Fuerte',     color: '#22c55e' },
    { min: 7, label: 'Muy fuerte', color: '#10b981' },
  ];

  const level = [...levels].reverse().find(l => score >= l.min);
  return { score, label: level.label, color: level.color, percent: Math.min(100, (score / 7) * 100) };
}

// ─── Clipboard ─────────────────────────────────────────────────────────────

export async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback
    const el = document.createElement('textarea');
    el.value = text;
    el.style.position = 'fixed';
    el.style.opacity = '0';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    return true;
  }
}

// ─── Toast notifications ───────────────────────────────────────────────────

export function toast(message, type = 'success', duration = 3000) {
  const container = document.getElementById('toast-container') || createToastContainer();
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;

  const icons = { success: '✓', error: '✕', info: 'ℹ', warning: '⚠' };
  el.innerHTML = `<span class="toast-icon">${icons[type] || '•'}</span><span>${message}</span>`;

  container.appendChild(el);
  requestAnimationFrame(() => el.classList.add('toast-show'));

  setTimeout(() => {
    el.classList.remove('toast-show');
    el.classList.add('toast-hide');
    setTimeout(() => el.remove(), 300);
  }, duration);
}

function createToastContainer() {
  const c = document.createElement('div');
  c.id = 'toast-container';
  document.body.appendChild(c);
  return c;
}

// ─── DOM helpers ───────────────────────────────────────────────────────────

export function qs(sel, ctx = document) { return ctx.querySelector(sel); }
export function qsa(sel, ctx = document) { return [...ctx.querySelectorAll(sel)]; }

export function formatDate(iso) {
  if (!iso) return '-';
  return new Date(iso).toLocaleDateString('es-CL', {
    day: '2-digit', month: 'short', year: 'numeric'
  });
}

export function getFavicon(website) {
  if (!website) return null;
  try {
    const url = new URL(website.startsWith('http') ? website : `https://${website}`);
    return `https://www.google.com/s2/favicons?sz=32&domain=${url.hostname}`;
  } catch { return null; }
}

export const CATEGORIES = [
  'General', 'Redes Sociales', 'Trabajo', 'Finanzas',
  'Entretenimiento', 'Correo', 'Compras', 'Educación', 'Otros'
];
