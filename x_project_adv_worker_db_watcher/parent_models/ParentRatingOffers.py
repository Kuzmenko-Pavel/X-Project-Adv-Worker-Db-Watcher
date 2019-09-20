# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Float, BigInteger
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentRatingOffer(ParentBase):
    __tablename__ = 'v_worker_rating_offers'
    id_offer = Column(BigInteger, primary_key=True)
    id_block = Column(BigInteger, primary_key=True)
    rating = Column(Float(precision=4))
