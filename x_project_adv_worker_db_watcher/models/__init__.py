import csv
import os
import time

import transaction
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles

from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from .accounts import *
from .campaign import *
from .campaign2accounts import Campaign2Accounts, MVCampaign2Accounts
from .campaign2categories import Campaign2Categories, MVCampaign2Categories
from .campaign2device import Campaign2Device, MVCampaign2Device
from .campaign2domains import Campaign2Domains, MVCampaign2Domains
from .campaign2informer import Campaign2Informer, MVCampaign2Informer
from .categories import Categories, MVCategories
from .categories2domain import Categories2Domain, MVCategories2Domain
from .cron import Cron, MVCron
from .device import Device, MVDevice
from .domains import Domains, MVDomains
from .geo_lite_city import GeoLiteCity, MVGeoLiteCity
from .geo import Geo, MVGeo
from .informer import Informer, MVInformer
from .campaign2accounts_allowed import *
from .campaign2domains_allowed import *
from .campaign2informer_allowed import *
from .campaign2accounts_disallowed import *
from .campaign2domains_disallowed import *
from .campaign2informer_disallowed import *
from .meta import DBSession, metadata
from .offer import *
from .offer2informer import *


def get_engine(config):
    engine = create_engine(config['postgres']['uri'], echo=False, pool_recycle=600)
    DBSession.configure(bind=engine)
    metadata.bind = engine
    return engine


def check_table(engine):
    clear_table(engine)
    load_default_data()


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


def load_default_data():
    session = DBSession()
    with transaction.manager:
        default_account = Accounts(name='')
        default_category = Categories(guid='', title='')
        default_device = Device(name='**')
        default_domain = Domains(name='')
        session.add(default_account)
        session.add(default_category)
        session.add(default_device)
        session.add(default_domain)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/fixture/GEO', newline='') as geo_file:
            geo_reader = csv.reader(geo_file, delimiter=',')
            for row in geo_reader:
                session.add(GeoLiteCity(country=row[0], region=row[1], city=row[2]))
        with open(dir_path + '/fixture/GEO_NOT_FOUND', newline='') as geo_file:
            geo_reader = csv.reader(geo_file, delimiter=',')
            for row in geo_reader:
                session.add(GeoLiteCity(country=row[0], region=row[1], city=row[2]))

        session.flush()
    session.close()


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler):
    return compiler.visit_drop_table(element) + " CASCADE"


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
