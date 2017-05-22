from sqlalchemy import (Column, Integer, String, UniqueConstraint, select, Index, select, Index, cast)
from sqlalchemy.orm import relationship
from .meta import Base
from .__libs__.sql_view import create_view


class GeoLiteCity(Base):
    __tablename__ = 'geo_lite_city'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(length=9))
    region = Column(String(length=2))
    city = Column(String(length=50))
    campaigns = relationship('Campaign', secondary='geo', back_populates="geos", passive_deletes=True)
    __table_args__ = (UniqueConstraint('country', 'region', 'city',  name='country_region_city_uc'),)


class MVGeoLiteCity(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_geo_lite_city',
        select([
            GeoLiteCity.id,
            GeoLiteCity.country,
            GeoLiteCity.region,
            GeoLiteCity.city
        ]).select_from(GeoLiteCity),
        is_mat=True)


Index('ix_mv_geo_lite_city', MVGeoLiteCity.country, MVGeoLiteCity.region, MVGeoLiteCity.city, unique=True)
