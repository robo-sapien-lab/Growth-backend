# app/utils/streaks.py

from datetime import date, timedelta

def update_streak(user, today: date):
    if user.last_active_date == today:
        return  # Already updated today

    yesterday = today - timedelta(days=1)

    if user.last_active_date == yesterday:
        user.streak_count += 1  # Continued streak
    else:
        user.streak_count = 1  # Reset streak

    user.last_active_date = today
