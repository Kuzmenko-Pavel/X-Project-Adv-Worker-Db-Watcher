__all__ = ['Accounts', 'MVAccounts']
from sqlalchemy import (Column, BigInteger, Boolean, String, select, Index)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed

from .__libs__.sql_view import create_view
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
    blocked = Column(Boolean, default=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )

    @classmethod
    def upsert(cls, session, data):
        session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['name'],
                set_=dict(blocked=data['blocked'])
            ).values({
                'name': data['name'],
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
            Accounts.name,
            Accounts.blocked
        ]).select_from(Accounts),
        is_mat=True)


Index('ix_mv_accounts_id', MVAccounts.id, unique=True)
Index('ix_mv_accounts_name', MVAccounts.name)
