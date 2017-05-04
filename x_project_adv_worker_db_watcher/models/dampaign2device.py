from sqlalchemy import (Column, Integer)
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)