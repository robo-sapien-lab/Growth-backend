from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.chat import DirectMessage
from app.models.user import User
from app.database import get_db

router = APIRouter()

@router.post("/chat/send")
def send_message(sender_id: int, receiver_id: int, content: str, db: Session = Depends(get_db)):
    sender = db.query(User).filter(User.id == sender_id).first()
    receiver = db.query(User).filter(User.id == receiver_id).first()

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Sender or receiver not found")

    if sender.school_id != receiver.school_id:
        raise HTTPException(status_code=403, detail="Can only message users from the same school")

    message = DirectMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content,
        timestamp=datetime.utcnow()
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {"message": "Message sent", "id": message.id}

@router.get("/chat/history/{user1_id}/{user2_id}")
def get_chat_history(user1_id: int, user2_id: int, db: Session = Depends(get_db)):
    messages = db.query(DirectMessage).filter(
        ((DirectMessage.sender_id == user1_id) & (DirectMessage.receiver_id == user2_id)) |
        ((DirectMessage.sender_id == user2_id) & (DirectMessage.receiver_id == user1_id))
    ).order_by(DirectMessage.timestamp).all()

    return [
        {
            "id": msg.id,
            "sender_id": msg.sender_id,
            "receiver_id": msg.receiver_id,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]
