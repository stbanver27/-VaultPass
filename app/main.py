from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import mimetypes

# Force correct MIME types for static assets on Windows and some Python installs
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("application/json", ".json")

from app.db.database import engine, Base
from app.models import User, VaultItem
from app.routes import auth, vault

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VaultPass API",
    description="Gestor de contraseñas seguro con cifrado Fernet",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vault.router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css"), html=False), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js"), html=False), name="js")

    @app.get("/favicon.ico", include_in_schema=False)
    async def favicon():
        return {"ok": True}

    @app.get("/", include_in_schema=False)
    async def serve_login():
        return FileResponse(os.path.join(frontend_path, "pages", "login.html"))

    @app.get("/dashboard", include_in_schema=False)
    async def serve_dashboard():
        return FileResponse(os.path.join(frontend_path, "pages", "dashboard.html"))

    @app.get("/vault", include_in_schema=False)
    async def serve_vault():
        return FileResponse(os.path.join(frontend_path, "pages", "vault.html"))


@app.get("/api/health", tags=["health"])
async def health():
    return {"status": "ok", "app": "VaultPass"}
