# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class SiteByBlockingAdvCategory(ParentBase):
    """
    """
    __tablename__ = 'sites_by_block_adv_categories'

    id_site = Column(ForeignKey('sites.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_adv_category = Column(ForeignKey('adv_categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    site = relationship("Site", collection_class=set, passive_deletes=True)
    category = relationship("AdvCategory", collection_class=set, passive_deletes=True)

    @hybrid_property
    def site_name(self):
        return self.site.name

    @hybrid_property
    def category_name(self):
        return self.category.name

    def __hash__(self):
        return hash((self.id_site, self.id_adv_category, self.site, self.category))

    def __eq__(self, other):
        return all([getattr(self, x) == getattr(other, x) for x in
                    ['id_site', 'id_adv_category', 'site', 'category']])
