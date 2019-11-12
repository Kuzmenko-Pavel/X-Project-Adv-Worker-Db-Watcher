__all__ = ['Offer', 'MVOfferPlace', 'MVOfferSocial', 'MVOfferAccountRetargeting', 'MVOfferDynamicRetargeting']
from sqlalchemy import (Column, BigInteger, String, Text, ForeignKey, select, Index, Integer)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql.expression import and_
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, ChoiceType, URLType

from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignStylingType, CampaignRemarketingType,
                                                         CurrencyType)
from .__libs__.custom_arrays import ArrayOfCustomType
from .__libs__.sql_view import create_view
from .meta import Base

force_auto_coercion()
force_instant_defaults()


class Offer(Base):
    __tablename__ = 'offer'
    id = Column(BigInteger, primary_key=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False, index=True)
    id_acc = Column(BigInteger, nullable=False, index=True)
    title = Column(String(length=35))
    description = Column(String(length=70))
    url = Column(String)
    price = Column(String(length=35))
    currency = Column(ChoiceType(CurrencyType, impl=Integer()))
    id_ret = Column(Text)
    recommended = Column(ARRAY(BigInteger))
    images = Column(ArrayOfCustomType(URLType))
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()))
    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()))
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()))
    campaign_range_number = Column(Integer)
    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVOfferPlace(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_place',
        select([
            Offer.id,
            Offer.id_cam,
            Offer.id_acc,
            Offer.title,
            Offer.description,
            Offer.url,
            Offer.price,
            Offer.currency,
            Offer.recommended,
            Offer.images,
            Offer.campaign_range_number,
        ]).select_from(Offer).where(
            and_(Offer.campaign_type.in_([CampaignType.new_auditory, CampaignType.thematic]))
        ), is_mat=True)


Index('ix_mv_offer_place_id', MVOfferPlace.id, unique=True)
Index('ix_mv_offer_place_id_id_cam_range_number',
      MVOfferPlace.id,
      MVOfferPlace.id_cam,
      MVOfferPlace.campaign_range_number)

Index('ix_mv_offer_place_id_cam', MVOfferPlace.id_cam, )

class MVOfferSocial(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social',
        select([
            Offer.id,
            Offer.id_cam,
            Offer.id_acc,
            Offer.title,
            Offer.description,
            Offer.url,
            Offer.price,
            Offer.currency,
            Offer.recommended,
            Offer.images,
            Offer.campaign_range_number,
        ]).select_from(Offer).where(
            and_(Offer.campaign_type == CampaignType.social)
        ), is_mat=True)


Index('ix_mv_offer_social_id', MVOfferSocial.id, unique=True)
Index('ix_mv_offer_social_id_id_cam_range_number',
      MVOfferSocial.id,
      MVOfferSocial.id_cam,
      MVOfferSocial.campaign_range_number)

Index('ix_mv_offer_social_id_cam', MVOfferSocial.id_cam)


class MVOfferAccountRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_account_retargeting',
        select([
            Offer.id,
            Offer.id_cam,
            Offer.id_acc,
            Offer.title,
            Offer.description,
            Offer.url,
            Offer.price,
            Offer.currency,
            Offer.recommended,
            Offer.images,
            Offer.campaign_range_number,
        ]).select_from(Offer).where(
            and_(Offer.campaign_type == CampaignType.remarketing,
                 Offer.remarketing_type == CampaignRemarketingType.account)
        ), is_mat=True)


Index('ix_mv_offer_account_retargeting_id', MVOfferAccountRetargeting.id, unique=True)
Index('ix_mv_offer_account_retargeting_id_id_cam_range_number',
      MVOfferAccountRetargeting.id,
      MVOfferAccountRetargeting.id_cam,
      MVOfferAccountRetargeting.campaign_range_number)

Index('ix_mv_offer_account_retargeting_id_cam', MVOfferAccountRetargeting.id_cam)


class MVOfferDynamicRetargeting(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_dynamic_retargeting',
        select([
            Offer.id,
            Offer.id_cam,
            Offer.id_acc,
            Offer.title,
            Offer.description,
            Offer.url,
            Offer.price,
            Offer.currency,
            Offer.recommended,
            Offer.images,
            Offer.id_ret,
            Offer.campaign_range_number,
        ]).select_from(Offer).where(
            and_(Offer.campaign_type == CampaignType.remarketing,
                 Offer.remarketing_type == CampaignRemarketingType.offer)
        ),
        is_mat=True)


Index('ix_mv_offer_dynamic_retargeting_id', MVOfferDynamicRetargeting.id, unique=True)
Index('ix_mv_offer_dynamic_retargeting_id_ret', MVOfferDynamicRetargeting.id_ret)
