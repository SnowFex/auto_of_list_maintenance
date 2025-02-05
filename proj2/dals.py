from typing import Union
from sqlalchemy import select
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.DB_Creator.model_db import Notes


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        address: str,
        floor: int,
        full_name: str,
        position_at_work: str,
        computer_name: str,
        work_group: str,
        comment: str,
    ) -> Notes:
        new_user = Notes(
            address=address,
            floor=floor,
            full_name=full_name,
            position_at_work=position_at_work,
            computer_name=computer_name,
            work_group=work_group,
            comment=comment
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, full_name: str) -> Union[str, None]:
        query = (
            delete(Notes)
            .where(Notes.full_name == full_name)
            .returning(Notes.full_name)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_name(self, full_name: str) -> Union[str, None]:
        query = select(Notes).where(Notes.full_name == full_name)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, full_name: str, **kwargs) -> Union[str, None]:
        query = (
            update(Notes)
            .where(Notes.full_name == full_name)
            .values(kwargs)
            .returning(Notes.full_name)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]