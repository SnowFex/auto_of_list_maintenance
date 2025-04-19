from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row, RowMapping, column, or_
from app.DB_Creator.Pydantic_model import User_create
from app.DB_Creator.db_api import get_async_session
from app.DB_Creator.model_db import Notes
from typing import List, Optional
import logging

get_router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@get_router.get("/get_user", response_model=List[User_create])
async def get_user_for_name(computer_name: Optional[str] = None,
                            address: Optional[str] = None,
                            full_name: Optional[str] = None,
                            session: AsyncSession = Depends(get_async_session)):
    query = select(Notes)
    if computer_name:
        query = query.where(Notes.computer_name.op('~')(f'^{computer_name}'))
    if address:
        query = query.where(Notes.address.op('~')(address))
    if full_name:
        query = query.where(Notes.full_name.op('~')(full_name))
    logger.debug(f"Generated SQL: {query}")
    res = await session.execute(query)
    user_row = list(set(res.scalars().all()))
    if user_row:
        return user_row
    else:
        raise HTTPException(status_code=404, detail="No users found")
