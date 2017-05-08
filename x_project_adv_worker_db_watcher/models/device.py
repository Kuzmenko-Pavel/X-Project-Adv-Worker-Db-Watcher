from sqlalchemy import (Column, Integer, String)
from .meta import Base


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2), unique=True)
