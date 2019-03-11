# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType, ChoiceType

from .choiceTypes import AMQPStatusType
from .meta import ParentBase


class Site(ParentBase):
    __tablename__ = 'sites'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(ForeignKey('accounts.id'), index=True)
    url = Column(URLType)
    name = Column(String)
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))
    account = relationship('Account', back_populates='sites', foreign_keys='Site.id_account', uselist=False)
    blocks = relationship("Block", back_populates="site", collection_class=set, cascade="all", uselist=True)
    pricing = relationship("SitePricing", back_populates="site", foreign_keys='SitePricing.id', uselist=False)

    categories_block_adv = relationship("SiteByBlockingAdvCategory", uselist=True,
                                        foreign_keys='SiteByBlockingAdvCategory.id_site',
                                        primaryjoin='Site.id == SiteByBlockingAdvCategory.id_site')
