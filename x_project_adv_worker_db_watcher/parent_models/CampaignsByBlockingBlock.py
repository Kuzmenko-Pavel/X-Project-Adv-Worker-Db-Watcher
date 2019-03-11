# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class CampaignByBlockingBlock(ParentBase):
    __tablename__ = 'campaigns_by_blocking_block'

    id_campaign = Column(ForeignKey('campaigns.id'), primary_key=True)
    id_block = Column(ForeignKey('blocks.id'), primary_key=True)

    campaign = relationship('Campaign', foreign_keys=[id_campaign], uselist=False)
    block = relationship('Block', foreign_keys=[id_block], uselist=False)
