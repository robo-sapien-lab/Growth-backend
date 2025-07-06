# app/routes/user.py

import os
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_current_user

# Only one router, no prefix here
router = APIRouter(tags=["User"])

# Ensure upload directory exists
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/me")
def read_user_profile(current_user: User = Depends(get_current_user)):
    """
    GET /user/me → return current user's profile
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "grade": current_user.grade,
        "xp": current_user.xp,
        "avatar_url": current_user.avatar_url,
        "school_id": current_user.school_id,
        "school_name": current_user.school.name if current_user.school else None,
    }


@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    POST /user/upload-avatar → upload avatar for current user
    """
    try:
        ext = file.filename.split(".")[-1]
        filename = f"{uuid4()}.{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        with open(filepath, "wb") as buffer:
            buffer.write(await file.read())

        current_user.avatar_url = f"/static/avatars/{filename}"
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return {"message": "Avatar uploaded", "avatar_url": current_user.avatar_url}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
