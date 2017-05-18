from sqlalchemy import (Column, BigInteger, Integer, String, Boolean, SmallInteger, Float, Index, ForeignKey)
from sqlalchemy.orm import relationship
from .meta import Base


class OfferPlace(Base):
    __tablename__ = 'offer_place'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(String)

    __table_args__ = (
        Index('ix_offer_place_rating', rating.desc(), postgresql_using='btree', postgresql_with={"fillfactor": 50}),
    )


class OfferSocial(Base):
    __tablename__ = 'offer_social'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(String)

    __table_args__ = (
        Index('ix_offer_social_rating', rating.desc(), postgresql_using='btree', postgresql_with={"fillfactor": 50}),
    )


class OfferAccountRetargeting(Base):
    __tablename__ = 'offer_account_retargeting'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(String)


class OfferDynamicRetargeting(Base):
    __tablename__ = 'offer_dynamic_retargeting'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    description = (String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(String)
