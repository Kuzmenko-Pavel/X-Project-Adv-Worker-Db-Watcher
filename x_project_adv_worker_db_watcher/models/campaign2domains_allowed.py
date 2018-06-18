__all__ = ['Campaign2DomainsAllowed', 'MVCampaign2DomainsAllowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2DomainsAllowed(Base):
    __tablename__ = 'campaign2domains_allowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_dom = Column(BigInteger, ForeignKey('domains.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2DomainsAllowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2domains_allowed',
        select([
            Campaign2DomainsAllowed.id_cam,
            Campaign2DomainsAllowed.id_dom
        ]).select_from(Campaign2DomainsAllowed),
        is_mat=True)


Index('ix_mv_campaign2domains_allowed__id_cam__id_dom', MVCampaign2DomainsAllowed.id_cam,
      MVCampaign2DomainsAllowed.id_dom, unique=True)
