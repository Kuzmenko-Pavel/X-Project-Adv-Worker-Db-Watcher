import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from sqlalchemy import func
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.choiceTypes import BlockType
from x_project_adv_worker_db_watcher.choiceTypes import (CampaignType, CampaignRemarketingType)
from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Device, Geo, Block, Campaign, Campaign2BlockingBlock,
                                                    Campaign2Device, Campaign2Geo, Offer, Cron
                                                    )
from x_project_adv_worker_db_watcher.parent_models import (ParentDevice, ParentGeo, ParentBlock, ParentCampaign,
                                                           ParentOffer)
from .upsert import upsert
from .utils import thematic_range, trim_by_words, ad_style, to_hour, to_min

force_auto_coercion()
force_instant_defaults()


def hour(t):
    return t / 60


def minute(t):
    return t % 60


class Loader(object):
    __slots__ = ['session', 'parent_session', 'config', 'default_geo', 'default_device']

    def __init__(self, db_session, parent_db_session, config):
        self.session = db_session
        self.parent_session = parent_db_session
        self.config = config
        self.default_geo = None
        self.default_device = None

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
        logger.info('Starting Load Default')
        self.load_default()
        logger.info('Stopping Load Default')
        logger.info('Starting Load Block')
        self.load_block(refresh_mat_view=False)
        logger.info('Stopping Load Block')
        logger.info('Starting Load Campaign')
        self.load_campaign(refresh_mat_view=False)
        logger.info('Stopping Load Campaign')
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

    def load_default(self):
        session = self.session()
        with transaction.manager:
            all_device = session.query(Device).filter(Device.code == '**').one_or_none()
            all_geo = session.query(Geo).filter(Geo.country == '*', Geo.city == '*').one_or_none()
            if all_device is None:
                all_device_id = session.query(func.max(Device.id).label("max")).one().max + 1
                all_device = Device(id=all_device_id, code='**')
                session.add(all_device)
                session.flush()
            if all_geo is None:
                all_geo_id = session.query(func.max(Geo.id).label("max")).one().max + 1
                all_geo = Geo(id=all_geo_id, country='*', city='*')
                session.add(all_geo)
                session.flush()
            self.default_geo = all_geo.id
            self.default_device = all_device.id

    def load_device(self, *args, **kwargs):
        try:
            cols = ['id', 'code']
            rows = []
            filter_data = {}
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                devices = parent_session.query(ParentDevice).filter_by(**filter_data).all()
                for device in devices:
                    try:
                        rows.append([device.id, device.code])
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
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
                geos = parent_session.query(ParentGeo).filter_by(**filter_data).all()
                for geo in geos:
                    try:
                        rows.append([geo.id, geo.country, geo.city])
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
                upsert(session, Geo, rows, cols)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_geo_lite_city')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_block(self, id=None, id_site=None, id_account=None, *args, **kwargs):
        try:
            self.delete_block(id, id_site, id_account, refresh_mat_view=False)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        try:
            cols = ['id', 'guid', 'id_account', 'id_site', 'block_type', 'headerHtml', 'footerHtml', 'userCode',
                    'ad_style',
                    'place_branch', 'retargeting_branch', 'social_branch', 'rating_division', 'rating_hard_limit',
                    'site_name',
                    'block_adv_category',
                    'click_cost_min', 'click_cost_proportion', 'click_cost_max',
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
                blocks = parent_session.query(ParentBlock).filter_by(**filter_data)
                blocks = blocks.all()
                for block in blocks:
                    try:
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
                                     block.site_name,
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
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
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
                session.query(Block).filter_by(**filter_data).delete(synchronize_session=False)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_block')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_campaign(self, id=None, id_account=None, *args, **kwargs):
        try:
            self.delete_campaign(id, id_account, refresh_mat_view=False)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        try:
            cols = ['id', 'id_account', 'guid', 'campaign_type', 'campaign_style', 'campaign_style_logo',
                    'campaign_style_head_title', 'campaign_style_button_title', 'utm', 'utm_human_data',
                    'disable_filter',
                    'time_filter', 'payment_model', 'lot_concurrency', 'remarketing_type', 'recommended_algorithm',
                    'recommended_count', 'thematic_day_new_auditory', 'thematic_day_off_new_auditory', 'offer_count',
                    'click_cost', 'impression_cost']
            blocking_block_cols = ['id_cam', 'id_block', 'change']
            geo_cols = ['id_cam', 'id_geo', 'change']
            device_cols = ['id_cam', 'id_dev', 'change']
            cron_cols = ['id_cam', 'range', 'day', 'hour', 'min', 'start_stop']
            rows = []
            blocking_block_rows = []
            geo_rows = []
            device_rows = []
            cron_rows = []
            filter_data = {}
            if id:
                filter_data['id'] = id
            if id_account:
                filter_data['id_account'] = id_account
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                campaigns = parent_session.query(ParentCampaign).filter_by(**filter_data).all()
                for campaign in campaigns:
                    try:
                        rows.append([
                            campaign.id,
                            campaign.id_account,
                            campaign.guid,
                            campaign.campaign_type,
                            campaign.campaign_style,
                            campaign.campaign_style_logo,
                            campaign.campaign_style_head_title,
                            campaign.campaign_style_button_title,
                            campaign.utm,
                            campaign.utm_human_data,
                            campaign.disable_filter,
                            campaign.time_filter,
                            campaign.payment_model,
                            campaign.lot_concurrency,
                            campaign.remarketing_type,
                            campaign.recommended_algorithm,
                            campaign.recommended_count,
                            campaign.thematic_day_new_auditory,
                            campaign.thematic_day_off_new_auditory,
                            campaign.offer_count,
                            campaign.click_cost,
                            campaign.impression_cost,
                        ])

                        for block_id in campaign.blocking_block:
                            blocking_block_rows.append([campaign.id, block_id, True])

                        for counter, cron in enumerate(campaign.cron, 1):
                            if len(cron) == 4:
                                cron_rows.append([campaign.id, 0, counter, hour(cron[0]), minute(cron[0]), True])
                                cron_rows.append([campaign.id, 0, counter, hour(cron[1]), minute(cron[1]), False])
                                cron_rows.append([campaign.id, 1, counter, hour(cron[2]), minute(cron[2]), True])
                                cron_rows.append([campaign.id, 1, counter, hour(cron[3]), minute(cron[3]), False])

                        if campaign.geo:
                            for geo_id in campaign.geo:
                                geo_rows.append([campaign.id, geo_id, True])
                        else:
                            if self.default_geo is None:
                                self.load_default()
                            geo_rows.append([campaign.id, self.default_geo, True])

                        if campaign.device:
                            for device_id in campaign.device:
                                device_rows.append([campaign.id, device_id, True])
                        else:
                            if self.default_device is None:
                                self.load_default()
                            device_rows.append([campaign.id, self.default_device, True])
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))

                upsert(session, Campaign, rows, cols)
                upsert(session, Campaign2BlockingBlock, blocking_block_rows, blocking_block_cols)
                upsert(session, Campaign2Geo, geo_rows, geo_cols)
                upsert(session, Campaign2Device, device_rows, device_cols)
                upsert(session, Cron, cron_rows, cron_cols)

            self.load_offer(id_campaign=id, id_account=id_account)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_campaigns_by_blocking_block')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                # self.refresh_mat_view('mv_cron')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def delete_campaign(self, id=None, id_account=None, *args, **kwargs):
        filter_data = {}
        if id:
            filter_data['id'] = id
        if id_account:
            filter_data['id_account'] = id_account
        session = self.session()
        with transaction.manager:
            session.query(Campaign).filter_by(**filter_data).delete(synchronize_session=False)
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_campaign')
            self.refresh_mat_view('mv_campaigns_by_blocking_block')
            self.refresh_mat_view('mv_geo')
            self.refresh_mat_view('mv_campaign2device')
            # self.refresh_mat_view('mv_cron')

        session.close()

    def load_offer(self, id=None, id_campaign=None, id_account=None, *args, **kwargs):
        try:
            self.delete_offer(id, id_campaign, id_account, refresh_mat_view=False)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        try:
            offer_place = False
            offer_social = False
            offer_account_retargeting = False
            offer_dynamic_retargeting = False
            cols = ['id', 'id_cam', 'id_acc', 'title', 'description', 'url', 'price', 'currency', 'id_ret',
                    'recommended', 'images', 'campaign_type', 'campaign_style', 'remarketing_type',
                    'campaign_range_number']
            rows = []
            filter_data = {}
            if id:
                filter_data['id'] = id
            if id_campaign:
                filter_data['id_campaign'] = id
            if id_account:
                filter_data['id_account'] = id_account

            limit = self.config.get('offer', {}).get('limit', 1000)
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                offers = parent_session.query(ParentOffer).filter(
                    ParentOffer.campaign_range_number < limit
                ).filter_by(**filter_data).all()
                for offer in offers:
                    try:
                        if offer.campaign_type == CampaignType.new_auditory:
                            offer_place = True
                        elif offer.campaign_type == CampaignType.thematic:
                            offer_place = True
                        elif offer.campaign_type == CampaignType.social:
                            offer_social = True
                        elif offer.campaign_type == CampaignType.remarketing:
                            if offer.remarketing_type == CampaignRemarketingType.account:
                                offer_account_retargeting = True
                            elif offer.remarketing_type == CampaignRemarketingType.offer:
                                offer_dynamic_retargeting = True
                        rows.append([
                            offer.id,
                            offer.id_campaign,
                            offer.id_account,
                            offer.title,
                            offer.description,
                            offer.url,
                            offer.price,
                            offer.currency,
                            offer.id_retargeting,
                            offer.recommended,
                            offer.images,
                            offer.campaign_type,
                            offer.campaign_style,
                            offer.remarketing_type,
                            offer.campaign_range_number
                        ])
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
                    if len(rows) > 1000:
                        upsert(session, Offer, rows, cols)
                        rows = []
                upsert(session, Offer, rows, cols)
            if kwargs.get('refresh_mat_view', True):
                if offer_place:
                    self.refresh_mat_view('mv_offer_place')
                if offer_social:
                    self.refresh_mat_view('mv_offer_social')
                if offer_account_retargeting:
                    self.refresh_mat_view('mv_offer_account_retargeting')
                if offer_dynamic_retargeting:
                    self.refresh_mat_view('mv_offer_dynamic_retargeting')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def delete_offer(self, id=None, id_campaign=None, id_account=None, *args, **kwargs):
        filter_data = {}
        if id:
            filter_data['id'] = id
        if id_campaign:
            filter_data['id_campaign'] = id_campaign
        if id_account:
            filter_data['id_account'] = id_account
        session = self.session()
        with transaction.manager:
            session.query(Offer).filter_by(**filter_data).delete(synchronize_session=False)
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_offer_place')
            self.refresh_mat_view('mv_offer_social')
            self.refresh_mat_view('mv_offer_account_retargeting')
            self.refresh_mat_view('mv_offer_dynamic_retargeting')

        session.close()
