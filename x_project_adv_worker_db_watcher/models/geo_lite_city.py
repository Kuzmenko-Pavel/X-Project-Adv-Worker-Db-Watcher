from sqlalchemy import (Column, Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship
from .meta import Base


class GeoLiteCity(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(length=9))
    region = Column(String(length=2))
    city = Column(String(length=50))
    campaigns = relationship('Campaign', secondary='geo', back_populates="geos", passive_deletes=True)
    __table_args__ = (UniqueConstraint('country', 'region', 'city',  name='country_region_city_uc'),)
