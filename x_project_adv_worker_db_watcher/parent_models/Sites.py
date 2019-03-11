# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Integer, text, String, ForeignKey, Boolean, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType, ChoiceType
from sqlalchemy.ext.declarative import declared_attr

from .choiceTypes import AMQPStatusType
from .meta import ParentBase


class SiteAbstract(object):
    @declared_attr
    def id_account(cls):
        return Column(ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False, index=True)

    url = Column(URLType, index=True)
    name = Column(String, index=True, unique=True)
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()), default=AMQPStatusType.new,
                         server_default=text("'" + str(AMQPStatusType.new.value) + "'::integer"), nullable=False)


class Site(SiteAbstract, ParentBase):
    __tablename__ = 'sites'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    account = relationship('Account', back_populates='sites', foreign_keys='Site.id_account', uselist=False)
    blocks = relationship("Block", back_populates="site", collection_class=set, cascade="all", uselist=True)
    pricing = relationship("SitePricing", back_populates="site", foreign_keys='SitePricing.id', uselist=False)

    categories_block_adv = relationship("SiteByBlockingAdvCategory", uselist=True,
                                        collection_class=set,
                                        cascade="all, delete-orphan",
                                        foreign_keys='SiteByBlockingAdvCategory.id_site',
                                        primaryjoin='Site.id == SiteByBlockingAdvCategory.id_site')
