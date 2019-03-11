import os

from sqlalchemy import create_engine

from .meta import ParentDBSession, parent_metadata
from .Devices import Device


def get_parent_engine(config):
    application_name = 'AdvWorkerDbWatcher pid=%s' % os.getpid()
    engine = create_engine(config['parent_postgres']['uri'], echo=False, pool_recycle=300, pool_pre_ping=True,
                           max_overflow=5, connect_args={"application_name": application_name})
    ParentDBSession.configure(bind=engine)
    parent_metadata.bind = engine
    return engine
