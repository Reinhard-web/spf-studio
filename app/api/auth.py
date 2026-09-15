from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.current_user import CurrentUser
from app.auth.service import authenticate_user
from app.db.session import get_db
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


DbSession = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: DbSession,
):
    token = authenticate_user(
        db,
        request.email,
        request.password,
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return LoginResponse(access_token=token)


@router.post("/token", response_model=LoginResponse)
def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbSession,
):
    access_token = authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    return LoginResponse(access_token=access_token)


@router.get("/me")
def get_me(current_user: CurrentUser):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }