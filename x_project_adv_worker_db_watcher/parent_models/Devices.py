# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy import Column, String, BigInteger

from .meta import ParentBase


class Device(ParentBase):
    __tablename__ = 'devices'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    code = Column(String)
    name_translations = Column(HSTORE)
