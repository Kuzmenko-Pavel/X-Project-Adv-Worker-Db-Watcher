# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Integer, BigInteger, SmallInteger, String, Boolean, Float
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, ChoiceType, UUIDType, LtreeType
from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignPaymentModel, CampaignRemarketingType,
                                                         CampaignRecommendedAlgorithmType, CampaignStylingType)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentCampaign(ParentBase):
    __tablename__ = 'v_worker_campaigns'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(BigInteger)
    guid = Column(UUIDType(binary=True))
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()))
    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()))
    campaign_style_logo = Column(String)
    campaign_style_head_title = Column(String)
    campaign_style_button_title = Column(String)
    utm = Column(Boolean)
    utm_human_data = Column(Boolean)
    disable_filter = Column(Boolean)
    time_filter = Column(Integer)
    payment_model = Column(ChoiceType(CampaignPaymentModel, impl=Integer()))
    lot_concurrency = Column(SmallInteger)
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()))
    recommended_algorithm = Column(ChoiceType(CampaignRecommendedAlgorithmType, impl=Integer()))
    recommended_count = Column(SmallInteger)
    thematic_day_new_auditory = Column(SmallInteger)
    thematic_day_off_new_auditory = Column(SmallInteger)
    offer_count = Column(ARRAY(BigInteger))
    blocking_block = Column(ARRAY(BigInteger))
    thematic_categories = Column(ARRAY(LtreeType))
    geo = Column(ARRAY(BigInteger))
    device = Column(ARRAY(BigInteger))
    cron = Column(JSON)
    click_cost = Column(Float)
    impression_cost = Column(Float)
