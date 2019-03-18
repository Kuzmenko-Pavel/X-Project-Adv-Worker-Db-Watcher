from datetime import datetime

import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from sqlalchemy import or_
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Accounts, Device, GeoLiteCity, Site, Informer)
from x_project_adv_worker_db_watcher.parent_models import (ParentAccount, ParentDevice, ParentGeo, ParentSite,
                                                           ParentBlock)
from x_project_adv_worker_db_watcher.parent_models.choiceTypes import AccountType, ProjectType, BlockType
from .adv_settings import AdvSetting
from .block_settings import BlockSetting
from .upsert import upsert


class Loader(object):
    __slots__ = ['session', 'parent_session', 'config']

    def __init__(self, db_session, parent_db_session, config):
        self.session = db_session
        self.parent_session = parent_db_session
        self.config = config

    def all(self):
        logger.info('Starting VACUUM')
        self.vacuum()
        logger.info('Stopping VACUUM')
        logger.info('Starting load Device')
        self.load_device(refresh_mat_view=False)
        logger.info('Stopping load Device')
        logger.info('Starting load Geo')
        self.load_geo(refresh_mat_view=False)
        logger.info('Stopping load Geo')
        logger.info('Starting Load Account')
        self.load_account(refresh_mat_view=False)
        logger.info('Stopping Load Account')
        logger.info('Starting Load Sites')
        self.load_sites(refresh_mat_view=False)
        logger.info('Stopping Load Sites')
        logger.info('Starting Load Informer')
        self.load_informer(refresh_mat_view=False)
        logger.info('Stopping Load Informer')
        logger.info('Starting Reload Mat View')
        self.refresh_mat_view()
        logger.info('Stopping Reload Mat View')
        logger.info('Starting VACUUM')
        self.vacuum()
        logger.info('Stopping VACUUM')

    def refresh_mat_view(self, name=None):
        session = self.session()
        with transaction.manager:
            session.flush()
            conn = session.connection()
            if name:
                logger.info('Mat View %s' % name)
                conn.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY %s' % name)
                mark_changed(session)
                session.flush()
            else:
                for item in conn.execute("SELECT matviewname FROM pg_matviews WHERE schemaname = 'public'"):
                    name = item[0]
                    logger.info('Mat View %s' % name)
                    conn.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY %s' % name)
                    mark_changed(session)
                    session.flush()
        session.close()

    def vacuum(self):
        engine = self.session.bind
        connection = engine.raw_connection()
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        try:
            connection.commit()
            cursor = connection.cursor()
            logger.info('VACUUM')
            cursor.execute("VACUUM VERBOSE ANALYZE;")
            cursor.close()
        except Exception as e:
            print(e)
        connection.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
        connection.close()

    def load_device(self, id=None, *args, **kwargs):
        try:
            cols = ['id', 'name']
            rows = []
            parent_session = self.parent_session()
            devices = parent_session.query(ParentDevice)
            if id:
                devices = devices.filter(ParentDevice.id == id)
            rows = [[
                x.id,
                x.code
            ] for x in devices.all()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, Device, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_device')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_geo(self, id=None, *args, **kwargs):
        try:
            cols = ['id', 'country', 'city']
            rows = []
            parent_session = self.parent_session()
            geos = parent_session.query(ParentGeo)
            if id:
                geos = geos.filter(ParentGeo.id == id)
            rows = [[
                x.id,
                x.country,
                x.city
            ] for x in geos.all()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, GeoLiteCity, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_geo_lite_city')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_account(self, id=None, *args, **kwargs):
        try:
            cols = ['id', 'guid', 'blocked']
            rows = []
            parent_session = self.parent_session()
            accounts = parent_session.query(ParentAccount)
            if id:
                accounts = accounts.filter(ParentAccount.id == id)
            rows = [[
                x.id,
                x.guid,
                False
            ] for x in accounts.all()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, Accounts, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_accounts')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_sites(self, id=None, *args, **kwargs):
        try:
            cols = ['id', 'account', 'guid', 'name']
            rows = []
            parent_session = self.parent_session()
            sites = parent_session.query(ParentSite)
            if id:
                sites = sites.filter(ParentSite.id == id)
            rows = [[
                x.id,
                x.id_account,
                x.guid,
                x.name,
            ] for x in sites.all()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, Site, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_site')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_informer(self, id=None, *args, **kwargs):
        try:
            cols = ['id', 'guid', 'title', 'site', 'account', 'headerHtml', 'footerHtml', 'userCode', 'ad_style',
                    'dynamic', 'place_branch', 'retargeting_branch', 'social_branch', 'rating_division',
                    'rating_hard_limit', 'disable_filter']
            rows = []
            parent_session = self.parent_session()
            blocks = parent_session.query(ParentBlock)
            if id:
                blocks = blocks.filter(ParentBlock.id == id)
            rows = [[
                x.id,
                x.guid,
                x.name,
                x.id_site,
                x.id_account,
                x.headerHtml,
                x.footerHtml,
                x.userCode,
                x.ad_style,
                True if x.block_type == BlockType.adaptive else False,
                x.place_branch,
                x.retargeting_branch,
                x.social_branch,
                x.rating_division,
                x.rating_hard_limit,
                x.disable_filter

            ] for x in blocks.all()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, Informer, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_informer')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))