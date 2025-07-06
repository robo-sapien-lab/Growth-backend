from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from uuid import uuid4
from app.database import get_db
from app.models.user import User

router = APIRouter()
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/user/avatar")
async def upload_avatar(user_id: int = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    file_ext = image.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(await image.read())

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.avatar_url = f"/static/avatars/{filename}"
    db.commit()

    return {"message": "Avatar uploaded", "avatar_url": user.avatar_url}
