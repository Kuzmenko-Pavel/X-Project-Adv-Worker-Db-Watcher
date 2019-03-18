from sqlalchemy import Column, Integer, String, select, Index
from sqlalchemy.orm import relationship

from .__libs__.sql_view import create_view
from .meta import Base


class Device(Base):
    __tablename__ = 'device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=2), unique=True)
    campaigns = relationship('Campaign', secondary='campaign2device', back_populates="devices", passive_deletes=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


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
