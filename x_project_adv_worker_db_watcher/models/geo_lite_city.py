from sqlalchemy import (Column, Integer, String, UniqueConstraint)
from .meta import Base


class GeoLiteCity(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(length=9))
    region = Column(String(length=2))
    city = Column(String(length=50))
    __table_args__ = (UniqueConstraint('country', 'region', 'city',  name='country_region_city_uc'),)
