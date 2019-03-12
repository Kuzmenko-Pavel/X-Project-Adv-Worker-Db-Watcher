# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentSiteByBlockingAdvCategory(ParentBase):
    """
    """
    __tablename__ = 'sites_by_block_adv_categories'

    id_site = Column(ForeignKey('sites.id'), primary_key=True)
    id_adv_category = Column(ForeignKey('adv_categories.id'), primary_key=True)

    site = relationship("ParentSite", foreign_keys=[id_site], uselist=False)
    category = relationship("ParentAdvCategory", foreign_keys=[id_adv_category], uselist=False)
