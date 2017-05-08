from sqlalchemy import (Column, Integer, SmallInteger, ForeignKey)
from .meta import Base


class Campaign2Domains(Base):
    __tablename__ = 'campaign2domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(Integer, ForeignKey('campaign.id'))
    id_dom = Column(Integer, ForeignKey('domains.id'))
    allowed = Column(SmallInteger)