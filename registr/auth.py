from datetime import timedelta, datetime
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter, Response
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.DB_Creator.Pydantic_model import Token, TokenData, User_Create, User_Response
from app.DB_Creator.db_api import get_async_session
from registr.model_db_reg_user import User_Reg
from registr.hash_pass import Hasher
from sqlalchemy import select
from config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login_user/auth_user")
JWT_ACCESS_COOKIE_NAME = "access_token"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

login_router = APIRouter(prefix="/login_user")


async def get_user_for_email(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(User_Reg).where(User_Reg.email == email)
    res = await session.execute(query)
    user_row = res.fetchone()
    if user_row is not None:
        return user_row[0]


async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await get_user_for_email(email=email, session=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str, db: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user_for_email(email=token_data.email, session=db)
    if user is None:
        raise credentials_exception
    return user


@login_router.post("/auth_user", response_model=Token)
async def login_for_access_token(response: Response, form_data: User_Create, db: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(form_data.email, form_data.hashed_password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(JWT_ACCESS_COOKIE_NAME, access_token)
    return Token(access_token=access_token, token_type="bearer")


@login_router.get("/auth_user_header", response_model=User_Response)
async def sample_endpoint_under_jwt(current_user: str = Depends(get_current_user)):
    return current_user