from sqlalchemy import create_engine
from zope.sqlalchemy import mark_changed
from sqlalchemy import event
from sqlalchemy.engine import Engine
import transaction
import time
from x_project_adv_worker_db_watcher.logger import logger
from .meta import DBSession, metadata

from .campaign import Campaign


def get_engine(config):
    engine = create_engine(config['database'], echo=True)
    DBSession.configure(bind=engine)
    metadata.bind = engine
    return engine


def clear_table(engine):
    with transaction.manager:
        metadata.create_all(engine, checkfirst=True)
        for table in reversed(metadata.sorted_tables):
            DBSession.execute(table.delete())
        mark_changed(DBSession())
        DBSession.flush()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())
    logger.debug("=================== Start Query: ===================")
    logger.debug(statement)


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop(-1)
    logger.debug("=================== Query Complete! ===================")
    logger.debug("=================== Total Time: %f ===================", total)

