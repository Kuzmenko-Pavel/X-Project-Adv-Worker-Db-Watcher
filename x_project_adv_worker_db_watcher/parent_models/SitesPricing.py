# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, Float, Integer, ForeignKey)
from sqlalchemy.orm import relationship

from .meta import ParentBase


class SitePricing(ParentBase):
    __tablename__ = 'sites_pricing'
    id = Column(ForeignKey('sites.id'), primary_key=True)
    site = relationship('Site', foreign_keys=[id], uselist=False)
    click_cost_min = Column(Float)
    click_cost_proportion = Column(Integer)
    click_cost_max = Column(Float)
    impression_cost_min = Column(Float)
    impression_cost_proportion = Column(Integer)
    impression_cost_max = Column(Float)
