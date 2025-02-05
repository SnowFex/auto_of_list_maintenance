from pydantic import BaseModel


class User_create(BaseModel):
    address: str
    floor: int
    full_name: str
    position_at_work: str
    computer_name: str
    work_group: str
    comment: str = None