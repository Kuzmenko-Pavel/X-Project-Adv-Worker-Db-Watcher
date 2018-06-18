__all__ = ['Campaign2AccountsAllowed', 'MVCampaign2AccountsAllowed']
from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2AccountsAllowed(Base):
    __tablename__ = 'campaign2accounts_allowed'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_acc = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2AccountsAllowed(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2accounts_allowed',
        select([
            Campaign2AccountsAllowed.id_cam,
            Campaign2AccountsAllowed.id_acc
        ]).select_from(Campaign2AccountsAllowed),
        is_mat=True)


Index('ix_mv_campaign2accounts_allowed__id_cam__id_acc', MVCampaign2AccountsAllowed.id_cam,
      MVCampaign2AccountsAllowed.id_acc, unique=True)
