from sqlalchemy import (Column, Integer, BigInteger, UniqueConstraint, Boolean, ForeignKey)
from .meta import Base


class Campaign2Accounts(Base):
    __tablename__ = 'campaign2accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), nullable=False)
    id_acc = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    allowed = Column(Boolean, default=False, index=True)

    __table_args__ = (UniqueConstraint('id_cam', 'id_acc', name='id_cam_id_acc_uc'),)
