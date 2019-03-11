# -*- coding: utf-8 -*-
__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey, String, ARRAY)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults, URLType)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class OfferBody(ParentBase):
    __tablename__ = 'offers_body'

    id = Column(ForeignKey('offers.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    offer = relationship('Offer', back_populates='body', foreign_keys=[id], uselist=False)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    currency = Column(String)
    url = Column(URLType)
    recommended = Column(ARRAY(String), nullable=True)
    id_retargeting = Column(String, nullable=True, index=True)


__all__ = [OfferBody]
