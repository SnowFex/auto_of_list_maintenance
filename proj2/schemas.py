import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr, conint
from pydantic import validator

#########################
# BLOCK WITH API MODELS #
#########################

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    address: str
    floor: str
    cabinet: str
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str
    ip_address: str
    kaspersky: str
    windows: str


class UserCreate(BaseModel):
    address: str
    floor: str
    cabinet: str
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str
    ip_address: str
    kaspersky: str
    comment: str
    windows: str

    @validator("full_name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_name: str


class UpdatedUserResponse(BaseModel):
    updated_computer_name: str


class UpdateUserRequest(BaseModel):
    address: Optional[constr()] = None
    floor: Optional[constr()] = None
    cabinet: Optional[constr()] = None
    full_name: Optional[constr()] = None
    position_at_work: Optional[constr()] = None
    work_group: Optional[constr()] = None
    ip_address: Optional[constr()] = None
    kaspersky: Optional[constr()] = None
    comment: Optional[str] = None
    windows: Optional[constr()] = None
