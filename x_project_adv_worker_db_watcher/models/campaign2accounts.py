from sqlalchemy import (Column, Integer, BigInteger, UniqueConstraint, Boolean, ForeignKey, select, Index, cast)
from .meta import Base
from .__libs__.sql_view import create_view


class Campaign2Accounts(Base):
    __tablename__ = 'campaign2accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    id_acc = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)

    __table_args__ = (UniqueConstraint('id_cam', 'id_acc', name='id_cam_id_acc_uc'),)


class MVCampaign2Accounts(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2accounts',
        select([
            Campaign2Accounts.id,
            cast(Campaign2Accounts.id_cam, BigInteger).label('id_cam'),
            cast(Campaign2Accounts.id_acc, Integer).label('id_acc'),
            Campaign2Accounts.allowed
        ]).select_from(Campaign2Accounts),
        is_mat=True)


Index('ix_mv_campaign2accounts_id', MVCampaign2Accounts.id, unique=True)
