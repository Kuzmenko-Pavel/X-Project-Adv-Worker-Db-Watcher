# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class CampaignByBlockingBlock(ParentBase):
    __tablename__ = 'campaigns_by_blocking_block'

    id_campaign = Column(ForeignKey('campaigns.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_block = Column(ForeignKey('blocks.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    campaign = relationship('Campaign', foreign_keys=[id_campaign], uselist=False, passive_deletes=True)
    block = relationship('Block', foreign_keys=[id_block], uselist=False, passive_deletes=True)

    @hybrid_property
    def campaign_name(self):
        return self.campaign.name

    @hybrid_property
    def block_guid(self):
        return self.block.guid

    def __hash__(self):
        return hash((self.id_campaign, self.id_block, self.campaign, self.block))

    def __eq__(self, other):
        return all([getattr(self, x) == getattr(other, x) for x in
                    ['id_campaign', 'id_block', 'campaign', 'block']])
