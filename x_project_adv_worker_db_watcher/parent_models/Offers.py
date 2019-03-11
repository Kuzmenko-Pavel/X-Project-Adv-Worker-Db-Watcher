# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy_utils import ChoiceType
from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from .choiceTypes import AMQPStatusType, OfferType
from .meta import ParentBase


class Offer(ParentBase):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(ForeignKey('accounts.id'), index=True)
    id_campaign = Column(ForeignKey('campaigns.id'), index=True)

    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))

    offer_type = Column(ChoiceType(OfferType, impl=Integer()))
    account = relationship('Account', back_populates='offers', foreign_keys='Offer.id_account', uselist=False)

    body = relationship("OfferBody", back_populates="offer", uselist=False)

    campaign = relationship('Campaign', back_populates='offers', foreign_keys='Offer.id_campaign', uselist=False)

    images = relationship("OfferByImages", uselist=True, back_populates="offer")

    adv_categories = relationship("OfferByAdvCategories", uselist=True,
                                  foreign_keys='OfferByAdvCategories.id_offer',
                                  primaryjoin='Offer.id == OfferByAdvCategories.id_offer')
