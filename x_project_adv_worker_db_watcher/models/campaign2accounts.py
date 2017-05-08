from sqlalchemy import (Column, Integer, UniqueConstraint, ForeignKey)
from .meta import Base


class Campaign2Accounts(Base):
    __tablename__ = 'campaign2accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(Integer, ForeignKey('campaign.id'))
    id_acc = Column(Integer, ForeignKey('accounts.id'))
    __table_args__ = (UniqueConstraint('id_cam', 'id_acc', name='id_cam_id_acc_uc'), )