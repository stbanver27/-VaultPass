"""
VaultPass — Configuración sin .env
La clave Fernet se genera automáticamente la primera vez
y se persiste en 'vaultpass.key' para que las contraseñas
cifradas sigan siendo legibles entre reinicios.
"""
from pathlib import Path
from cryptography.fernet import Fernet

# ─── Rutas base ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent   # raíz del proyecto
KEY_FILE  = BASE_DIR / "vaultpass.key"

# ─── JWT ─────────────────────────────────────────────────────────────────────
SECRET_KEY = "vaultpass-jwt-secret-hardcoded-xZ9!qR2#mK8@pL5"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ─── Base de datos ───────────────────────────────────────────────────────────
DATABASE_URL = f"sqlite:///{BASE_DIR / 'vaultpass.db'}"

# ─── Clave Fernet ─────────────────────────────────────────────────────────────
def _load_or_create_fernet_key() -> bytes:
    """
    Lee la clave de vaultpass.key.
    Si no existe, genera una nueva y la guarda.
    ⚠ Nunca borres vaultpass.key: perderías las contraseñas cifradas.
    """
    if KEY_FILE.exists():
        key = KEY_FILE.read_bytes().strip()
        try:
            Fernet(key)
            return key
        except Exception:
            pass  # Corrupta → genera nueva

    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    try:
        KEY_FILE.chmod(0o600)   # Solo lectura para el dueño (Unix/Mac)
    except Exception:
        pass
    print(f"[VaultPass] Clave de cifrado generada → {KEY_FILE}")
    return key


FERNET_KEY: bytes = _load_or_create_fernet_key()
