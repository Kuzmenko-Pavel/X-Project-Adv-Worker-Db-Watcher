from sqlalchemy import (Column, Integer, BigInteger, Boolean, UniqueConstraint, ForeignKey)
from .meta import Base


class Campaign2Informer(Base):
    __tablename__ = 'campaign2informer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    id_inf = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)

    __table_args__ = (UniqueConstraint('id_cam', 'id_inf', name='id_cam_id_inf_uc'),)
