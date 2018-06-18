__all__ = ['Campaign2AccountsDisallowed', 'MVCampaign2AccountsDisallowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2AccountsDisallowed(Base):
    __tablename__ = 'campaign2accounts_disallowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_acc = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2AccountsDisallowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2accounts_disallowed',
        select([
            Campaign2AccountsDisallowed.id_cam,
            Campaign2AccountsDisallowed.id_acc
        ]).select_from(Campaign2AccountsDisallowed),
        is_mat=True)


Index('ix_mv_campaign2accounts_disallowed__id_cam__id_acc',
      MVCampaign2AccountsDisallowed.id_cam,
      MVCampaign2AccountsDisallowed.id_acc, unique=True)
