from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, Float)
from .meta import Base


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True, index=True)
    campaignId = Column(Integer)
    image = Column(String)
    uniqueHits = Column(SmallInteger)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    campaign_guid = Column(String(length=64))
    social = Column(Boolean)
    offer_by_campaign_unique = Column(SmallInteger)
    UnicImpressionLot = Column(SmallInteger)
    html_notification = Column(Boolean)
    rating = Column(Float)