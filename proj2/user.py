from typing import Union

from proj2.schemas import ShowUser
from app.DB_Creator.Pydantic_model import User_create
from app.DB_Creator.model_db import Notes
from proj2.dals import UserDAL


async def _create_new_user(body: User_create, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            address=body.address,
            floor=body.floor,
            cabinet=body.cabinet,
            full_name=body.full_name,
            position_at_work=body.position_at_work,
            computer_name=body.computer_name,
            work_group=body.work_group,
            ip_address=body.ip_address,
            kaspersky=body.kaspersky,
            comment=body.comment,
            windows=body.windows
        )
        return ShowUser(
            address=user.address,
            floor=user.floor,
            cabinet=user.cabinet,
            full_name=user.full_name,
            position_at_work=user.position_at_work,
            computer_name=user.computer_name,
            work_group=user.work_group,
            ip_address=user.ip_address,
            kaspersky=user.kaspersky,
            comment=user.comment,
            windows=user.windows
        )


async def _delete_user(computer_name, session) -> Union[str, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            computer_name=computer_name,
        )
        return deleted_user_id


async def _update_user(computer_name: str, updated_user_params: dict, session) -> Union[str, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_name = await user_dal.update_user(
            computer_name=computer_name, **updated_user_params
        )
        return updated_user_name


async def _get_user_by_name(computer_name, session) -> Union[Notes, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_name(
            computer_name=computer_name,
        )
        if user is not None:
            return user

