from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from app.DB_Creator.Pydantic_model import User_create
from app.DB_Creator.db_api import get_async_session
from app.DB_Creator.model_db import Notes
from typing import Union

create_router = APIRouter(prefix='/create user', tags=['Create User'])
get_router = APIRouter(prefix="/get user", tags=["Get User"])
delete_router = APIRouter(prefix="/delete user", tags=["Delete"])


@create_router.post("/create_user", response_model=User_create)
async def create_user(user: User_create, sessions: AsyncSession = Depends(get_async_session)) -> User_create:
    new_user = Notes(address=user.address,
    floor=user.floor,
    full_name=user.full_name,
    position_at_work=user.position_at_work,
    computer_name=user.computer_name,
    work_group=user.work_group,
    comment=user.comment)
    sessions.add(new_user)
    await sessions.commit()
    await sessions.refresh(new_user)
    return User_create(
        address=user.address,
        floor=user.floor,
        full_name=user.full_name,
        position_at_work=user.position_at_work,
        computer_name=user.computer_name,
        work_group=user.work_group,
        comment=user.comment
    )


async def update_user(name: str, **kwargs) -> Union[str, None]:
    query = (
        update(Notes)
        .where(Notes.full_name == name)
        .values(kwargs)
        .returning(Notes.user_id)
    )
    res = await db_session.execute(query)
    update_user_id_row = res.fetchone()
    if update_user_id_row is not None:
        return update_user_id_row[0]


@get_router.get("/get_user", response_model=User_create)
async def get_user_for_name(full_name: str, session: AsyncSession = Depends(get_async_session)) -> Union[int, None]:
    query = select(Notes).where(Notes.full_name == full_name)
    res = await session.execute(query)
    user_row = res.fetchone()
    if user_row is not None:
        return user_row[0]
    else:
        raise HTTPException(status_code=400, detail="Not found name")


# @delete_router.delete("/delete_user", response_model=add_user)
# async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)) -> add_user:
#     query = update(User)\
#         .where(and_(User.user_id == user_id, User.is_active == True))\
#         .values(is_active=False)\
#         .returning(User.user_id)
#     res = await session.execute(query)
#     deleted_user_id_rows = res.fetchone()
#     if deleted_user_id_rows is not None:
#         return deleted_user_id_rows[0]