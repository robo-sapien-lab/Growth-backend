import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import Base, engine

from app.models.user import User, School
from app.models.doubt import Doubt
from app.models.story import Story
from app.models.story import Story, StoryView

print("Creating all tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
