from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import create_access_token, get_current_admin, verify_password
from ..database import get_db
from ..models import AdminUser
from ..schemas import LoginIn, TokenOut

router = APIRouter()


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.email == payload.email.lower()).first()
    if not admin or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(401, "Identifiants incorrects.")
    return TokenOut(
        access_token=create_access_token(admin.email),
        name=admin.name,
        email=admin.email,
    )


@router.get("/me")
def me(admin: AdminUser = Depends(get_current_admin)):
    return {"email": admin.email, "name": admin.name}
