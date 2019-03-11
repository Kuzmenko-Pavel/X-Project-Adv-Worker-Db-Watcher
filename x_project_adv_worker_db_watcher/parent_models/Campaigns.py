# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, ForeignKey, String, Integer, Float, text, Boolean, SmallInteger, BigInteger
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .choiceTypes import (AMQPStatusType, CampaignType, CampaignStylingType,
                          CampaignRemarketingType, CampaignRecommendedAlgorithmType)
from .meta import ParentBase


class CampaignAbstract(object):
    @declared_attr
    def id_account(cls):
        return Column(ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String, default="")

    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()), default=AMQPStatusType.new,
                         server_default=text("'" + str(AMQPStatusType.new.value) + "'::integer"), nullable=False)

    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()), default=CampaignType.new_auditory,
                           server_default=text("'" + str(CampaignType.new_auditory.value) + "'::integer"),
                           nullable=False)

    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()), default=CampaignStylingType.dynamic,
                            server_default=text("'" + str(CampaignStylingType.dynamic.value) + "'::integer"),
                            nullable=False)

    campaign_style_logo = Column(String, default="")

    campaign_style_head_title = Column(String, default="")

    campaign_style_button_title = Column(String, default="")

    utm = Column(Boolean, default=True)

    auto_run = Column(Boolean, default=True)

    unique_impression_lot = Column(SmallInteger, default=1, server_default='1', nullable=False)

    lot_concurrency = Column(SmallInteger, default=1, server_default='1', nullable=False)

    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()),
                              default=CampaignRemarketingType.offer,
                              server_default=text("'" + str(CampaignRemarketingType.offer.value) + "'::integer"),
                              nullable=False)

    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()),
                                   default=CampaignRecommendedAlgorithmType.none,
                                   server_default=text(
                                       "'" + str(CampaignRecommendedAlgorithmType.none.value) + "'::integer"),
                                   nullable=False)

    recommended_count = Column(SmallInteger, default=1, server_default='1', nullable=False)

    click_cost = Column(Float)

    impression_cost = Column(Float)

    day_budget = Column(Float, nullable=True)

    monthly_budget = Column(Float, nullable=True)


class Campaign(CampaignAbstract, ParentBase):
    __tablename__ = 'campaigns'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account = relationship('Account', back_populates='campaigns', foreign_keys='Campaign.id_account',
                           uselist=False)

    offers = relationship("Offer", collection_class=set, back_populates="campaign", cascade="all")

    thematic_categories = relationship("CampaignByThematicCategories", uselist=True,
                                       collection_class=set,
                                       cascade="all, delete-orphan",
                                       foreign_keys='CampaignByThematicCategories.id_campaign',
                                       primaryjoin='Campaign.id == CampaignByThematicCategories.id_campaign')

    blocks_blocking = relationship("CampaignByBlockingBlock", uselist=True,
                                   collection_class=set,
                                   cascade="all, delete-orphan",
                                   foreign_keys='CampaignByBlockingBlock.id_campaign',
                                   primaryjoin='Campaign.id == CampaignByBlockingBlock.id_campaign')

    geos = relationship("CampaignsByGeo", uselist=True,
                        collection_class=set,
                        cascade="all, delete-orphan",
                        foreign_keys='CampaignsByGeo.id_campaign',
                        primaryjoin='Campaign.id == CampaignsByGeo.id_campaign')

    devices = relationship("CampaignByDevices", uselist=True,
                           collection_class=set,
                           cascade="all, delete-orphan",
                           foreign_keys='CampaignByDevices.id_campaign',
                           primaryjoin='Campaign.id == CampaignByDevices.id_campaign')

    cron = relationship("CampaignCron", uselist=False,
                        cascade="all, delete-orphan",
                        foreign_keys='CampaignCron.id', primaryjoin='Campaign.id == CampaignCron.id')
