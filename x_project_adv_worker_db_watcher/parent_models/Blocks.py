# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, String, ForeignKey, Integer, text, Boolean, SmallInteger, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType, ChoiceType
from sqlalchemy.orm import relationship

from .choiceTypes import AMQPStatusType, BlockType
from .meta import ParentBase


class Block(ParentBase):
    __tablename__ = 'blocks'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUIDType(binary=True), index=True)
    name = Column(String, default='')
    amqp_status = Column(ChoiceType(AMQPStatusType, impl=Integer()), default=AMQPStatusType.new,
                         server_default=text("'" + str(AMQPStatusType.new.value) + "'::integer"), nullable=False)
    block_type = Column(ChoiceType(BlockType, impl=Integer()), default=BlockType.adaptive,
                        server_default=text("'" + str(BlockType.adaptive.value) + "'::integer"), nullable=False)
    button = Column(Boolean)
    extended_settings = Column(Boolean)
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

    id_account = Column(ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False, index=True)
    id_site = Column(ForeignKey('sites.id', ondelete='CASCADE'), nullable=True, index=True)
    account = relationship('Account', back_populates='blocks', foreign_keys='Block.id_account', uselist=False)
    site = relationship('Site', back_populates='blocks', foreign_keys='Block.id_site', uselist=False)
    pricing = relationship("BlockPricing", back_populates="block", foreign_keys='BlockPricing.id', uselist=False)
