# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class CampaignByThematicCategories(ParentBase):
    __tablename__ = 'campaigns_by_thematic_categories'

    id_campaign = Column(ForeignKey('campaigns.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    id_adv_category = Column(ForeignKey('adv_categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    campaign = relationship('Campaign', foreign_keys=[id_campaign], uselist=False, passive_deletes=True)

    thematic_category = relationship('AdvCategory', foreign_keys=[id_adv_category], uselist=False, passive_deletes=True)

    @hybrid_property
    def campaign_name(self):
        return self.campaign.name

    @hybrid_property
    def thematic_category_name(self):
        return self.thematic_category.name

    def __hash__(self):
        return hash((self.id_campaign, self.id_adv_category, self.campaign, self.thematic_category))

    def __eq__(self, other):
        return all([getattr(self, x) == getattr(other, x) for x in
                    ['id_campaign', 'id_adv_category', 'campaign', 'thematic_category']])
