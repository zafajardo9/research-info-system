from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import update
from sqlalchemy import delete
from sqlalchemy.future.engine import Connection
from sqlalchemy.sql.expression import BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import db

T = TypeVar('T')


class BaseRepo:
    model = Generic[T]

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        model = cls.model(**kwargs)
        db.add(model)
        await db.commit()
        return model

    @classmethod
    async def get_all(cls, db: AsyncSession):
        query = select(cls.model)
        return await db.execute(query)

    @classmethod
    async def get_by_id(cls, db: AsyncSession, model_id: int):
        query = select(cls.model).where(cls.model.id == model_id)
        return await db.execute(query)

    @classmethod
    async def update(cls, db: AsyncSession, model: T, **kwargs):
        for key, value in kwargs.items():
            setattr(model, key, value)
        await db.commit()

    @classmethod
    async def delete(cls, db: AsyncSession, model: T):
        db.delete(model)
        await db.commit()
