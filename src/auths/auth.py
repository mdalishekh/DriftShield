from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auths.password import verify_password
from src.auths.jwt_auth import create_access_token
from src.auths.schemas import LoginRequest, TokenResponse
from src.database.connection import get_db
from src.database.db_models import User


# Router for Login
router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(
        (User.email == credentials.login_id) |
        (User.username == credentials.login_id)
    ).first()

    if user is None or not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }