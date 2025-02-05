from sqlalchemy import Column, Integer, String
from app.DB_Creator.db_api import Base


class Notes(Base):
    __tablename__ = "notes"

    address = Column(String, nullable=False)
    floor = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    position_at_work = Column(String, nullable=False)
    computer_name = Column(String, nullable=False)
    work_group = Column(String, nullable=False)
    comment = Column(String)