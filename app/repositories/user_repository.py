from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user_model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(
        self,
        email: str,
        password_hash: str,
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
        )

        self.db.add(user)

        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise

        self.db.refresh(user)

        return user

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:
        statement = select(User).where(User.email == email)

        return self.db.scalar(statement)

    def get_user_by_id(
        self,
        user_id: str,
    ) -> User | None:
        statement = select(User).where(User.id == user_id)

        return self.db.scalar(statement)

    def user_exists(
        self,
        email: str,
    ) -> bool:
        statement = select(User.id).where(User.email == email)

        return self.db.scalar(statement) is not None