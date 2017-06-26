from sqlalchemy import (Column, BigInteger, String, Float, Boolean, ForeignKey, select, Index, cast)
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func, join, true, false, and_

from .__libs__.sql_view import create_view
from .campaign import Campaign
from .meta import Base


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64))
    retid = Column(String, default='')
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    image = Column(ARRAY(String), default=[])
    description = Column(String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    price = Column(String(length=35))
    rating = Column(Float)
    recommended = Column(ARRAY(String), default=[])
    campaigns = relationship('Campaign', back_populates="offers", passive_deletes=True)
    __table_args__ = (
        Index('ix_offer_rating', rating.desc().nullslast()),
        Index('ix_offer_retid_id_cam', retid, id_cam.desc().nullslast()),
        # {'prefixes': ['UNLOGGED']}
    )


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
            cast(Campaign.brending, Boolean).label('brending'),
            cast(Campaign.style_data, JSON).label('logo'),
            cast(Campaign.style_class, String).label('style_class'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            Offer.price,
            func.recommended_to_json(Offer.recommended,
                                     Campaign.style_class_recommendet,
                                     Campaign.brending,
                                     Offer.id_cam).label('recommended')
        ]).select_from(
            join(Offer, Campaign, and_(Offer.id_cam == Campaign.id,
                                       Campaign.social == false(),
                                       Campaign.retargeting == false()
                                       ), isouter=False)
        ).where(and_(Campaign.social == false(),
                     Campaign.retargeting == false())
                ).order_by(Offer.rating.desc().nullslast()), is_mat=True)


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
            cast(Campaign.brending, Boolean).label('brending'),
            cast(Campaign.style_data, JSON).label('logo'),
            cast(Campaign.style_class, String).label('style_class'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            Offer.price,
            func.recommended_to_json(Offer.recommended,
                                     Campaign.style_class_recommendet,
                                     Campaign.brending,
                                     Offer.id_cam).label('recommended')
        ]).select_from(
            join(Offer, Campaign, and_(Offer.id_cam == Campaign.id,
                                       Campaign.social == true(),
                                       Campaign.retargeting == false()
                                       ), isouter=False)
        ).where(and_(
            Campaign.social == true(),
            Campaign.retargeting == false())
        ).order_by(Offer.rating.desc().nullslast()),
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
            cast(Campaign.brending, Boolean).label('brending'),
            cast(Campaign.style_data, JSON).label('logo'),
            cast(Campaign.style_class, String).label('style_class'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            Offer.price,
            func.recommended_to_json(Offer.recommended,
                                     Campaign.style_class_recommendet,
                                     Campaign.brending,
                                     Offer.id_cam).label('recommended')
        ]).select_from(
            join(Offer, Campaign, and_(Offer.id_cam == Campaign.id,
                                       Campaign.retargeting == true(),
                                       Campaign.retargeting_type == 'account'
                                       ), isouter=False)
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
            cast(Campaign.brending, Boolean).label('brending'),
            cast(Campaign.style_data, JSON).label('logo'),
            cast(Campaign.style_class, String).label('style_class'),
            Offer.image,
            Offer.description,
            Offer.url,
            Offer.title,
            Offer.price,
            func.recommended_to_json(Offer.recommended,
                                     Campaign.style_class_recommendet,
                                     Campaign.brending,
                                     Offer.id_cam).label('recommended')
        ]).select_from(
            join(Offer, Campaign, and_(Offer.id_cam == Campaign.id,
                                       Campaign.retargeting == true(),
                                       Campaign.retargeting_type == 'offer'
                                       ), isouter=False)
        ).where(and_(Campaign.retargeting == true(), Campaign.retargeting_type == 'offer')),
        is_mat=True)


Index('ix_mv_offer_dynamic_retargeting_id', MVOfferDynamicRetargeting.id, unique=True)
