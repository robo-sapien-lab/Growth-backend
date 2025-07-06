# src/routes/doubt.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import os
import httpx
from dotenv import load_dotenv
from datetime import date
from sqlalchemy.orm import Session

from app.utils.streaks import update_streak
from app.utils.auth import get_current_user
from app.models.doubt import Doubt
from app.models.user import User
from app.database import get_db

load_dotenv()

router = APIRouter()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment")

# --- 📌 Input model ---
class DoubtRequest(BaseModel):
    question: str
    subject: str

# --- 🤖 Ask AI Doubt ---
@router.post("/ask")
async def solve_doubt(
    data: DoubtRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 1. Prepare the payload once
    payload = {
        "model": "llama-3-3-70b-instruct",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful tutor for students in grade 6–12. "
                    f"Explain concepts clearly for {data.subject}."
                ),
            },
            {"role": "user", "content": data.question},
        ],
        "temperature": 0.7,
        "max_tokens": 512,
    }

    try:
        # 2. Single Async HTTP call
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            resp.raise_for_status()
            result = resp.json()  # sync parse on the one response

        answer = result["choices"][0]["message"]["content"].strip()

        # 3. Save the Doubt and update user XP/streak
        new_doubt = Doubt(
            user_id=user.id,
            question=data.question,
            subject=data.subject,
            answer=answer,
            xp_awarded=10,
        )
        db.add(new_doubt)

        user.xp += 10
        update_streak(user, date.today())

        db.commit()

        return {
            "question": data.question,
            "subject": data.subject,
            "answer": answer,
            "xp_earned": 10,
            "total_xp": user.xp,
            "streak_count": user.streak_count,
        }

    except httpx.HTTPStatusError as groq_err:
        db.rollback()
        # Explicitly catch errors from the Groq call
        raise HTTPException(
            status_code=502,
            detail=f"Groq API error: {groq_err.response.status_code} - {groq_err.response.text}",
        )
    except Exception as e:
        db.rollback()
        # Log or print traceback if you need more detail here
        raise HTTPException(status_code=500, detail=str(e))
