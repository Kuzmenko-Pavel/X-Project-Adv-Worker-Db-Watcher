from sqlalchemy import (Column, Integer, String, select, Index, cast)
from sqlalchemy.dialects.postgresql import insert
from zope.sqlalchemy import mark_changed
from sqlalchemy.orm import relationship
from .meta import Base
from .__libs__.sql_view import create_view


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String(length=64), unique=True, index=True)
    title = Column(String(length=1024))
    domains = relationship('Domains', secondary='categories2domain', back_populates="categories", passive_deletes=True)
    campaigns = relationship('Campaign', secondary='campaign2categories', back_populates="categories",
                             passive_deletes=True)

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['guid'],
                set_=dict(title=data['title'])
            ).values({
                'guid': data['guid'],
                'title': data['title']
            }).returning()
        )
        mark_changed(session)
        session.flush()
        return {'id': acc.inserted_primary_key[0],
                'guid': data['guid'],
                'title': data['title']}


class MVCategories(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_categories',
        select([
            Categories.id,
            Categories.guid,
            Categories.title
        ]).select_from(Categories),
        is_mat=True)


Index('ix_mv_categories_id', MVCategories.id, unique=True)
Index('ix_mv_categories_guid', MVCategories.guid)
