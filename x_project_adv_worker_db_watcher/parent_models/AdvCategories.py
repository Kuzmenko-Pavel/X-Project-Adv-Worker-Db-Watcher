# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, BigInteger, ForeignKey, Integer
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class AdvCategory(ParentBase):
    __tablename__ = 'adv_categories'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    order = Column(Integer, default=0)
    parent_id = Column(BigInteger, ForeignKey('adv_categories.id', ondelete='SET NULL'), nullable=True)
    name_translations = Column(HSTORE)
    description_translations = Column(HSTORE)
    children = relationship("AdvCategory",
                            backref=backref('parent', remote_side='AdvCategory.id')
                            )

    __mapper_args__ = {
        "order_by": order
    }

    @hybrid_property
    def children_count(self):
        return len(self.children)
