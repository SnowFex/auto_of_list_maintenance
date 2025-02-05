from logging import getLogger

from fastapi import APIRouter, Form
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Body
from proj2.user import _create_new_user
from proj2.user import _delete_user
from proj2.user import _get_user_by_name
from proj2.user import _update_user
from typing import Union
from proj2.schemas import DeleteUserResponse
from proj2.schemas import ShowUser
from proj2.schemas import UpdatedUserResponse
from proj2.schemas import UpdateUserRequest
from fastapi.responses import FileResponse
from app.DB_Creator.db_api import get_async_session

from app.DB_Creator.Pydantic_model import User_create

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.get("/")
def root():
    return FileResponse("public/v2.html")


@user_router.post("/create", response_model=ShowUser)
async def create_user(body: User_create = Form(), db: AsyncSession = Depends(get_async_session)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/delete", response_model=DeleteUserResponse)
async def delete_user(
    full_name: str,
    db: AsyncSession = Depends(get_async_session)
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_name(full_name, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {full_name} not found."
        )
    deleted_user_name = await _delete_user(full_name, db)
    if deleted_user_name is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {full_name} not found."
        )
    return DeleteUserResponse(deleted_user_name=deleted_user_name)


@user_router.get("/get user", response_model=ShowUser)
async def get_user_by_name(full_name: str, db: AsyncSession = Depends(get_async_session)) -> Union[str, None]:
    user = await _get_user_by_name(full_name=full_name, session=db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {full_name} not found."
        )
    return user


@user_router.patch("/update_user", response_model=UpdatedUserResponse)
async def update_user_by_name(
    name: str,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_async_session),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_name(name, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {name} not found."
        )
    try:
        updated_user_name = await _update_user(full_name=name, updated_user_params=updated_user_params, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_name=updated_user_name)
