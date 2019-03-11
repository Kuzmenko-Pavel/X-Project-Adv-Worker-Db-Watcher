# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class CampaignByDevices(ParentBase):
    __tablename__ = 'campaigns_by_devices'

    id_campaign = Column(ForeignKey('campaigns.id'), primary_key=True)
    id_device = Column(ForeignKey('devices.id'), primary_key=True)

    campaign = relationship('Campaign', foreign_keys=[id_campaign], uselist=False)
    device = relationship('Device', foreign_keys=[id_device], uselist=False)
