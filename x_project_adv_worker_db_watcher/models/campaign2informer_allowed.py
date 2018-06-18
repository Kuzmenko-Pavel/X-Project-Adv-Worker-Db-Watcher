__all__ = ['Campaign2InformerAllowed', 'MVCampaign2InformerAllowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2InformerAllowed(Base):
    __tablename__ = 'campaign2informer_allowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_inf = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2InformerAllowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2informer_allowed',
        select([
            Campaign2InformerAllowed.id_cam,
            Campaign2InformerAllowed.id_inf
        ]).select_from(Campaign2InformerAllowed),
        is_mat=True)


Index('ix_campaign2informer_allowed__id_cam__id_inf', MVCampaign2InformerAllowed.id_cam,
      MVCampaign2InformerAllowed.id_inf, unique=True)
