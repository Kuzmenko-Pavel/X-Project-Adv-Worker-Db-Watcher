from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Categories2Domain(Base):
    __tablename__ = 'categories2domain'
    id_cat = Column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_dom = Column(BigInteger, ForeignKey('domains.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCategories2Domain(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_categories2domain',
        select([
            Categories2Domain.id_cat,
            Categories2Domain.id_dom
        ]).select_from(Categories2Domain),
        is_mat=True)


Index('ix_mv_categories2domain__id_cat__id_dom',
      MVCategories2Domain.id_cat, MVCategories2Domain.id_dom, unique=True)
