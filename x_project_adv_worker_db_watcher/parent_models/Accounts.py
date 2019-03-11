# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, BigInteger, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType, ChoiceType
from .choiceTypes import AccountType, ProjectType

from .meta import ParentBase


class Account(ParentBase):
    __tablename__ = 'accounts'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUIDType(binary=True), index=True)
    account_type = Column(ChoiceType(AccountType, impl=Integer()))
    project = Column(ChoiceType(ProjectType, impl=Integer()))

    sites = relationship("Site", back_populates="account")
    blocks = relationship("Block", back_populates="account")
    campaigns = relationship("Campaign", back_populates="account")
    offers = relationship("Offer", back_populates="account")
    rates = relationship("AccountRates", foreign_keys='AccountRates.id', uselist=False)
