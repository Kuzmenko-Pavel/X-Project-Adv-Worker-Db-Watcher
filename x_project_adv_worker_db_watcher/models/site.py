from sqlalchemy import (Column, BigInteger, Boolean, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(BigInteger, primary_key=True)
    blocked = Column(Boolean, default=False)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVSite(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_site',
        select([
            Site.id,
            Site.blocked,
        ]).select_from(Site),
        is_mat=True)


Index('ix_mv_site_id', MVSite.id, unique=True)
