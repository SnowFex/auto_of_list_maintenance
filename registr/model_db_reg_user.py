from sqlalchemy import Column, String, Integer
from app.DB_Creator.db_api import Base



class User_Reg(Base):
    __tablename__ = "registration"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)