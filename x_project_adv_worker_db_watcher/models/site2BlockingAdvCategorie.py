from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Site2BlockingAdvCategorie(Base):
    __tablename__ = 'site_by_block_adv_categories'
    id_site = Column(BigInteger, ForeignKey('site.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_adv_category = Column(Integer, ForeignKey('block.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVSite2BlockingAdvCategorie(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_site_by_block_adv_categories',
        select([
            Site2BlockingAdvCategorie.id_site,
            Site2BlockingAdvCategorie.id_adv_category
        ]).select_from(Site2BlockingAdvCategorie),
        is_mat=True)


Index('ix_mv_site_by_block_adv_categories', MVSite2BlockingAdvCategorie.id_cam,
      MVSite2BlockingAdvCategorie.id_adv_category,
      unique=True)
