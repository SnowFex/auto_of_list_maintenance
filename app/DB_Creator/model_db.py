from sqlalchemy import Column, Integer, String
from app.DB_Creator.db_api import Base


class Notes(Base):
    __tablename__ = "testnotes"

    id = Column(Integer, primary_key=True)
    address = Column(String)
    floor = Column(String)
    cabinet = Column(String)
    full_name = Column(String)
    position_at_work = Column(String)
    computer_name = Column(String)
    work_group = Column(String)
    ip_address = Column(String)
    kaspersky = Column(String)
    comment = Column(String)
    windows = Column(String)