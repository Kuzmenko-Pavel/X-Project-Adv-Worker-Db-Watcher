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
    id = Column(ForeignKey('campaigns.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    campaign = relationship('Campaign', foreign_keys=[id], uselist=False)
    monday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    tuesday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    wednesday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    thursday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    friday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    saturday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
    sunday = Column(ARRAY(Integer), default=[0, 720, 720, 1440], server_default='{0, 720, 720, 1440}')
