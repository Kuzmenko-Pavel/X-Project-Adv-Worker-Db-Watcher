import os
import socket

import transaction
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from .cron import Cron, MVCron
from .device import Device, MVDevice
from .geo import Geo, MVGeo
from .block import Block, MVBlock
from .campaign import Campaign, MVCampaign
from .campaign2BlockingBlock import Campaign2BlockingBlock, MVCampaign2BlockingBlock
from .campaign2Device import Campaign2Device, MVCampaign2Device
from .campaign2Geo import Campaign2Geo, MVCampaign2Geo
from .campaign_thematic import CampaignThematic, MVCampaignThematic
from .campaign2BlockPrice import Campaign2BlockPrice, MVCampaign2BlockPrice
from .offer import Offer, MVOfferPlace, MVOfferSocial, MVOfferAccountRetargeting, MVOfferDynamicRetargeting
from .offer_categories import OfferCategories, MVOfferCategories
from .offer2blockRating import (Offer2BlockRating, OfferSocial2BlockRating, MVOfferPlace2Informer,
                                MVOfferSocialPlace2Informer)
from .meta import DBSession, metadata

server_name = socket.gethostname()


def get_engine(config):
    application_name = 'AdvWorkerDbWatcher on %s pid=%s' % (server_name, os.getpid())
    engine = create_engine(config['postgres']['uri'],
                           echo=False,
                           pool_size=2,
                           max_overflow=5,
                           pool_recycle=300,
                           pool_use_lifo=False,
                           pool_pre_ping=True,
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
