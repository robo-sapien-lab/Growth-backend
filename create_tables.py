from app.database import Base, engine
from app.models.user import User, School
from app.models.doubt import Doubt

print("Dropping old tables...")
Base.metadata.drop_all(bind=engine)

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created.")

