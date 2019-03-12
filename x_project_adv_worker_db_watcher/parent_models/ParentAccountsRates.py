# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, Float, Integer, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentAccountRates(ParentBase):
    __tablename__ = 'accounts_rates'
    id = Column(ForeignKey('accounts.id'), primary_key=True)
    account = relationship('ParentAccount', foreign_keys=[id], uselist=False)
    click_cost_min = Column(Float)
    click_cost_proportion = Column(Integer)
    click_cost_recommended = Column(Float)
    click_cost_max = Column(Float)
    impression_cost_min = Column(Float)
    impression_cost_proportion = Column(Integer)
    impression_cost_recommended = Column(Float)
    impression_cost_max = Column(Float)
