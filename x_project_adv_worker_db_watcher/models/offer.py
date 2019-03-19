__all__ = ['Offer', 'MVOfferPlace', 'MVOfferSocial', 'MVOfferAccountRetargeting', 'MVOfferDynamicRetargeting']
from sqlalchemy import (Column, BigInteger, String, Float, ForeignKey, select, Index, cast)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import func, join, true, false, and_

from .__libs__.sql_view import create_view
from .campaign import Campaign
from .meta import Base


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True), unique=True)
    retid = Column(String, default='')
    campaign = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    images = Column(ARRAY(String), default=[])
    description = Column(String(length=70))
    url = Column(String)
    title = Column(String(length=35))
    price = Column(String(length=35))
    rating = Column(Float)
    recommended_ids = Column(ARRAY(String), default=[])
    recommended = Column(ARRAY(BigInteger), default=[])
    __table_args__ = (
        Index('ix_offer_rating', rating.desc().nullslast()),
        Index('ix_offer_retid_campaign', retid, campaign.desc().nullslast()),
        {'prefixes': ['UNLOGGED']}
    )


place_sub = select([
    func.row_number().over(partition_by=Offer.campaign).label('campaign_range_number'),
    Offer.id,
    Offer.guid,
    Offer.campaign,
    Offer.images,
    Offer.description,
    Offer.url,
    Offer.title,
    Offer.price,
    Offer.recommended
]).select_from(
    join(Offer, Campaign, and_(Offer.campaign == Campaign.id,
                               Campaign.social == false(),
                               Campaign.retargeting == false()
                               ), isouter=False)
).where(and_(Campaign.social == false(),
             Campaign.retargeting == false())
        ).order_by(Offer.rating.desc().nullslast()).alias('place_sub')

social_sub = select([
    func.row_number().over(partition_by=Offer.campaign).label('campaign_range_number'),
    Offer.id,
    Offer.guid,
    Offer.campaign,
    Offer.images,
    Offer.description,
    Offer.url,
    Offer.title,
    Offer.price,
    Offer.recommended
]).select_from(
    join(Offer, Campaign, and_(Offer.campaign == Campaign.id,
                               Campaign.social == true(),
                               Campaign.retargeting == false()
                               ), isouter=False)
).where(and_(
    Campaign.social == true(),
    Campaign.retargeting == false())
).order_by(Offer.rating.desc().nullslast()).alias('social_sub')

account_retargeting_sub = select([
    func.row_number().over(partition_by=Offer.campaign).label('campaign_range_number'),
    Offer.id,
    Offer.guid,
    Offer.campaign,
    Offer.images,
    Offer.description,
    Offer.url,
    Offer.title,
    Offer.price,
    Offer.recommended
]).select_from(
    join(Offer, Campaign, and_(Offer.campaign == Campaign.id,
                               Campaign.retargeting == true(),
                               Campaign.retargeting_type == 'account'
                               ), isouter=False)
).where(and_(Campaign.retargeting == true(), Campaign.retargeting_type == 'account')).alias('account_retargeting_sub')


class MVOfferPlace(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_place',
        select([
            place_sub.c.id,
            place_sub.c.guid,
            place_sub.c.campaign,
            place_sub.c.images,
            place_sub.c.description,
            place_sub.c.url,
            place_sub.c.title,
            place_sub.c.price,
            place_sub.c.recommended,
            place_sub.c.campaign_range_number
        ]).select_from(place_sub), is_mat=True)


Index('ix_mv_offer_place_id', MVOfferPlace.id, unique=True)
Index('ix_mv_offer_place_campaign_range_number', MVOfferPlace.campaign, MVOfferPlace.campaign_range_number)


class MVOfferSocial(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social',
        select([
            social_sub.c.id,
            social_sub.c.guid,
            social_sub.c.campaign,
            social_sub.c.images,
            social_sub.c.description,
            social_sub.c.url,
            social_sub.c.title,
            social_sub.c.price,
            social_sub.c.recommended,
            social_sub.c.campaign_range_number
        ]).select_from(social_sub), is_mat=True)


Index('ix_mv_offer_social_id', MVOfferSocial.id, unique=True)
Index('ix_mv_offer_social_campaign_range_number', MVOfferSocial.campaign, MVOfferSocial.campaign_range_number)


class MVOfferAccountRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_account_retargeting',
        select([
            account_retargeting_sub.c.id,
            account_retargeting_sub.c.guid,
            account_retargeting_sub.c.campaign,
            account_retargeting_sub.c.images,
            account_retargeting_sub.c.description,
            account_retargeting_sub.c.url,
            account_retargeting_sub.c.title,
            account_retargeting_sub.c.price,
            account_retargeting_sub.c.recommended,
            account_retargeting_sub.c.campaign_range_number
        ]).select_from(account_retargeting_sub), is_mat=True)


Index('ix_mv_offer_account_retargeting_id', MVOfferAccountRetargeting.id, unique=True)
Index('ix_mv_offer_account_retargeting_campaign_range_number', MVOfferAccountRetargeting.campaign,
      MVOfferAccountRetargeting.campaign_range_number)


class MVOfferDynamicRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_dynamic_retargeting',
        select([
            Offer.id,
            Offer.guid,
            Offer.retid,
            Offer.campaign,
            cast(Campaign.account, String).label('accounts_cam'),
            Offer.images,
            Offer.description,
            Offer.url,
            Offer.title,
            Offer.price,
            Offer.recommended
        ]).select_from(
            join(Offer, Campaign, and_(Offer.campaign == Campaign.id,
                                       Campaign.retargeting == true(),
                                       Campaign.retargeting_type == 'offer'
                                       ), isouter=False)
        ).where(and_(Campaign.retargeting == true(), Campaign.retargeting_type == 'offer')),
        is_mat=True)


Index('ix_mv_offer_dynamic_retargeting_id', MVOfferDynamicRetargeting.id, unique=True)
Index('ix_mv_offer_dynamic_retargeting_retid_accounts_cam', MVOfferDynamicRetargeting.retid,
      MVOfferDynamicRetargeting.accounts_cam)
