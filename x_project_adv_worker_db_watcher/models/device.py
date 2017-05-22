from sqlalchemy import (Column, Integer, String, Boolean, select, Index, select, Index, cast)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed
from .meta import Base
from .__libs__.sql_view import create_view


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2), unique=True)
    flag = Column(Boolean, default=False)
    campaigns = relationship('Campaign', secondary='campaign2device', back_populates="devices", passive_deletes=True)

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


class MVDevice(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_device',
        select([
            Device.id,
            Device.name
        ]).select_from(Device),
        is_mat=True)


Index('ix_mv_device_id', MVDevice.id, unique=True)
Index('ix_mv_device_name', MVDevice.name, unique=True)
