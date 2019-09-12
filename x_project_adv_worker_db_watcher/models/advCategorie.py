# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import Column, BigInteger, select, Index
from sqlalchemy_utils import LtreeType, force_auto_coercion, force_instant_defaults

from .__libs__.sql_view import create_view
from .meta import Base

force_auto_coercion()
force_instant_defaults()


class AdvCategory(Base):
    __tablename__ = 'adv_categories'

    id = Column(BigInteger, primary_key=True)
    path = Column(LtreeType, nullable=False)


class MVAdvCategory(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_adv_categories',
        select([
            AdvCategory.id,
            AdvCategory.path
        ]).select_from(AdvCategory),
        is_mat=True)


Index('ix_mv_adv_categories_id', MVAdvCategory.id, unique=True)
Index('ix_mv_adv_categories_path', MVAdvCategory.path, postgresql_using="gist")
