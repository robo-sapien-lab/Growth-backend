from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.feed import FeedPost, FeedComment
from app.models.story import Story

router = APIRouter()


@router.get("/{school_id}")
def get_full_leaderboard(school_id: int, db: Session = Depends(get_db)):
    try:
        users = db.query(User).filter(User.school_id == school_id).all()
        if not users:
            raise HTTPException(status_code=404, detail="No users found for this school")

        contributors = []
        streaks = []
        improvements = []

        now = datetime.utcnow()
        start_of_this_week = now - timedelta(days=now.weekday())  # Monday this week
        start_of_last_week = start_of_this_week - timedelta(days=7)
        end_of_last_week = start_of_this_week

        for user in users:
            # 🟡 Total contributions
            feed_post_count = db.query(FeedPost).filter_by(user_id=user.id).count()
            story_count = db.query(Story).filter_by(user_id=user.id).count()
            comment_count = db.query(FeedComment).filter_by(user_id=user.id).count()
            total_contribution = feed_post_count + story_count + comment_count

            contributors.append({
                "user_id": user.id,
                "name": user.name,
                "score": total_contribution,
                "avatar_url": user.avatar_url
            })

            # 🔵 Streak
            streaks.append({
                "user_id": user.id,
                "name": user.name,
                "streak": user.streak or 0,
                "avatar_url": user.avatar_url
            })

            # 🧠 Most Improved
            current_total = db.query(FeedPost).filter(
                FeedPost.user_id == user.id,
                FeedPost.created_at >= start_of_this_week
            ).count() + db.query(FeedComment).filter(
                FeedComment.user_id == user.id,
                FeedComment.created_at >= start_of_this_week
            ).count() + db.query(Story).filter(
                Story.user_id == user.id,
                Story.created_at >= start_of_this_week
            ).count()

            last_total = db.query(FeedPost).filter(
                FeedPost.user_id == user.id,
                FeedPost.created_at >= start_of_last_week,
                FeedPost.created_at < end_of_last_week
            ).count() + db.query(FeedComment).filter(
                FeedComment.user_id == user.id,
                FeedComment.created_at >= start_of_last_week,
                FeedComment.created_at < end_of_last_week
            ).count() + db.query(Story).filter(
                Story.user_id == user.id,
                Story.created_at >= start_of_last_week,
                Story.created_at < end_of_last_week
            ).count()

            improvement = current_total - last_total
            if improvement > 0:
                improvements.append({
                    "user_id": user.id,
                    "name": user.name,
                    "avatar_url": user.avatar_url,
                    "last_week": last_total,
                    "this_week": current_total,
                    "improvement": improvement
                })

        top_contributors = sorted(contributors, key=lambda x: x["score"], reverse=True)[:5]
        top_streaks = sorted(streaks, key=lambda x: x["streak"], reverse=True)[:5]
        most_improved = sorted(improvements, key=lambda x: x["improvement"], reverse=True)[0] if improvements else None

        return {
            "top_contributors": top_contributors,
            "top_streaks": top_streaks,
            "most_improved": most_improved
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
