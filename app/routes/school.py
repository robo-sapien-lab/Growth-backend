from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import School

router = APIRouter(tags=["School"])

@router.post("/create")
def create_school(data: dict):
    db: Session = SessionLocal()

    existing = db.query(School).filter(School.code == data["code"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="School already exists.")

    school = School(name=data["name"], code=data["code"])
    db.add(school)
    db.commit()
    db.refresh(school)
    db.close()
    return {"message": "School created", "school_id": school.id}
