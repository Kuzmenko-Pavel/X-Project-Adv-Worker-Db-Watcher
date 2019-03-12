# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentCampaignsByGeo(ParentBase):
    __tablename__ = 'campaigns_by_geo'

    id_campaign = Column(ForeignKey('campaigns.id'), primary_key=True)
    id_geo = Column(ForeignKey('geo.id'), primary_key=True)

    campaign = relationship('ParentCampaign', foreign_keys=[id_campaign], uselist=False)
    geo = relationship('ParentGeo', foreign_keys=[id_geo], uselist=False)
