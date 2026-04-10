from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    website = Column(String(500), nullable=True)
    username = Column(String(255), nullable=True)
    # Stored encrypted
    password_encrypted = Column(Text, nullable=False)
    category = Column(String(100), default="General")
    # Stored encrypted
    notes_encrypted = Column(Text, nullable=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="vault_items")
