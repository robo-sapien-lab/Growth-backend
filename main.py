from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import Base, engine
from app import models
from app.routes import auth, doubt, user, school, story, feed, chat, leaderboard

# Create upload directories
os.makedirs("uploads/feed", exist_ok=True)
os.makedirs("uploads/avatars", exist_ok=True)

app = FastAPI()

# CORS setup (dev only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],  # Change to ["http://localhost:8081"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directories
app.mount("/static/feed", StaticFiles(directory="uploads/feed"), name="feed_images")
app.mount("/static/avatars", StaticFiles(directory="uploads/avatars"), name="avatar_images")

# Include routers under their proper prefixes
app.include_router(auth.router, prefix="/auth")
app.include_router(doubt.router, prefix="/doubt")
app.include_router(user.router, prefix="/user")
app.include_router(school.router, prefix="/school")
app.include_router(story.router, prefix="/story")
app.include_router(feed.router)         # ✅ feed mounted here
app.include_router(chat.router, prefix="/chat")
app.include_router(leaderboard.router, prefix="/leaderboard")

@app.get("/")
def read_root():
    return {"message": "Growth backend is running!"}

# Create all tables at startup
Base.metadata.create_all(bind=engine)

# Custom OpenAPI with JWT security
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="Growth Study Assistant API",
        version="1.0.0",
        description="Backend for Growth EdTech",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in schema["paths"].values():
        for method in path.values():
            method["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
