from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from typing import Optional

from app.models.vault import VaultItem
from app.models.user import User
from app.core.crypto import encrypt, decrypt
from app.schemas.schemas import (
    VaultItemCreate, VaultItemUpdate, VaultItemOut,
    VaultItemSummary, DashboardStats
)


def _decrypt_item(item: VaultItem) -> VaultItemOut:
    return VaultItemOut(
        id=item.id,
        title=item.title,
        website=item.website,
        username=item.username,
        password=decrypt(item.password_encrypted),
        category=item.category,
        notes=decrypt(item.notes_encrypted) if item.notes_encrypted else None,
        is_favorite=item.is_favorite,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


def create_item(db: Session, user: User, data: VaultItemCreate) -> VaultItemOut:
    item = VaultItem(
        owner_id=user.id,
        title=data.title,
        website=data.website,
        username=data.username,
        password_encrypted=encrypt(data.password),
        category=data.category,
        notes_encrypted=encrypt(data.notes) if data.notes else None,
        is_favorite=data.is_favorite,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _decrypt_item(item)


def list_items(
    db: Session,
    user: User,
    search: Optional[str] = None,
    category: Optional[str] = None,
    favorites_only: bool = False,
) -> list[VaultItemSummary]:
    q = db.query(VaultItem).filter(VaultItem.owner_id == user.id)
    if search:
        q = q.filter(VaultItem.title.ilike(f"%{search}%"))
    if category:
        q = q.filter(VaultItem.category == category)
    if favorites_only:
        q = q.filter(VaultItem.is_favorite == True)
    items = q.order_by(VaultItem.updated_at.desc()).all()
    return [
        VaultItemSummary(
            id=i.id, title=i.title, website=i.website, username=i.username,
            category=i.category, is_favorite=i.is_favorite,
            created_at=i.created_at, updated_at=i.updated_at,
        )
        for i in items
    ]


def get_item(db: Session, user: User, item_id: int) -> VaultItemOut:
    item = db.query(VaultItem).filter(
        VaultItem.id == item_id, VaultItem.owner_id == user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return _decrypt_item(item)


def update_item(db: Session, user: User, item_id: int, data: VaultItemUpdate) -> VaultItemOut:
    item = db.query(VaultItem).filter(
        VaultItem.id == item_id, VaultItem.owner_id == user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    if data.title is not None:
        item.title = data.title
    if data.website is not None:
        item.website = data.website
    if data.username is not None:
        item.username = data.username
    if data.password is not None:
        item.password_encrypted = encrypt(data.password)
    if data.category is not None:
        item.category = data.category
    if data.notes is not None:
        item.notes_encrypted = encrypt(data.notes)
    if data.is_favorite is not None:
        item.is_favorite = data.is_favorite

    db.commit()
    db.refresh(item)
    return _decrypt_item(item)


def delete_item(db: Session, user: User, item_id: int) -> dict:
    item = db.query(VaultItem).filter(
        VaultItem.id == item_id, VaultItem.owner_id == user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Item eliminado correctamente"}


def get_dashboard(db: Session, user: User) -> DashboardStats:
    items = db.query(VaultItem).filter(VaultItem.owner_id == user.id).all()
    total = len(items)
    favorites = sum(1 for i in items if i.is_favorite)

    cats: dict[str, int] = {}
    for i in items:
        cats[i.category] = cats.get(i.category, 0) + 1

    recent = sorted(items, key=lambda x: x.updated_at, reverse=True)[:5]
    recent_out = [
        VaultItemSummary(
            id=i.id, title=i.title, website=i.website, username=i.username,
            category=i.category, is_favorite=i.is_favorite,
            created_at=i.created_at, updated_at=i.updated_at,
        )
        for i in recent
    ]
    return DashboardStats(
        total_items=total,
        total_favorites=favorites,
        categories=cats,
        recent_items=recent_out,
    )


def export_vault(db: Session, user: User) -> list[dict]:
    items = db.query(VaultItem).filter(VaultItem.owner_id == user.id).all()
    return [
        {
            "id": i.id,
            "title": i.title,
            "website": i.website,
            "username": i.username,
            "password": decrypt(i.password_encrypted),
            "category": i.category,
            "notes": decrypt(i.notes_encrypted) if i.notes_encrypted else None,
            "is_favorite": i.is_favorite,
            "created_at": i.created_at.isoformat(),
            "updated_at": i.updated_at.isoformat(),
        }
        for i in items
    ]
