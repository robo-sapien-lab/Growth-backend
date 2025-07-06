from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
from passlib.hash import bcrypt
from fastapi import status
from app.models.user import User, School
from app.database import SessionLocal
from app.utils.auth import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_token,
)

router = APIRouter(tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# ----------------- Signup -----------------
class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    grade: str
    school_code: str


@router.post("/signup")
def signup(data: SignupRequest):
    db: Session = SessionLocal()
    try:
        school = db.query(School).filter(School.code == data.school_code).first()
        if not school:
            raise HTTPException(status_code=404, detail="School not found")

        existing_user = db.query(User).filter(User.email == data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = bcrypt.hash(data.password)
        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            grade=data.grade,
            school_id=school.id
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "Signup successful", "user_id": user.id}
    finally:
        db.close()


# ----------------- Login -----------------
class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()
        if not user or not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": access_token, "token_type": "bearer"}
    finally:
        db.close()


# ----------------- Token Check -----------------


@router.get("/check")
def check_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {"status": "ok", "user_id": user_id}
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

