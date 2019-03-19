# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy_utils import UUIDType, ChoiceType
from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from .choiceTypes import AMQPStatusType, OfferType
from .meta import ParentBase


class ParentOffer(ParentBase):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True))
    id_account = Column(ForeignKey('accounts.id'), index=True)
    id_campaign = Column(ForeignKey('campaigns.id'), index=True)

    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))

    offer_type = Column(ChoiceType(OfferType, impl=Integer()))
    account = relationship('ParentAccount', back_populates='offers', foreign_keys='ParentOffer.id_account',
                           uselist=False)

    body = relationship("ParentOfferBody", back_populates="offer", uselist=False)

    campaign = relationship('ParentCampaign', back_populates='offers', foreign_keys='ParentOffer.id_campaign',
                            uselist=False)

    images = relationship("ParentOfferByImages", uselist=True, back_populates="offer")

    adv_categories = relationship("ParentOfferByAdvCategories", uselist=True,
                                  foreign_keys='ParentOfferByAdvCategories.id_offer',
                                  primaryjoin='ParentOffer.id == ParentOfferByAdvCategories.id_offer')
