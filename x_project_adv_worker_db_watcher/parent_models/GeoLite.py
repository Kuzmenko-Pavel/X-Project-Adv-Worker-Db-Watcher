# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, BigInteger, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from sqlalchemy.orm import relationship, backref

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class Geo(ParentBase):
    __tablename__ = 'geo'
    __table_args__ = (
        UniqueConstraint('country', 'city'),
    )
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order = Column(Integer, default=0)
    parent_id = Column(BigInteger, ForeignKey('geo.id', ondelete='SET NULL'), nullable=True)
    country = Column(String(length=9))
    city = Column(String(length=50))
    name_translations = Column(HSTORE)
    children = relationship("Geo", backref=backref('parent', remote_side='Geo.id'))

    __mapper_args__ = {
        "order_by": order
    }

    @hybrid_property
    def children_count(self):
        return len(self.children)
