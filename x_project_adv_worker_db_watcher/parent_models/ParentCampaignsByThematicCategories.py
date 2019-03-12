# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentCampaignByThematicCategories(ParentBase):
    __tablename__ = 'campaigns_by_thematic_categories'

    id_campaign = Column(ForeignKey('campaigns.id'), primary_key=True)

    id_adv_category = Column(ForeignKey('adv_categories.id'), primary_key=True)

    campaign = relationship('ParentCampaign', foreign_keys=[id_campaign], uselist=False)

    thematic_category = relationship('ParentAdvCategory', foreign_keys=[id_adv_category], uselist=False)
