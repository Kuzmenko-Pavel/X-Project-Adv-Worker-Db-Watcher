from sqlalchemy import (Column, BigInteger, String, ForeignKey, select, Index)
from sqlalchemy_utils import UUIDType

from .__libs__.sql_view import create_view
from .meta import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(BigInteger, primary_key=True)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    guid = Column(UUIDType(binary=True))
    name = Column(String(length=2048))

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVSite(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_site',
        select([
            Site.id,
            Site.name
        ]).select_from(Site),
        is_mat=True)


Index('ix_mv_site_id', MVSite.id, unique=True)
Index('ix_mv_site_name', MVSite.name)
