from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)

    students = relationship("User", back_populates="school")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"))
    xp = Column(Integer, default=0)
    stories = relationship("Story", back_populates="user", cascade="all, delete-orphan")
    streak = Column(Integer, default=0)
    avatar_url = Column(String, nullable=True)

    # ✅ Streak fields
    streak_count = Column(Integer, default=0)
    last_active_date = Column(Date, default=date.today)

    school = relationship("School", back_populates="students")
    doubts = relationship("Doubt", back_populates="user")
