from sqlalchemy import (Column, BigInteger, String, Boolean, select, Index)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed

from .__libs__.sql_view import create_view
from .meta import Base


class Domains(Base):
    __tablename__ = 'domains'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(length=2048), unique=True)
    flag = Column(Boolean, default=False)
    categories = relationship('Categories', secondary='categories2domain', back_populates="domains",
                              passive_deletes=True)
    campaigns_allowed = relationship('Campaign', secondary='campaign2domains_allowed', back_populates="domains_allowed",
                                     passive_deletes=True)
    campaigns_disallowed = relationship('Campaign', secondary='campaign2domains_disallowed',
                                        back_populates="domains_disallowed", passive_deletes=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )

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


class MVDomains(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_domains',
        select([
            Domains.id,
            Domains.name
        ]).select_from(Domains),
        is_mat=True)


Index('ix_mv_domains_id', MVDomains.id, unique=True)
Index('ix_mv_domains_name', MVDomains.name)
