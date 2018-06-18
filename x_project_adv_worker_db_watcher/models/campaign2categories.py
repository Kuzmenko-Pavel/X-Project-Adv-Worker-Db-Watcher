from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2Categories(Base):
    __tablename__ = 'campaign2categories'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_cat = Column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2Categories(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2categories',
        select([
            Campaign2Categories.id_cam,
            Campaign2Categories.id_cat
        ]).select_from(Campaign2Categories),
        is_mat=True)


Index('ix_mv_campaign2categories__id_cam__id_cat',
      MVCampaign2Categories.id_cam, MVCampaign2Categories.id_cat, unique=True)
