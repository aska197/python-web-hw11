from typing import Union
from libgravatar import Gravatar
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas import UserModel  # Assuming UserModel is correctly defined in app/schemas.py

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_token(user: User, token: Union[str, None], db: Session) -> None:
    user.refresh_token = token
    db.commit()