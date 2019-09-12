from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2BlockingBlock(Base):
    __tablename__ = 'campaigns_by_blocking_block'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_block = Column(Integer, ForeignKey('block.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2BlockingBlock(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaigns_by_blocking_block',
        select([
            Campaign2BlockingBlock.id_cam,
            Campaign2BlockingBlock.id_block
        ]).select_from(Campaign2BlockingBlock),
        is_mat=True)


Index('ix_mv_domains_id_cam_pk_id_geo_pk', MVCampaign2BlockingBlock.id_cam, MVCampaign2BlockingBlock.id_block,
      unique=True)
