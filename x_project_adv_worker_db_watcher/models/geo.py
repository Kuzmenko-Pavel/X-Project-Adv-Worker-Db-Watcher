from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Geo(Base):
    __tablename__ = 'geo'
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), primary_key=True, nullable=False)
    id_geo = Column(Integer, ForeignKey('geo_lite_city.id'), primary_key=True, nullable=False)
