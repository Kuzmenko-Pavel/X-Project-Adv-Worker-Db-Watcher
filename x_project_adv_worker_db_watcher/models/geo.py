from sqlalchemy import (Column, Integer, ForeignKey)
from .meta import Base


class Geo(Base):
    __tablename__ = 'geo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(Integer, ForeignKey('campaign.id'))
    id_geo = Column(Integer, ForeignKey('geo_lite_city.id'))
