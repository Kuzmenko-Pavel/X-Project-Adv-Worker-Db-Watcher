# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, ForeignKey, String, Integer, Float, Boolean, SmallInteger, BigInteger
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

from .choiceTypes import (AMQPStatusType, CampaignType, CampaignStylingType,
                          CampaignRemarketingType, CampaignRecommendedAlgorithmType)
from .meta import ParentBase


class ParentCampaign(ParentBase):
    __tablename__ = 'campaigns'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(ForeignKey('accounts.id'), index=True)
    name = Column(String)
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()))
    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()))
    campaign_style_logo = Column(String)
    campaign_style_head_title = Column(String)
    campaign_style_button_title = Column(String)
    utm = Column(Boolean)
    auto_run = Column(Boolean)
    unique_impression_lot = Column(SmallInteger)
    lot_concurrency = Column(SmallInteger)
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()))
    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()))
    recommended_count = Column(SmallInteger)
    click_cost = Column(Float)
    impression_cost = Column(Float)
    account = relationship('ParentAccount', back_populates='campaigns', foreign_keys='ParentCampaign.id_account',
                           uselist=False)
    offers = relationship("ParentOffer", back_populates="campaign")
    thematic_categories = relationship("ParentCampaignByThematicCategories", uselist=True,
                                       foreign_keys='ParentCampaignByThematicCategories.id_campaign',
                                       primaryjoin='ParentCampaign.id == ParentCampaignByThematicCategories.id_campaign')
    blocks_blocking = relationship("ParentCampaignByBlockingBlock", uselist=True,
                                   foreign_keys='ParentCampaignByBlockingBlock.id_campaign',
                                   primaryjoin='ParentCampaign.id == ParentCampaignByBlockingBlock.id_campaign')
    geos = relationship("ParentCampaignsByGeo", uselist=True,
                        foreign_keys='ParentCampaignsByGeo.id_campaign',
                        primaryjoin='ParentCampaign.id == ParentCampaignsByGeo.id_campaign')
    devices = relationship("ParentCampaignByDevices", uselist=True,
                           foreign_keys='ParentCampaignByDevices.id_campaign',
                           primaryjoin='ParentCampaign.id == ParentCampaignByDevices.id_campaign')
    cron = relationship("ParentCampaignCron", uselist=False,
                        foreign_keys='ParentCampaignCron.id', primaryjoin='ParentCampaign.id == ParentCampaignCron.id')
