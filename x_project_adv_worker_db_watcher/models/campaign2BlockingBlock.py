from sqlalchemy import (Column, Boolean, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2BlockingBlock(Base):
    __tablename__ = 'campaigns_by_blocking_block'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_block = Column(BigInteger, ForeignKey('block.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    change = Column(Boolean, default=False)

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


Index('ix_mv_campaigns_by_blocking_block_id_cam_id_block',
      MVCampaign2BlockingBlock.id_cam, MVCampaign2BlockingBlock.id_block,
      unique=True)

Index('ix_mv_campaigns_by_blocking_block_id_block', MVCampaign2BlockingBlock.id_block)
