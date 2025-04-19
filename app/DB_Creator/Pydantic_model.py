from pydantic import BaseModel


class User_create(BaseModel):
    address: str
    floor: str
    cabinet: str
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str
    ip_address: str
    kaspersky: str
    comment: str = None
    windows: str


class User_Create(BaseModel):
    email: str
    hashed_password: str

class User_Response(BaseModel):
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str