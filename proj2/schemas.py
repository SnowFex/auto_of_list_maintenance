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
    floor: int
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str


class UserCreate(BaseModel):
    address: str
    floor: int
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str
    comment: str

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
    updated_user_name: str


class UpdateUserRequest(BaseModel):
    address: Optional[constr(min_length=1)]
    floor: Optional[conint()]
    position_at_work: Optional[constr(min_length=1)]
    computer_name: Optional[constr(min_length=1)]
    work_group: Optional[constr(min_length=1)]
    comment: Optional[constr(min_length=1)]
