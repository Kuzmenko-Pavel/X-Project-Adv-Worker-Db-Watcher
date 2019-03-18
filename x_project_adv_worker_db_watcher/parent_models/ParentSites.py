# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType, ChoiceType, UUIDType

from .choiceTypes import AMQPStatusType
from .meta import ParentBase


class ParentSite(ParentBase):
    __tablename__ = 'sites'
    id = Column(BigInteger, primary_key=True)
    id_account = Column(ForeignKey('accounts.id'), index=True)
    guid = Column(UUIDType(binary=True), index=True)
    url = Column(URLType)
    name = Column(String)
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))
    account = relationship('ParentAccount', back_populates='sites', foreign_keys='ParentSite.id_account', uselist=False)
    blocks = relationship("ParentBlock", back_populates="site", collection_class=set, cascade="all", uselist=True)
    pricing = relationship("ParentSitePricing", back_populates="site", foreign_keys='ParentSitePricing.id',
                           uselist=False)

    categories_block_adv = relationship("ParentSiteByBlockingAdvCategory", uselist=True,
                                        foreign_keys='ParentSiteByBlockingAdvCategory.id_site',
                                        primaryjoin='ParentSite.id == ParentSiteByBlockingAdvCategory.id_site')
