from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import select, insert, update, delete
from slugify import slugify

router = APIRouter()


@router.get("/")
async def all_users(db: Session = Depends(get_db)):
    users = db.execute(select(User)).scalars().all()
    return users


@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@router.post("/create")
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = User(**user.dict(), slug=slugify(user.username))
    db.add(db_user)
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put("/update")
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}


@router.delete("/delete")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User was not found")

    db.delete(db_user)
    db.commit()
    return {'status_code': status.HTTP_204_NO_CONTENT, 'transaction': 'User deleted successfully!'}