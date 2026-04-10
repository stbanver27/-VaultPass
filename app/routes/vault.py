from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.db.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.schemas import (
    VaultItemCreate, VaultItemUpdate, VaultItemOut,
    VaultItemSummary, DashboardStats
)
from app.services import vault_service

router = APIRouter(prefix="/api/vault", tags=["vault"])


@router.get("/dashboard", response_model=DashboardStats)
async def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.get_dashboard(db, current_user)


@router.get("/items", response_model=list[VaultItemSummary])
async def list_items(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    favorites: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.list_items(db, current_user, search, category, favorites)


@router.post("/items", response_model=VaultItemOut, status_code=201)
async def create_item(
    data: VaultItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.create_item(db, current_user, data)


@router.get("/items/{item_id}", response_model=VaultItemOut)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.get_item(db, current_user, item_id)


@router.put("/items/{item_id}", response_model=VaultItemOut)
async def update_item(
    item_id: int,
    data: VaultItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.update_item(db, current_user, item_id, data)


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return vault_service.delete_item(db, current_user, item_id)


@router.get("/export")
async def export_vault(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = vault_service.export_vault(db, current_user)
    content = json.dumps({"vault": data, "exported_by": current_user.email}, indent=2, ensure_ascii=False)
    return JSONResponse(
        content=json.loads(content),
        headers={"Content-Disposition": 'attachment; filename="vaultpass_export.json"'},
    )
