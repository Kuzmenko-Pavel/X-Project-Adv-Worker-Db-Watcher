from sqlalchemy import (Column, Integer, String, UniqueConstraint, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Geo(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True)
    country = Column(String(length=9))
    city = Column(String(length=50))
    __table_args__ = (
        UniqueConstraint('country', 'city', name='country_city_uc'),
        {'prefixes': ['UNLOGGED']}
    )

    def __repr__(self):
        return 'GeoLiteCity %s %s' % (self.country, self.city)


class MVGeo(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_geo_lite_city',
        select([
            Geo.id,
            Geo.country,
            Geo.city
        ]).select_from(Geo),
        is_mat=True)


Index('ix_mv_geo_lite_city', MVGeo.country, MVGeo.city, unique=True)
