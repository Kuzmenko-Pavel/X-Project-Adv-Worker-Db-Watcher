from sqlalchemy import (Column, BigInteger, Integer, String, Boolean, SmallInteger, Float, ForeignKey)
from sqlalchemy.orm import relationship
from .meta import Base


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True, index=True)
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), nullable=False)
    image = Column(String)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(String)
    campaign = relationship('Campaign', back_populates="offers")
