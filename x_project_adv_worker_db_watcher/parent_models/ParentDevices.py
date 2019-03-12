# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, String, BigInteger

from .meta import ParentBase


class ParentDevice(ParentBase):
    __tablename__ = 'devices'
    id = Column(BigInteger, primary_key=True)
    code = Column(String)
