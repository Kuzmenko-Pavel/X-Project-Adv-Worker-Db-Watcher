from sqlalchemy import (Column, Integer, BigInteger, Boolean, UniqueConstraint, ForeignKey)
from .meta import Base


class Campaign2Domains(Base):
    __tablename__ = 'campaign2domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'))
    id_dom = Column(Integer, ForeignKey('domains.id'))
    allowed = Column(Boolean, default=False)

    __table_args__ = (UniqueConstraint('id_cam', 'id_dom', name='id_cam_id_dom_uc'),)
