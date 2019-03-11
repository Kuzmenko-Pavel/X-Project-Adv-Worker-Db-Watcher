# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class OfferByAdvCategories(ParentBase):
    __tablename__ = 'offers_by_adv_categories'

    id_offer = Column(ForeignKey('offers.id', ondelete="CASCADE"), primary_key=True, nullable=False)

    id_adv_category = Column(ForeignKey('adv_categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    offer = relationship('Offer', foreign_keys=[id_offer], uselist=False, passive_deletes=True)

    adv_category = relationship('AdvCategory', foreign_keys=[id_adv_category], uselist=False, passive_deletes=True)

    @hybrid_property
    def adv_category_name(self):
        return self.adv_category.name

    def __hash__(self):
        return hash((self.id_offer, self.id_adv_category, self.offer, self.adv_category))

    def __eq__(self, other):
        return all([getattr(self, x) == getattr(other, x) for x in
                    ['id_offer', 'id_adv_category', 'offer', 'adv_category']])
