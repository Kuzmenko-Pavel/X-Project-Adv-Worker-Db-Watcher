# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Float, BigInteger
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, UUIDType

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentBlock(ParentBase):
    __tablename__ = 'v_worker_campaign_block_prices'
    id = Column(BigInteger, primary_key=True)
    block_guid = Column(UUIDType(binary=True))
    click_cost = Column(Float)
    impression_cost = Column(Float)
