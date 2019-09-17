# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from sqlalchemy import Column, String

from .__mixins__ import PrimaryKey
from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class Device(PrimaryKey, ParentBase):
    __tablename__ = 'devices'
    code = Column(String)
