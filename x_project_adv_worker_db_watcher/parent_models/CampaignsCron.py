# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey, Integer)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class CampaignCron(ParentBase):
    __tablename__ = 'campaigns_cron'
    id = Column(ForeignKey('campaigns.id'), primary_key=True)
    campaign = relationship('Campaign', foreign_keys=[id], uselist=False)
    monday = Column(ARRAY(Integer))
    tuesday = Column(ARRAY(Integer))
    wednesday = Column(ARRAY(Integer))
    thursday = Column(ARRAY(Integer))
    friday = Column(ARRAY(Integer))
    saturday = Column(ARRAY(Integer))
    sunday = Column(ARRAY(Integer))
