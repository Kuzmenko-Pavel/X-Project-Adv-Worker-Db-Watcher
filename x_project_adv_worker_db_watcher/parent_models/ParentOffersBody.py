# -*- coding: utf-8 -*-
__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey, String, ARRAY)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults, URLType)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentOfferBody(ParentBase):
    __tablename__ = 'offers_body'

    id = Column(ForeignKey('offers.id'), primary_key=True)
    offer = relationship('ParentOffer', back_populates='body', foreign_keys=[id], uselist=False)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    currency = Column(String)
    url = Column(URLType)
    recommended = Column(ARRAY(String))
    id_retargeting = Column(String)
