# models/feed.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class FeedPost(Base):
    __tablename__ = "feed_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    school_id = Column(Integer, ForeignKey("schools.id"))
    image_url = Column(String)
    caption = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class FeedReaction(Base):
    __tablename__ = "feed_reactions"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("feed_posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    emoji = Column(String)  # e.g., "🔥" or "👍"
    reacted_at = Column(DateTime, default=datetime.utcnow)


class FeedComment(Base):
    __tablename__ = "feed_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("feed_posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ fixed field name
