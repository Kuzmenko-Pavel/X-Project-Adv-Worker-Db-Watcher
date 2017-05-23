import csv
import os
import time

import transaction
from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import logger
from .accounts import Accounts, MVAccounts
from .campaign import Campaign, MVCampaign
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
from .geo import Geo, MVGeo
from .geo_lite_city import GeoLiteCity, MVGeoLiteCity
from .informer import Informer, MVInformer
from .meta import DBSession, metadata
from .offer import Offer, MVOfferPlace, MVOfferSocial, MVOfferAccountRetargeting, MVOfferDynamicRetargeting
from .offer2informer import Offer2Informer, MVOfferPlace2Informer, MVOfferSocial2Informer


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
        DBSession.execute('TRUNCATE {} RESTART IDENTITY CASCADE;'.format(
            ', '.join([table.name for table in reversed(metadata.sorted_tables)])))
        # for table in reversed(metadata.sorted_tables):
        #     DBSession.execute(table.delete())
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
