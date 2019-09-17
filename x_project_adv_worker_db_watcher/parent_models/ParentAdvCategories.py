# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, BigInteger
from sqlalchemy_utils import LtreeType, force_auto_coercion, force_instant_defaults

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentAdvCategory(ParentBase):
    __tablename__ = 'v_worker_adv_categories'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    path = Column(LtreeType, nullable=False)
