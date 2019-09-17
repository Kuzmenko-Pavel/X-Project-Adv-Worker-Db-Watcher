# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from sqlalchemy import Column, String, BigInteger

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class Device(ParentBase):
    __tablename__ = 'v_worker_devices'
    id = Column(BigInteger, primary_key=True)
    code = Column(String)
