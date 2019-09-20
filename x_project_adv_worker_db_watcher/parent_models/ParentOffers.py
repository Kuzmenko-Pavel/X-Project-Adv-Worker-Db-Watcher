# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, String, Integer, BigInteger, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, ChoiceType, URLType, LtreeType
from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignRemarketingType,
                                                         CampaignStylingType, CurrencyType)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentOffer(ParentBase):
    __tablename__ = 'v_worker_offers'
    id = Column(BigInteger, primary_key=True)
    id_campaign = Column(BigInteger)
    id_account = Column(BigInteger)
    title = Column(String)
    description = Column(String)
    url = Column(URLType)
    price = Column(String)
    currency = Column(ChoiceType(CurrencyType, impl=Integer()))
    id_retargeting = Column(Text)
    recommended = Column(ARRAY(BigInteger))
    images = Column(ARRAY(URLType))
    categories = Column(ARRAY(LtreeType))
    campaign_type = Column(ChoiceType(CampaignType, impl=Integer()))
    campaign_style = Column(ChoiceType(CampaignStylingType, impl=Integer()))
    remarketing_type = Column(ChoiceType(CampaignRemarketingType, impl=Integer()))