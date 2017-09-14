from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2Categories(Base):
    __tablename__ = 'campaign2categories'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_cat = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2Categories(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2categories',
        select([
            cast(Campaign2Categories.id_cam, BigInteger).label('id_cam_pk'),
            cast(Campaign2Categories.id_cat, Integer).label('id_cat_pk')
        ]).select_from(Campaign2Categories),
        is_mat=True)


Index('ix_mv_campaign2categories_id_cam_pk_id_cat_pk',
      MVCampaign2Categories.id_cam_pk, MVCampaign2Categories.id_cat_pk, unique=True)
