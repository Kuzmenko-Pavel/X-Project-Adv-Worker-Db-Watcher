# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, BigInteger, Integer
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from sqlalchemy.orm import relationship, backref

from .__mixins__ import PrimaryKey
from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentGeo(PrimaryKey, ParentBase):
    __tablename__ = 'geo'
    __table_args__ = (
        UniqueConstraint('country', 'city'),
    )
    order = Column(Integer, default=0)
    user_count = Column(Integer, default=0)
    parent_id = Column(BigInteger, ForeignKey('geo.id', ondelete='SET NULL'), nullable=True, index=True)
    country = Column(String(length=9))
    city = Column(String(length=50))
    children = relationship("Geo",
                            backref=backref('parent', remote_side='Geo.id')
                            )

    __mapper_args__ = {
        "order_by": order
    }
