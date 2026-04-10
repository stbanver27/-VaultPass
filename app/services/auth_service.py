from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta

from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.schemas import LoginRequest, TokenResponse


def authenticate_user(db: Session, login: LoginRequest) -> TokenResponse:
    user = db.query(User).filter(User.email == login.email).first()
    if not user or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")

    token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(
        access_token=token,
        user_name=user.name,
        user_email=user.email,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
