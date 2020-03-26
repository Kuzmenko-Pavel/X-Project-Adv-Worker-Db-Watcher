from sqlalchemy import (Column, Float, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2BlockPrice(Base):
    __tablename__ = 'campaigns_by_block_price'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_block = Column(BigInteger, primary_key=True, nullable=False)
    click_cost = Column(Float)
    impression_cost = Column(Float)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2BlockPrice(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaigns_by_block_price',
        select([
            Campaign2BlockPrice.id_cam,
            Campaign2BlockPrice.id_block,
            Campaign2BlockPrice.click_cost,
            Campaign2BlockPrice.impression_cost,
        ]).select_from(Campaign2BlockPrice),
        is_mat=True)


Index('ix_mv_campaigns_by_block_price_block_id_cam_id_block',
      MVCampaign2BlockPrice.id_cam, MVCampaign2BlockPrice.id_block,
      unique=True)
