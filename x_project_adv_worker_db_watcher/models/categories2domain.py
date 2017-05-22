from sqlalchemy import (Column, Integer, ForeignKey, select, Index, cast)
from .meta import Base
from .__libs__.sql_view import create_view


class Categories2Domain(Base):
    __tablename__ = 'categories2domain'
    id_cat = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_dom = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), primary_key=True, nullable=False)


class MVCategories2Domain(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_categories2domain',
        select([
            cast(Categories2Domain.id_cat, Integer).label('id_cat_pk'),
            cast(Categories2Domain.id_dom, Integer).label('id_dom_pk')
        ]).select_from(Categories2Domain),
        is_mat=True)


Index('ix_mv_categories2domain_id_cat_pk_id_dom_pk',
      MVCategories2Domain.id_cat_pk, MVCategories2Domain.id_dom_pk, unique=True)
