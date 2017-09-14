from sqlalchemy import (Column, Integer, BigInteger, Boolean, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2Domains(Base):
    __tablename__ = 'campaign2domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    id_dom = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2Domains(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2domains',
        select([
            Campaign2Domains.id,
            cast(Campaign2Domains.id_cam, BigInteger).label('id_cam'),
            cast(Campaign2Domains.id_dom, Integer).label('id_dom'),
            Campaign2Domains.allowed
        ]).select_from(Campaign2Domains),
        is_mat=True)


Index('ix_mv_campaign2domains_id', MVCampaign2Domains.id, unique=True)
