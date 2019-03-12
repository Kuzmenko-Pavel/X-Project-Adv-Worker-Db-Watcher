# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, SmallInteger, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType, ChoiceType
from sqlalchemy.orm import relationship

from .choiceTypes import AMQPStatusType, BlockType
from .meta import ParentBase


class ParentBlock(ParentBase):
    __tablename__ = 'blocks'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True), index=True)
    name = Column(String)
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()))
    block_type = Column(ChoiceType(BlockType, impl=Integer()))
    button = Column(Boolean)
    headerHtml = Column(String)
    footerHtml = Column(String)
    userCode = Column(String)
    ad_style = Column(JSONB)
    auto_reload = Column(SmallInteger)
    blinking = Column(SmallInteger)
    shake = Column(SmallInteger)
    blinking_reload = Column(Boolean)
    shake_reload = Column(Boolean)
    shake_mouse = Column(Boolean)
    html_notification = Column(Boolean)
    place_branch = Column(Boolean)
    retargeting_branch = Column(Boolean)
    social_branch = Column(Boolean)
    rating_division = Column(Integer)

    id_account = Column(ForeignKey('accounts.id'), index=True)
    id_site = Column(ForeignKey('sites.id'), index=True)
    account = relationship('ParentAccount', back_populates='blocks', foreign_keys='ParentBlock.id_account',
                           uselist=False)
    site = relationship('ParentSite', back_populates='blocks', foreign_keys='ParentBlock.id_site', uselist=False)
    pricing = relationship("ParentBlockPricing", back_populates="block", foreign_keys='ParentBlockPricing.id',
                           uselist=False)
