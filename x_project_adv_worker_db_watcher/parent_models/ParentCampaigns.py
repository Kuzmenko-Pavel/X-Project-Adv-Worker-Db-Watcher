# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, ForeignKey, String, Integer, text, Boolean, SmallInteger, false, true
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults, ChoiceType)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from dashboard.libs.choiceTypes import (AMQPStatusType, CampaignActionType, CampaignType, CampaignStylingType,
                                        CampaignRemarketingType, CampaignRecommendedAlgorithmType, CampaignPaymentModel)
from .__libs__.sql_trigger import Trigger
from .meta import Base
from .__mixins__ import *

force_auto_coercion()
force_instant_defaults()


class CampaignAbstract(object):
    @declared_attr
    def id_account(cls):
        return Column(ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String, default="")

    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()), default=AMQPStatusType.new,
                         server_default=text("'" + str(AMQPStatusType.new.value) + "'::integer"), nullable=False)

    status = Column(ChoiceType(CampaignActionType, impl=Integer()), default=CampaignActionType.new,
                    server_default=text("'" + str(CampaignActionType.new.value) + "'::integer"), nullable=False)

    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()), default=CampaignType.new_auditory,
                           server_default=text("'" + str(CampaignType.new_auditory.value) + "'::integer"),
                           nullable=False)

    payment_model = Column(ChoiceType(CampaignPaymentModel, impl=Integer()), default=CampaignPaymentModel.ppc,
                           server_default=text("'" + str(CampaignPaymentModel.ppc.value) + "'::integer"),
                           nullable=False)

    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()), default=CampaignStylingType.dynamic,
                            server_default=text("'" + str(CampaignStylingType.dynamic.value) + "'::integer"),
                            nullable=False)

    campaign_style_logo = Column(String, default="", server_default=text("''"))

    campaign_style_head_title = Column(String, default="", server_default=text("''"))

    campaign_style_button_title = Column(String, default="", server_default=text("''"))

    utm = Column(Boolean, default=True, server_default=true())

    utm_human_data = Column(Boolean, default=False, server_default=false())
    disable_filter = Column(Boolean, default=False, server_default=false())
    time_filter = Column(Integer, default=0, server_default="0")

    auto_run = Column(Boolean, default=True, server_default=true())

    unique_impression_lot = Column(SmallInteger, default=1, server_default='1')

    lot_concurrency = Column(SmallInteger, default=1, server_default='1')

    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()),
                              default=CampaignRemarketingType.offer,
                              server_default=text("'" + str(CampaignRemarketingType.offer.value) + "'::integer"),
                              nullable=False)

    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()),
                                   default=CampaignRecommendedAlgorithmType.none,
                                   server_default=text(
                                       "'" + str(CampaignRecommendedAlgorithmType.none.value) + "'::integer"),
                                   nullable=False)

    recommended_count = Column(SmallInteger, default=1, server_default='1')

    extended_settings = Column(Boolean, default=False, server_default=false())

    thematic_day_new_auditory = Column(SmallInteger, default=10, server_default='10')
    thematic_day_off_new_auditory = Column(SmallInteger, default=10, server_default='10')


class Campaign(PrimaryKey, GUID, Timestamp, StatisticDimensionUpdate, CampaignAbstract, Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        Trigger(name='zzz_send_worker_amqp',
                event='UPDATE',
                function='send_worker_amqp()',
                before=True,
                for_row=True,
                comment='Отправляет amqp сообшения рекламным модулям'
                ),
    )

    account = relationship('AdloadCustomer', back_populates='campaigns', foreign_keys='Campaign.id_account',
                           uselist=False)

    offers = relationship("Offer", collection_class=set, back_populates="campaign", cascade="all")

    statistic = relationship("CampaignStatistic", uselist=False, cascade="all, delete-orphan",
                             foreign_keys='CampaignStatistic.id', primaryjoin='Campaign.id == CampaignStatistic.id')

    statistic_array = relationship("CampaignStatisticArray", uselist=False, cascade="all, delete-orphan",
                                   foreign_keys='CampaignStatisticArray.id',
                                   primaryjoin='Campaign.id == CampaignStatisticArray.id')

    feeds = relationship("Feed", collection_class=set, back_populates="campaign", cascade="all")

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

    pricing = relationship("CampaignPricing", back_populates="campaign", foreign_keys='CampaignPricing.id',
                           uselist=False)
