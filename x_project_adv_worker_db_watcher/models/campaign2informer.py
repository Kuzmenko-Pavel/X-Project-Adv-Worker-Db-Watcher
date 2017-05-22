from sqlalchemy import (Column, Integer, BigInteger, Boolean, UniqueConstraint, ForeignKey, select, Index, cast)
from .meta import Base
from .__libs__.sql_view import create_view


class Campaign2Informer(Base):
    __tablename__ = 'campaign2informer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    id_inf = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)


class MVCampaign2Informer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2informer',
        select([
            Campaign2Informer.id,
            cast(Campaign2Informer.id_cam, BigInteger).label('id_cam'),
            cast(Campaign2Informer.id_inf, BigInteger).label('id_inf'),
            Campaign2Informer.allowed
        ]).select_from(Campaign2Informer),
        is_mat=True)


Index('ix_mv_campaign2informer_id', MVCampaign2Informer.id, unique=True)
Index('ix_mv_campaign2informer_id_cam_id_inf', MVCampaign2Informer.id_cam, MVCampaign2Informer.id_inf, )
Index('ix_mv_campaign2informer_allowed', MVCampaign2Informer.allowed)
