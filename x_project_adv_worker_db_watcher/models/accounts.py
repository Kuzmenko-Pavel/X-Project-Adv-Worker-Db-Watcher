__all__ = ['Accounts', 'MVAccounts']
from sqlalchemy import (Column, BigInteger, Boolean, String, select, Index)
from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed

from .__libs__.sql_view import create_view
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True))
    blocked = Column(Boolean, default=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )

    @classmethod
    def upsert(cls, session, data):
        session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['id'],
                set_=dict(guid=data['guid'], blocked=data['blocked'])
            ).values({
                'blocked': data['blocked']
            }).returning()
        )
        mark_changed(session)
        session.flush()


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
