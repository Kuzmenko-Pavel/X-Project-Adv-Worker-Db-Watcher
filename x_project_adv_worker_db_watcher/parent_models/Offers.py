# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy_utils import ChoiceType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, text, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from .choiceTypes import AMQPStatusType, OfferType
from .meta import ParentBase


class OfferAbstract(object):

    @declared_attr
    def id_account(cls):
        return Column(ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False, index=True)

    @declared_attr
    def id_campaign(cls):
        return Column(ForeignKey('campaigns.id', ondelete="SET NULL"), nullable=True, index=True)

    @declared_attr
    def id_feeds(cls):
        return Column(ForeignKey('feeds.id', ondelete="CASCADE"), nullable=True, index=True)

    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()), default=AMQPStatusType.new,
                         server_default=text("'" + str(AMQPStatusType.new.value) + "'::integer"), nullable=False)

    offer_type = Column(ChoiceType(OfferType, impl=Integer()), default=OfferType.teaser,
                        server_default=text("'" + str(OfferType.teaser.value) + "'::integer"),
                        nullable=False)


class Offer(OfferAbstract, ParentBase):
    __tablename__ = 'offers'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account = relationship('Account', back_populates='offers', foreign_keys='Offer.id_account', uselist=False)

    body = relationship("OfferBody", back_populates="offer", uselist=False, cascade="all, delete-orphan",
                        passive_deletes=True)

    campaign = relationship('Campaign', back_populates='offers', foreign_keys='Offer.id_campaign', uselist=False)

    images = relationship("OfferByImages", uselist=True,
                          collection_class=set, back_populates="offer", cascade="all, delete-orphan",
                          passive_deletes=True)

    adv_categories = relationship("OfferByAdvCategories", uselist=True,
                                  collection_class=set,
                                  cascade="all, delete-orphan",
                                  foreign_keys='OfferByAdvCategories.id_offer',
                                  primaryjoin='Offer.id == OfferByAdvCategories.id_offer')
