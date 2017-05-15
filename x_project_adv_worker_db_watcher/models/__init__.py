import os
from sqlalchemy import create_engine
from zope.sqlalchemy import mark_changed
from sqlalchemy import event
from sqlalchemy.engine import Engine
import transaction
import time
import csv
from x_project_adv_worker_db_watcher.logger import logger
from .meta import DBSession, metadata

from .informer import Informer
from .accounts import Accounts
from .campaign import Campaign
from .categories import Categories
from .device import Device
from .domains import Domains
from .cron import Cron
from .geo import Geo
from .geo_lite_city import GeoLiteCity
from .categories2domain import Categories2Domain
from .campaign2accounts import Campaign2Accounts
from .campaign2categories import Campaign2Categories
from .campaign2device import Campaign2Device
from .campaign2domains import Campaign2Domains
from .campaign2informer import Campaign2Informer


def get_engine(config):
    engine = create_engine(config['postgres']['uri'], echo=True)
    DBSession.configure(bind=engine)
    metadata.bind = engine
    return engine


def check_table(engine):
    clear_table(engine)
    load_default_data()


def clear_table(engine):
    with transaction.manager:
        metadata.drop_all(engine, checkfirst=True)
        metadata.create_all(engine, checkfirst=True)
        for table in reversed(metadata.sorted_tables):
            DBSession.execute(table.delete())
        mark_changed(DBSession())
        DBSession.flush()


def load_default_data():
    with transaction.manager:
        default_account = Accounts(name='')
        default_category = Categories(guid='', title='')
        default_device = Device(name='**')
        default_domain = Domains(name='')
        DBSession.add(default_account)
        DBSession.add(default_category)
        DBSession.add(default_device)
        DBSession.add(default_domain)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/fixture/GEO', newline='') as geo_file:
            geo_reader = csv.reader(geo_file, delimiter=',')
            for row in geo_reader:
                DBSession.add(GeoLiteCity(country=row[0], region=row[1], city=row[2]))
        with open(dir_path + '/fixture/GEO_NOT_FOUND', newline='') as geo_file:
            geo_reader = csv.reader(geo_file, delimiter=',')
            for row in geo_reader:
                DBSession.add(GeoLiteCity(country=row[0], region=row[1], city=row[2]))

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

