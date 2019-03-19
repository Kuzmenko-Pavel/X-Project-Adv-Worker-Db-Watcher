from sqlalchemy import (Column, Integer, String, UniqueConstraint, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class GeoLiteCity(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(length=9))
    city = Column(String(length=50))
    __table_args__ = (
        UniqueConstraint('country', 'city', name='country_city_uc'),
        {'prefixes': ['UNLOGGED']}
    )

    def __repr__(self):
        return 'GeoLiteCity %s %s' % (self.country, self.city)


class MVGeoLiteCity(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_geo_lite_city',
        select([
            GeoLiteCity.id,
            GeoLiteCity.country,
            GeoLiteCity.city
        ]).select_from(GeoLiteCity),
        is_mat=True)


Index('ix_mv_geo_lite_city', MVGeoLiteCity.country, MVGeoLiteCity.city, unique=True)
