from sqlalchemy import (Column, Integer, Boolean, String)
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
    blocked = Column(Boolean, default=False)
