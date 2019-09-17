# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, ChoiceType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy_utils.functions import get_query_entities
from sqlalchemy import Column, Integer, text, ForeignKey
from sqlalchemy.orm import relationship

from dashboard.libs.choiceTypes import AMQPStatusType, RejectedMessagesOffer, OfferActionType, OfferType
from .__libs__.sql_trigger import Trigger
from .meta import Base
from .__mixins__ import *

force_auto_coercion()
force_instant_defaults()


class OfferManager(object):
    @staticmethod
    def not_moderated(query):
        return query.filter_by(status=OfferActionType.moderation)

    @staticmethod
    def valid(query):
        entities = get_query_entities(query)
        if not entities:
            return query
        cls = entities[0]
        return query.filter(cls.status.notin_([OfferActionType.moderation, OfferActionType.new,
                                               OfferActionType.invalid]))

    @staticmethod
    def invalid(query):
        return query.filter_by(status=OfferActionType.invalid)

    @staticmethod
    def not_feeds(query):
        entities = get_query_entities(query)
        if not entities:
            return query
        cls = entities[0]
        return query.filter(cls.id_feeds.is_(None))

    @staticmethod
    def feeds(query):
        entities = get_query_entities(query)
        if not entities:
            return query
        cls = entities[0]
        return query.filter(cls.id_feeds.isnot(None))


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

    rejected_message = Column(ChoiceType(RejectedMessagesOffer, impl=Integer()), default=RejectedMessagesOffer.none,
                              server_default=text("'" + str(RejectedMessagesOffer.none.value) + "'::integer"),
                              nullable=False)
    status = Column(ChoiceType(OfferActionType, impl=Integer()), default=OfferActionType.new,
                    server_default=text("'" + str(OfferActionType.new.value) + "'::integer"), nullable=False)

    offer_type = Column(ChoiceType(OfferType, impl=Integer()), default=OfferType.teaser,
                        server_default=text("'" + str(OfferType.teaser.value) + "'::integer"),
                        nullable=False)


class Offer(PrimaryKey, GUID, HASH, Timestamp, StatisticDimensionUpdate, OfferAbstract, Base):
    __tablename__ = 'offers'
    __manager__ = OfferManager
    __table_args__ = (
        Trigger(name='auto_moderation_call',
                event='INSERT OR UPDATE',
                function='auto_moderation_call()',
                before=False,
                for_row=True
                ),
        Trigger(name='zzz_send_worker_amqp',
                event='UPDATE',
                function='send_worker_amqp()',
                before=True,
                for_row=True,
                comment='Отправляет amqp сообшения рекламным модулям'
                ),
    )
    account = relationship('AdloadCustomer', back_populates='offers', foreign_keys='Offer.id_account', uselist=False)

    body = relationship("OfferBody", back_populates="offer", uselist=False, cascade="all, delete-orphan",
                        passive_deletes=True)

    campaign = relationship('Campaign', back_populates='offers', foreign_keys='Offer.id_campaign', uselist=False)

    statistic = relationship("OfferStatistic", uselist=False, foreign_keys='OfferStatistic.id',
                             cascade="all, delete-orphan",
                             primaryjoin='Offer.id == OfferStatistic.id')

    feed = relationship('Feed', backref='offers', foreign_keys='Offer.id_feeds', uselist=False)

    images = relationship("OfferByImages", uselist=True,
                          collection_class=set, back_populates="offer", cascade="all, delete-orphan",
                          passive_deletes=True)

    adv_categories = relationship("OfferByAdvCategories", uselist=True,
                                  collection_class=set,
                                  cascade="all, delete-orphan",
                                  foreign_keys='OfferByAdvCategories.id_offer',
                                  primaryjoin='Offer.id == OfferByAdvCategories.id_offer')
