from sqlalchemy import (Column, Integer)
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, primary_key=True, autoincrement=True)