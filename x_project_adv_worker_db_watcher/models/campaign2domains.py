from sqlalchemy import (Column, Integer, BigInteger, Boolean, UniqueConstraint, ForeignKey)
from .meta import Base


class Campaign2Domains(Base):
    __tablename__ = 'campaign2domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), nullable=False)
    id_dom = Column(Integer, ForeignKey('domains.id'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)

    __table_args__ = (UniqueConstraint('id_cam', 'id_dom', name='id_cam_id_dom_uc'),)
