# Домашнее задание по теме "Модели SQLALchemy. Отношения между таблицами."
# ННазаров ПВ
# module_17_2.py

from fastapi import APIRouter

# Импортируем роутеры
from .task import router as task_router
from .user import router as user_router

# Создаем главный роутер и объединяем маршруты
router = APIRouter()
router.include_router(task_router)
router.include_router(user_router)