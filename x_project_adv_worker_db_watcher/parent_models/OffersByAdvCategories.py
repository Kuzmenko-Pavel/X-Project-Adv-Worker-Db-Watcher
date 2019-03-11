# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class OfferByAdvCategories(ParentBase):
    __tablename__ = 'offers_by_adv_categories'
    id_offer = Column(ForeignKey('offers.id'), primary_key=True)
    id_adv_category = Column(ForeignKey('adv_categories.id'), primary_key=True)
    offer = relationship('Offer', foreign_keys=[id_offer], uselist=False)
    adv_category = relationship('AdvCategory', foreign_keys=[id_adv_category], uselist=False)
