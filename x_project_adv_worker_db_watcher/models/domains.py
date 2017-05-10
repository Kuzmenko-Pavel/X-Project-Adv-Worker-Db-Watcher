from sqlalchemy import (Column, Integer, String, Boolean)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed
from .meta import Base


class Domains(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
    flag = Column(Boolean, default=False)
    categories = relationship('Categories', secondary='categories2domain',
                              back_populates="domains")

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['name'],
                set_=dict(flag=False)
            ).values({
                'name': data['name']
            }).returning()
        )
        mark_changed(session)
        session.flush()
        return {'id': acc.inserted_primary_key[0], 'name': data['name']}
