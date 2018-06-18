__all__ = ['Campaign2DomainsDisallowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2DomainsDisallowed(Base):
    __tablename__ = 'campaign2domains_disallowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_dom = Column(BigInteger, ForeignKey('domains.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2DomainsDisallowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2domains_disallowed',
        select([
            Campaign2DomainsDisallowed.id_cam,
            Campaign2DomainsDisallowed.id_dom
        ]).select_from(Campaign2DomainsDisallowed),
        is_mat=True)


Index('ix_mv_campaign2domains_disallowed__id_cam__id_dom', MVCampaign2DomainsDisallowed.id_cam,
      MVCampaign2DomainsDisallowed.id_dom, unique=True)
