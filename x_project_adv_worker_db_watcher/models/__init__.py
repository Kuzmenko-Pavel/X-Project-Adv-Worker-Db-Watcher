import os

import transaction
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from .advCategorie import AdvCategory
from .meta import DBSession, metadata


def get_engine(config):
    application_name = 'AdvWorkerDbWatcher pid=%s' % os.getpid()
    engine = create_engine(config['postgres']['uri'], echo=False, pool_recycle=300, pool_pre_ping=True, max_overflow=5,
                           connect_args={"application_name": application_name})
    DBSession.configure(bind=engine)
    metadata.bind = engine
    return engine


def check_table(engine):
    clear_table(engine)


def clear_table(engine):
    session = DBSession()
    with transaction.manager:
        metadata.drop_all(engine, checkfirst=True)
        logger.info('Check and Create DB')
        metadata.create_all(engine, checkfirst=True)
        logger.info('Truncate DB')
        session.execute('TRUNCATE {} RESTART IDENTITY CASCADE;'.format(
            ', '.join([table.name for table in reversed(metadata.sorted_tables)])))
        mark_changed(session)
        session.flush()
    session.close()


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler):
    return compiler.visit_drop_table(element) + " CASCADE"

# from sqlalchemy import event
# from sqlalchemy.engine import Engine
# import time
# @event.listens_for(Engine, "before_cursor_execute")
# def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     conn.info.setdefault('query_start_time', []).append(time.time())
#     logger.debug("=================== Start Query: ===================")
#     logger.debug(statement)
#
#
# @event.listens_for(Engine, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
#     total = time.time() - conn.info['query_start_time'].pop(-1)
#     logger.debug("=================== Query Complete! ===================")
#     logger.debug("=================== Total Time: %f ===================", total)
