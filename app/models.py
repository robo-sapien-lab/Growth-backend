from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String, unique=True, nullable=False)  # e.g., "DAV123"
    city = Column(String, nullable=True)

    students = relationship("User", back_populates="school")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    grade = Column(String, nullable=True)
    school_id = Column(Integer, ForeignKey("schools.id"))

    school = relationship("School", back_populates="students")
