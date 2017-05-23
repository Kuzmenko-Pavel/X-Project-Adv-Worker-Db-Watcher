from sqlalchemy import (Column, BigInteger, String, Float, ForeignKey, select, Index, cast)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func, join, true, false, and_

from .__libs__.sql_view import create_view
from .campaign import Campaign
from .meta import Base


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='', index=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(String)
    description = Column(String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(ARRAY(String), default=[])
    campaigns = relationship('Campaign', back_populates="offers", passive_deletes=True)


class MVOfferPlace(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_place',
        select([
            Offer.id,
            Offer.guid,
            cast(Offer.id_cam, BigInteger).label('id_cam'),
            cast(Campaign.account, String).label('accounts_cam'),
            cast(Campaign.guid, String).label('guid_cam'),
            cast(Campaign.title, String).label('title_cam'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            func.recommended_to_json(Offer.recommended).label('recommended')
        ]).select_from(
            join(Offer, Campaign, Offer.id_cam == Campaign.id, isouter=True)
        ).where(and_(Campaign.social == false(), Campaign.retargeting == false())).order_by(Offer.rating), is_mat=True)


Index('ix_mv_offer_place_id', MVOfferPlace.id, unique=True)


class MVOfferSocial(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social',
        select([
            Offer.id,
            Offer.guid,
            cast(Offer.id_cam, BigInteger).label('id_cam'),
            cast(Campaign.account, String).label('accounts_cam'),
            cast(Campaign.guid, String).label('guid_cam'),
            cast(Campaign.title, String).label('title_cam'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            func.recommended_to_json(Offer.recommended).label('recommended')
        ]).select_from(
            join(Offer, Campaign, Offer.id_cam == Campaign.id, isouter=True)
        ).where(and_(Campaign.social == true(), Campaign.retargeting == false())).order_by(Offer.rating),
        is_mat=True)


Index('ix_mv_offer_social_id', MVOfferSocial.id, unique=True)


class MVOfferAccountRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_account_retargeting',
        select([
            Offer.id,
            Offer.guid,
            cast(Offer.id_cam, BigInteger).label('id_cam'),
            cast(Campaign.account, String).label('accounts_cam'),
            cast(Campaign.guid, String).label('guid_cam'),
            cast(Campaign.title, String).label('title_cam'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            func.recommended_to_json(Offer.recommended).label('recommended')
        ]).select_from(
            join(Offer, Campaign, Offer.id_cam == Campaign.id, isouter=True)
        ).where(and_(Campaign.retargeting == true(), Campaign.retargeting_type == 'account')),
        is_mat=True)


Index('ix_mv_offer_account_retargeting_id', MVOfferAccountRetargeting.id, unique=True)


class MVOfferDynamicRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_dynamic_retargeting',
        select([
            Offer.id,
            Offer.guid,
            cast(Offer.id_cam, BigInteger).label('id_cam'),
            cast(Campaign.account, String).label('accounts_cam'),
            cast(Campaign.guid, String).label('guid_cam'),
            cast(Campaign.title, String).label('title_cam'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            func.recommended_to_json(Offer.recommended).label('recommended')
        ]).select_from(
            join(Offer, Campaign, Offer.id_cam == Campaign.id, isouter=True)
        ).where(and_(Campaign.retargeting == true(), Campaign.retargeting_type == 'offer')),
        is_mat=True)


Index('ix_mv_offer_dynamic_retargeting_id', MVOfferDynamicRetargeting.id, unique=True)
