from app.DB_Creator.Pydantic_model import User_Create, User_Response
from app.DB_Creator.db_api import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from registr.model_db_reg_user import User_Reg
from registr.hash_pass import Hasher


create_reg_router = APIRouter()
@create_reg_router.post("/register_user", response_model=User_Response)
async def create_user(user: User_Create, sessions: AsyncSession = Depends(get_async_session)):
    existing_user = await get_user_for_email(user.email, sessions)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        )
    new_user = User_Reg(
                    email=user.email,
                    hashed_password=Hasher.get_password_hash(user.hashed_password))
    sessions.add(new_user)
    await sessions.commit()
    await sessions.refresh(new_user)
    return User_Response(
        email=new_user.email
    )

async def get_user_for_email(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(User_Reg).where(User_Reg.email == email)
    res = await session.execute(query)
    user_row = res.fetchone()
    if user_row is not None:
        return user_row[0]