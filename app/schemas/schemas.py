from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# ─── Auth ────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_name: str
    user_email: str
    expires_in: int


# ─── User ────────────────────────────────────────────────────────────────────

class UserOut(BaseModel):
    id: int
    email: str
    name: str
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Vault ───────────────────────────────────────────────────────────────────

class VaultItemCreate(BaseModel):
    title: str
    website: Optional[str] = None
    username: Optional[str] = None
    password: str
    category: str = "General"
    notes: Optional[str] = None
    is_favorite: bool = False

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("El título no puede estar vacío")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v):
        if not v:
            raise ValueError("La contraseña no puede estar vacía")
        return v


class VaultItemUpdate(BaseModel):
    title: Optional[str] = None
    website: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None


class VaultItemOut(BaseModel):
    id: int
    title: str
    website: Optional[str]
    username: Optional[str]
    password: str          # decrypted — sent over HTTPS only
    category: str
    notes: Optional[str]
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VaultItemSummary(BaseModel):
    id: int
    title: str
    website: Optional[str]
    username: Optional[str]
    category: str
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ─── Dashboard ───────────────────────────────────────────────────────────────

class DashboardStats(BaseModel):
    total_items: int
    total_favorites: int
    categories: dict[str, int]
    recent_items: list[VaultItemSummary]
