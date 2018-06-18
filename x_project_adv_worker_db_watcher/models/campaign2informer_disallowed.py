__all__ = ['Campaign2InformerDisallowed', 'MVCampaign2InformerDisallowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2InformerDisallowed(Base):
    __tablename__ = 'campaign2informer_disallowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_inf = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False, primary_key=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2InformerDisallowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2informer_disallowed',
        select([
            Campaign2InformerDisallowed.id_cam,
            Campaign2InformerDisallowed.id_inf
        ]).select_from(Campaign2InformerDisallowed),
        is_mat=True)


Index('ix_campaign2informer_disallowed__id_cam__id_inf', MVCampaign2InformerDisallowed.id_cam,
      MVCampaign2InformerDisallowed.id_inf, unique=True)
