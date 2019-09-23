import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.choiceTypes import BlockType
from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Device, Geo, Block)
from x_project_adv_worker_db_watcher.parent_models import (ParentDevice, ParentGeo, ParentBlock)
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
        logger.info('Starting Load Device')
        self.load_device(refresh_mat_view=False)
        logger.info('Stopping Load Device')
        logger.info('Starting Load Geo')
        self.load_geo(refresh_mat_view=False)
        logger.info('Stopping Load Geo')
        logger.info('Starting Load Block')
        self.load_block(refresh_mat_view=False)
        logger.info('Stopping Load Block')
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

    def load_device(self, *args, **kwargs):
        try:
            cols = ['id', 'code']
            rows = []
            filter_data = {}
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                devices = parent_session.query(ParentDevice).filter(**filter_data).all()
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
            filter_data = {}
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                geos = parent_session.query(ParentGeo).filter(**filter_data).all()
                for geo in geos:
                    rows.append([geo.id, geo.country, geo.city])
                upsert(session, Geo, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_geo_lite_city')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_block(self, id=None, id_site=None, id_account=None, *args, **kwargs):
        try:
            cols = ['id', 'guid', 'id_account', 'id_site', 'block_type', 'headerHtml', 'footerHtml', 'userCode',
                    'ad_style',
                    'place_branch', 'retargeting_branch', 'social_branch', 'rating_division', 'rating_hard_limit',
                    'name', 'block_adv_category', 'click_cost_min', 'click_cost_proportion', 'click_cost_max',
                    'impression_cost_min', 'impression_cost_proportion', 'impression_cost_max', 'cost_percent',
                    'disable_filter', 'time_filter']
            rows = []
            filter_data = {}
            if id:
                filter_data['id'] = id
            if id_site:
                filter_data['id_site'] = id_site
            if id_account:
                filter_data['id_account'] = id_account
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                blocks = parent_session.query(ParentBlock).filter(**filter_data).all()
                for block in blocks:
                    style = None
                    if block.block_type == BlockType.adaptive:
                        style = ad_style(block.ad_style)
                    rows.append([block.id,
                                 block.guid,
                                 block.id_account,
                                 block.id_site,
                                 block.block_type,
                                 block.headerHtml,
                                 block.footerHtml,
                                 block.userCode,
                                 style,
                                 block.place_branch,
                                 block.retargeting_branch,
                                 block.social_branch,
                                 block.rating_division,
                                 block.rating_hard_limit,
                                 block.name,
                                 block.block_adv_category,
                                 block.click_cost_min,
                                 block.click_cost_proportion,
                                 block.click_cost_max,
                                 block.impression_cost_min,
                                 block.impression_cost_proportion,
                                 block.impression_cost_max,
                                 block.cost_percent,
                                 block.disable_filter,
                                 block.time_filter
                                 ])
                upsert(session, Block, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_block')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

        def delete_block(self, id=None, id_site=None, id_account=None, *args, **kwargs):
            try:
                filter_data = {}
                if id:
                    filter_data['id'] = id
                if id_site:
                    filter_data['id_site'] = id_site
                if id_account:
                    filter_data['id_account'] = id_account
                session = self.session()
                with transaction.manager:
                    session.query(Block).filter(**filter_data).delete(synchronize_session=False)
                if kwargs.get('refresh_mat_view', True):
                    self.refresh_mat_view('mv_block')
                session.close()
            except Exception as e:
                logger.error(exception_message(exc=str(e)))

        def load_campaign(self, id=None, id_account=None, *args, **kwargs):
            pass

        def delete_campaign(self, id=None, id_account=None, *args, **kwargs):
            pass

        def load_offer(self, id=None, id_campaign=None, id_account=None, *args, **kwargs):
            pass

        def delete_offer(self, id=None, id_campaign=None, id_account=None, *args, **kwargs):
            pass
