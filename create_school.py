# create_school.py

from app.database import SessionLocal
from app.models.user import School

db = SessionLocal()

new_school = School(
    name="DAV Public School",
    code="DAV123"
)

db.add(new_school)
db.commit()
db.close()

print("School created.")

