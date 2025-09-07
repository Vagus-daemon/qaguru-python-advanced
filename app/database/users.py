from fastapi import HTTPException
from typing import Iterable, Type
from sqlmodel import Session, select

from app.database.engine import engine
from app.models.User import User, UserCreate


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def create_user(user: UserCreate) -> User:
    with Session(engine) as session:
        user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            avatar=str(user.avatar)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user: User) -> Type[User]:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
