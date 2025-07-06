from fastapi import APIRouter, Request, UploadFile, File, Form, Depends, HTTPException, Body, Path
from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
import os

from app.database import get_db
from app.models.user import User
from app.models.feed import FeedPost, FeedReaction, FeedComment

router = APIRouter()

# Ensure upload directory exists
UPLOAD_DIR = "uploads/feed"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image")
async def upload_feed_post(
    request: Request,
    user_id: int = Form(...),
    caption: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        ext = image.filename.split('.')[-1]
        filename = f"{datetime.utcnow().timestamp()}_{uuid4()}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            f.write(await image.read())

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        post = FeedPost(
            user_id=user_id,
            caption=caption,
            image_url=f"/static/feed/{filename}",
            school_id=user.school_id,
            created_at=datetime.utcnow()
        )
        db.add(post)
        db.commit()
        db.refresh(post)

        return {"message": "Post created", "post_id": post.id, "image_url": post.image_url}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/school/{school_id}")
def get_school_feed(
    school_id: int = Path(...),
    db: Session = Depends(get_db)
):
    posts = (
        db.query(FeedPost)
        .filter(FeedPost.school_id == school_id)
        .order_by(FeedPost.created_at.desc())
        .all()
    )
    return {
        "school_id": school_id,
        "feed": [
            {
                "post_id": p.id,
                "user_id": p.user_id,
                "caption": p.caption,
                "image_url": p.image_url,
                "created_at": p.created_at
            } for p in posts
        ]
    }

@router.get("/all")
def get_all_feed(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    posts = (
        db.query(FeedPost)
        .filter(FeedPost.school_id == user.school_id)
        .order_by(FeedPost.created_at.desc())
        .all()
    )
    return {
        "posts": [
            {
                "post_id": p.id,
                "user_id": p.user_id,
                "caption": p.caption,
                "image_url": p.image_url,
                "created_at": p.created_at,
            }
            for p in posts
        ]
    }

@router.post("/react")
def react_to_post(
    post_id: int = Body(...),
    user_id: int = Body(...),
    emoji: str = Body(...),
    db: Session = Depends(get_db)
):
    try:
        existing = db.query(FeedReaction).filter_by(
            post_id=post_id, user_id=user_id
        ).first()
        if existing:
            existing.emoji = emoji
            existing.reacted_at = datetime.utcnow()
        else:
            db.add(FeedReaction(post_id=post_id, user_id=user_id, emoji=emoji))
        db.commit()
        return {"message": "Reaction recorded"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/comment")
def comment_on_post(
    post_id: int = Body(...),
    user_id: int = Body(...),
    comment: str = Body(...),
    db: Session = Depends(get_db)
):
    try:
        db.add(FeedComment(post_id=post_id, user_id=user_id, comment=comment))
        db.commit()
        return {"message": "Comment added"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
