__all__ = ['Accounts', 'MVAccounts']
from sqlalchemy import (Column, BigInteger, Boolean, String, select, Index)
from sqlalchemy_utils import UUIDType

from .__libs__.sql_view import create_view
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True), unique=True)
    blocked = Column(Boolean, default=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVAccounts(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_accounts',
        select([
            Accounts.id,
            Accounts.blocked
        ]).select_from(Accounts),
        is_mat=True)


Index('ix_mv_accounts_id', MVAccounts.id, unique=True)
