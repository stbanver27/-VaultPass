"""
Módulo de cifrado simétrico con Fernet (AES-128-CBC + HMAC-SHA256).
Las contraseñas guardadas NUNCA se almacenan en texto plano.
"""
from cryptography.fernet import Fernet, InvalidToken
from app.core.config import FERNET_KEY

_fernet: Fernet = Fernet(FERNET_KEY)


def encrypt(plaintext: str) -> str:
    """Cifra texto plano → ciphertext base64."""
    if not plaintext:
        return ""
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    """Descifra ciphertext base64 → texto plano."""
    if not ciphertext:
        return ""
    try:
        return _fernet.decrypt(ciphertext.encode()).decode()
    except InvalidToken:
        raise ValueError("No se pudo descifrar. Clave incorrecta o dato corrupto.")
