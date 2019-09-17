import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (AdvCategory, Device, Geo)
from x_project_adv_worker_db_watcher.parent_models import (ParentAdvCategory, ParentDevice,
                                                           ParentGeo)
from .upsert import upsert
from .utils import thematic_range, trim_by_words, ad_style, to_hour, to_min


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
        logger.info('Starting Load AdvCategory')
        self.load_adv_category(refresh_mat_view=False)
        logger.info('Stopping Load AdvCategory')
        logger.info('Starting Load Device')
        self.load_device(refresh_mat_view=False)
        logger.info('Stopping Load Device')
        logger.info('Starting Load Geo')
        self.load_geo(refresh_mat_view=False)
        logger.info('Stopping Load Geo')
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

    def load_adv_category(self, *args, **kwargs):
        try:
            cols = ['id', 'path']
            rows = []
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                adv_category = parent_session.query(ParentAdvCategory).all()
                for category in adv_category:
                    rows.append([category.id, category.path])
                upsert(session, AdvCategory, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_adv_categories')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_device(self, *args, **kwargs):
        try:
            cols = ['id', 'code']
            rows = []
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                devices = parent_session.query(ParentDevice).all()
                for device in devices:
                    rows.append([device.id, device.code])
                upsert(session, Device, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_device')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_geo(self, *args, **kwargs):
        try:
            cols = ['id', 'country', 'city']
            rows = []
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                geos = parent_session.query(ParentGeo).all()
                for geo in geos:
                    rows.append([geo.id, geo.country, geo.city])
                upsert(session, Geo, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_geo_lite_city')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
