# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, Float, Integer, ForeignKey)
from sqlalchemy.orm import relationship

from .meta import ParentBase


class SitePricing(ParentBase):
    __tablename__ = 'sites_pricing'
    id = Column(ForeignKey('sites.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    site = relationship('Site', foreign_keys=[id], uselist=False)
    click_cost_min = Column(Float, default=0.1)
    click_cost_proportion = Column(Integer, default=50)
    click_cost_max = Column(Float, default=100)
    impression_cost_min = Column(Float, default=0.1)
    impression_cost_proportion = Column(Integer, default=50)
    impression_cost_max = Column(Float, default=100)
