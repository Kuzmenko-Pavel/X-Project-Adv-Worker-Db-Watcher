from sqlalchemy import (Column, Integer, Boolean, String)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed
from .meta import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
    blocked = Column(Boolean, default=False)
    campaigns = relationship('Campaign', secondary='campaign2accounts', back_populates="accounts")

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
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
        return {'id': acc.inserted_primary_key[0],
                'name': data['name'],
                'blocked': data['blocked']
                }
