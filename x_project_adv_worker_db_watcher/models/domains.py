from sqlalchemy import (Column, Integer, String)
from .meta import Base


class Domains(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
