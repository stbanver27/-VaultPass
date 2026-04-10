# 🔐 VaultPass

Gestor de contraseñas seguro, full-stack, estilo Bitwarden.  
**Sin archivos .env — funciona out of the box.**

---

## ⚡ Inicio rápido (3 pasos)

```bash
# 1. Instalar dependencias  (requiere Python 3.11 o 3.12)
pip install -r requirements.txt

# 2. Crear usuario administrador
python create_admin.py

# 3. Iniciar servidor
uvicorn app.main:app --reload
```

Abre **http://127.0.0.1:8000** en tu navegador.

Credenciales por defecto:
```
Email    : admin@vaultpass.com
Password : Admin0000!
```

---

## 📁 Estructura

```
vaultpass/
├── app/
│   ├── core/
│   │   ├── config.py        ← Configuración sin .env
│   │   ├── security.py      ← JWT + bcrypt
│   │   └── crypto.py        ← Cifrado Fernet
│   ├── db/database.py
│   ├── models/              ← User, VaultItem
│   ├── schemas/schemas.py
│   ├── routes/              ← auth.py, vault.py
│   ├── services/            ← auth_service, vault_service
│   └── main.py
├── frontend/
│   ├── pages/               ← login.html, dashboard.html, vault.html
│   ├── css/style.css
│   └── js/                  ← api.js, utils.js
├── create_admin.py          ← Setup inicial
├── vaultpass.key            ← Clave Fernet (auto-generada, NO borrar)
├── vaultpass.db             ← Base de datos SQLite (auto-generada)
└── requirements.txt
```

---

## 🔑 Archivos generados automáticamente

| Archivo | Descripción |
|---------|-------------|
| `vaultpass.db` | Base de datos SQLite — se crea al iniciar |
| `vaultpass.key` | Clave de cifrado Fernet — se crea al iniciar |

> ⚠️ **Nunca borres `vaultpass.key`** — es necesaria para descifrar las contraseñas guardadas.  
> Haz un backup de este archivo junto con `vaultpass.db`.

---

## 🔐 Seguridad

| Aspecto | Implementación |
|---------|----------------|
| Contraseñas de usuarios | bcrypt (passlib) |
| Contraseñas del vault | Fernet — AES-128-CBC + HMAC-SHA256 |
| Autenticación | JWT (python-jose) con expiración |
| Acceso a datos | Cada usuario solo ve sus propios ítems |
| Sin texto plano | Nada se guarda sin cifrar |

---

## 📡 API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login` | Login — obtener JWT |
| GET | `/api/auth/me` | Info del usuario actual |
| GET | `/api/vault/dashboard` | Estadísticas |
| GET | `/api/vault/items` | Listar (search, category, favorites) |
| POST | `/api/vault/items` | Crear ítem |
| GET | `/api/vault/items/{id}` | Detalle con contraseña descifrada |
| PUT | `/api/vault/items/{id}` | Editar |
| DELETE | `/api/vault/items/{id}` | Eliminar |
| GET | `/api/vault/export` | Exportar vault a JSON |

Documentación interactiva: **http://127.0.0.1:8000/docs**

---

## ✨ Funcionalidades

- ✅ Login seguro con JWT + bcrypt
- ✅ CRUD completo de contraseñas
- ✅ Cifrado Fernet (AES) en base de datos
- ✅ Generador de contraseñas configurable
- ✅ Indicador de fortaleza de contraseña
- ✅ Búsqueda por título y filtro por categoría
- ✅ Favoritos
- ✅ Copiar contraseña al portapapeles
- ✅ Mostrar / ocultar contraseña
- ✅ Dashboard con estadísticas y gráficos
- ✅ Exportación a JSON
- ✅ Notas cifradas por ítem
- ✅ Diseño responsive dark mode
- ✅ Expiración de sesión automática

---

## 🛠 Stack

**Backend:** FastAPI · SQLAlchemy · SQLite · python-jose · passlib · cryptography  
**Frontend:** HTML5 · CSS3 · JavaScript ES6+ (Vanilla, sin frameworks)

---

## ⚙️ Personalizar admin

```bash
python create_admin.py --email tu@email.com --name "Tu Nombre" --password "TuClave123!"
```

---

## 🐍 Versión de Python recomendada

**Python 3.11** o **Python 3.12**  
(Python 3.13 puede tener problemas compilando dependencias en Windows)


