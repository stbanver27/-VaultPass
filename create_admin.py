#!/usr/bin/env python3
"""
Script para crear el usuario administrador inicial.
Ejecutar UNA SOLA VEZ antes de iniciar la app.

Uso:
    python create_admin.py
    python create_admin.py --email tu@email.com --name "Tu Nombre" --password "TuClave123!"
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import engine, Base, SessionLocal
from app.models.user import User
from app.core.security import hash_password


def create_admin(email: str, name: str, password: str):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            print(f"⚠️  Ya existe un usuario con el email: {email}")
            return

        user = User(
            email=email,
            name=name,
            hashed_password=hash_password(password),
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        print(f"\n✅ Usuario administrador creado:")
        print(f"   Email    : {email}")
        print(f"   Nombre   : {name}")
        print(f"   Password : {password}")
        print(f"\n🚀 Ahora ejecuta: uvicorn app.main:app --reload")
        print(f"   Y abre   : http://127.0.0.1:8000\n")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crear usuario admin para VaultPass")
    parser.add_argument("--email",    default="admin@vaultpass.com")
    parser.add_argument("--name",     default="Administrador")
    parser.add_argument("--password", default="Admin0000!")
    args = parser.parse_args()

    print("🔑 VaultPass — Setup inicial")
    print("=" * 40)
    create_admin(args.email, args.name, args.password)
