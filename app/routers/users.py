from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/{user_id}")
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user

@router.post("/create")
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(user.username)
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slug
    )
    db.execute(insert(User).values(new_user.__dict__))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update/{user_id}")
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(
        update(User).where(User.id == user_id).values(**user.dict())
    )
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    existing_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deletion is successful!'}