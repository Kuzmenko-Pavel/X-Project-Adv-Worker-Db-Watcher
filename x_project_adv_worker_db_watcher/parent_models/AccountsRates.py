# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, Float, Integer, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class AccountRates(ParentBase):
    __tablename__ = 'accounts_rates'
    id = Column(ForeignKey('accounts.id'), primary_key=True, nullable=False)
    account = relationship('Account', foreign_keys=[id], uselist=False)
    click_cost_min = Column(Float, default=0.1)
    click_cost_proportion = Column(Integer, default=50)
    click_cost_recommended = Column(Float, default=0.1)
    click_cost_max = Column(Float, default=100)
    impression_cost_min = Column(Float, default=0.1)
    impression_cost_proportion = Column(Integer, default=50)
    impression_cost_recommended = Column(Float, default=0.1)
    impression_cost_max = Column(Float, default=100)
