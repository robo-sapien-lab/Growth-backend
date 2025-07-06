# app/routes/story.py

from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.story import Story, StoryView
from app.models.user import User

router = APIRouter(tags=["Story"])


# -------------------- Schemas --------------------

class StoryCreate(BaseModel):
    user_id: int
    content: str


# -------------------- Endpoints --------------------

@router.post("/post")
def post_story(story: StoryCreate, db: Session = Depends(get_db)):
    try:
        new_story = Story(
            user_id=story.user_id,
            content=story.content,
            created_at=datetime.utcnow()
        )
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
        return {"message": "Story posted", "story_id": new_story.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/active/{user_id}")
def get_active_stories(
    user_id: int,
    viewer_id: int = Query(..., description="User ID of the viewer"),
    db: Session = Depends(get_db)
):
    now = datetime.utcnow()
    cutoff_time = now - timedelta(hours=24)

    stories = db.query(Story).filter(
        Story.user_id == user_id,
        Story.created_at >= cutoff_time
    ).all()

    for story in stories:
        if user_id != viewer_id:
            already_viewed = db.query(StoryView).filter_by(
                story_id=story.id, viewer_id=viewer_id
            ).first()
            if not already_viewed:
                db.add(StoryView(
                    story_id=story.id,
                    viewer_id=viewer_id,
                    viewed_at=now
                ))
    db.commit()

    return {
        "user_id": user_id,
        "active_stories": [
            {
                "id": s.id,
                "content": s.content,
                "created_at": s.created_at.isoformat(),
                "views": db.query(StoryView).filter_by(story_id=s.id).count()
            } for s in stories
        ]
    }


@router.get("/active/all")
def get_all_active_stories(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    cutoff_time = now - timedelta(hours=24)

    stories = db.query(Story).filter(Story.created_at >= cutoff_time).all()

    results = {}
    for story in stories:
        user = db.query(User).filter_by(id=story.user_id).first()
        if not user:
            continue
        uname = user.name
        results.setdefault(uname, []).append({
            "id": story.id,
            "content": story.content,
            "created_at": story.created_at,
            "views": db.query(StoryView).filter_by(story_id=story.id).count()
        })

    return {"active_stories": results}


@router.get("/mine/{user_id}")
def my_stories(user_id: int, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    all_stories = db.query(Story).filter_by(user_id=user_id).all()

    active, expired = [], []
    for story in all_stories:
        target = active if (now - story.created_at) <= timedelta(hours=24) else expired
        target.append({
            "id": story.id,
            "content": story.content,
            "created_at": story.created_at.isoformat()
        })

    return {"user_id": user_id, "active": active, "expired": expired}


@router.post("/view")
def view_story(
    story_id: int = Body(...),
    viewer_id: int = Body(...),
    db: Session = Depends(get_db)
):
    try:
        exists = db.query(StoryView).filter_by(
            story_id=story_id,
            viewer_id=viewer_id
        ).first()

        if exists:
            return {"message": "Already viewed"}

        db.add(StoryView(
            story_id=story_id,
            viewer_id=viewer_id,
            viewed_at=datetime.utcnow()
        ))
        db.commit()
        return {"message": "View logged"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/views/{story_id}")
def get_story_views(story_id: int, db: Session = Depends(get_db)):
    views = db.query(StoryView).filter_by(story_id=story_id).all()
    usernames = [
        db.query(User).filter_by(id=view.viewer_id).first().name
        for view in views if db.query(User).filter_by(id=view.viewer_id).first()
    ]
    return {"story_id": story_id, "viewed_by": usernames}
