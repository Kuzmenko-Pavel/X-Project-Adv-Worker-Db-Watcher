from sqlalchemy import (Column, Integer)
from .meta import Base


class GeoLiteCity(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True, autoincrement=True)