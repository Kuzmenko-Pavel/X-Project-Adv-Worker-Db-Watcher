import transaction
from datetime import datetime
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from sqlalchemy import func
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.choiceTypes import (BlockType, CampaignType, CampaignRemarketingType,
                                                         CampaignStylingType)
from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (metadata, Device, Geo, Block, Campaign, Campaign2BlockingBlock,
                                                    Campaign2Device, Campaign2Geo, Offer, Cron, OfferCategories,
                                                    Campaign2BlockPrice, CampaignThematic, Offer2BlockRating,
                                                    OfferSocial2BlockRating)
from x_project_adv_worker_db_watcher.parent_models import (ParentDevice, ParentGeo, ParentBlock, ParentCampaign,
                                                           ParentOffer, ParentCampaignBlockPrice, ParentRatingOffer,
                                                           ParentRatingSocialOffer)
from .upsert import upsert
from .utils import thematicRange, trim_by_words, ad_style, to_hour, to_min

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
        logger.info('Starting Load Rating')
        self.load_rating(refresh_mat_view=False)
        logger.info('Stopping Load Rating')
        logger.info('Starting Reload Mat View')
        self.refresh_mat_view()
        logger.info('Stopping Reload Mat View')
        logger.info('Starting VACUUM')
        self.vacuum()
        logger.info('Stopping VACUUM')

    def truncate(self):
        session = self.session()
        with transaction.manager:
            logger.info('Truncate DB')
            session.execute('TRUNCATE {} RESTART IDENTITY CASCADE;'.format(
                ', '.join([table.name for table in reversed(metadata.sorted_tables)])))
            mark_changed(session)
            session.flush()
        session.close()

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
                try:
                    all_device_id = session.query(func.max(Device.id).label("max")).one().max + 1
                except Exception as e:
                    print(e)
                    all_device_id = 1
                all_device = Device(id=all_device_id, code='**')
                session.add(all_device)
                session.flush()
            if all_geo is None:
                try:
                    all_geo_id = session.query(func.max(Geo.id).label("max")).one().max + 1
                except Exception as e:
                    print(e)
                    all_geo_id = 1
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
            rows_count = 0
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
                        if block.block_type == BlockType.static:
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
                        rows_count += 1
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
                upsert(session, Block, rows, cols)

            if kwargs.get('refresh_mat_view', True) and rows_count > 0:
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
                count = session.query(Block).filter_by(**filter_data).delete(synchronize_session=False)
                logger.info('Deleted %s blocks' % count)
            if kwargs.get('refresh_mat_view', True):
                if count > 0:
                    self.refresh_mat_view('mv_block')
            transaction.commit()
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_campaign(self, id=None, id_account=None, *args, **kwargs):
        try:
            self.delete_campaign(id, id_account, refresh_mat_view=False)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        try:
            cols = ['id', 'id_account', 'guid', 'name', 'styling',
                    'campaign_type', 'campaign_style', 'campaign_style_logo',
                    'campaign_style_head_title', 'campaign_style_button_title',
                    'campaign_style_class', 'campaign_style_class_recommendet', 'capacity', 'thematic_range',
                    'utm', 'utm_human_data',
                    'disable_filter',
                    'time_filter', 'payment_model', 'lot_concurrency', 'remarketing_type', 'recommended_algorithm',
                    'recommended_count', 'thematic_day_new_auditory', 'thematic_day_off_new_auditory', 'offer_count',
                    'click_cost', 'impression_cost', 'started_time']
            blocking_block_cols = ['id_cam', 'id_block', 'change']
            geo_cols = ['id_cam', 'id_geo', 'change']
            device_cols = ['id_cam', 'id_dev', 'change']
            cron_cols = ['id_cam', 'range', 'day', 'time']
            thematic_categories_cols = ['id_cam', 'path']
            rows = []
            rows_count = 0
            blocking_block_rows = []
            geo_rows = []
            device_rows = []
            cron_rows = []
            thematic_categories_rows = []
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
                        capacity = 1
                        thematic_range = 0
                        styling = False
                        started_time = campaign.started_time
                        if started_time is None:
                            started_time = datetime.now()
                        lot_concurrency = campaign.lot_concurrency
                        campaign_style_class = 'Block'
                        campaign_style_class_recommendet = 'RecBlock'
                        if campaign.campaign_style == CampaignStylingType.common:
                            campaign_style_class = 'Block'
                            campaign_style_class_recommendet = 'Block'
                        elif campaign.campaign_style == CampaignStylingType.recommended:
                            campaign_style_class = 'RecBlock'
                            campaign_style_class_recommendet = 'RecBlock'
                        elif campaign.campaign_style == CampaignStylingType.remarketing:
                            campaign_style_class = 'RetBlock'
                            campaign_style_class_recommendet = 'RetBlock'
                        elif campaign.campaign_style in [CampaignStylingType.style_1, CampaignStylingType.style_2,
                                                         CampaignStylingType.style_3]:
                            campaign_style_class = str(campaign.id)
                            campaign_style_class_recommendet = str(campaign.id)
                            capacity = 2
                            lot_concurrency = 1
                            styling = True
                        else:
                            if campaign.campaign_type == CampaignType.remarketing:
                                campaign_style_class = 'RetBlock'
                        if campaign.campaign_type == CampaignType.thematic:
                            thematic_range = thematicRange(started_time, campaign.thematic_day_new_auditory,
                                                           campaign.thematic_day_off_new_auditory)

                        rows.append([
                            campaign.id,
                            campaign.id_account,
                            campaign.guid,
                            campaign.name,
                            styling,
                            campaign.campaign_type,
                            campaign.campaign_style,
                            campaign.campaign_style_logo,
                            campaign.campaign_style_head_title,
                            campaign.campaign_style_button_title,
                            campaign_style_class,
                            campaign_style_class_recommendet,
                            capacity,
                            thematic_range,
                            campaign.utm,
                            campaign.utm_human_data,
                            campaign.disable_filter,
                            campaign.time_filter,
                            campaign.payment_model,
                            lot_concurrency,
                            campaign.remarketing_type,
                            campaign.recommended_algorithm,
                            campaign.recommended_count,
                            campaign.thematic_day_new_auditory,
                            campaign.thematic_day_off_new_auditory,
                            campaign.offer_count,
                            campaign.click_cost,
                            campaign.impression_cost,
                            started_time
                        ])
                        rows_count += 1
                        if campaign.thematic_categories:
                            thematic_categories_rows.append([
                                campaign.id,
                                campaign.thematic_categories
                            ])

                        for block_id in campaign.blocking_block:
                            blocking_block_rows.append([campaign.id, block_id, True])

                        for counter, cron in enumerate(campaign.cron, 1):
                            if len(cron) == 4:
                                cron_rows.append([campaign.id, 0, counter, [cron[0], cron[1]]])
                                cron_rows.append([campaign.id, 1, counter, [cron[2], cron[3]]])

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
                upsert(session, CampaignThematic, thematic_categories_rows, thematic_categories_cols)

            transaction.commit()
            session.close()

            self.load_campaign_price(id=id, **kwargs)
            self.load_offer(id_campaign=id, id_account=id_account, **kwargs)

            if kwargs.get('refresh_mat_view', True) and rows_count > 0:
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_campaigns_by_blocking_block')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                self.refresh_mat_view('mv_cron')
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
            count = session.query(Campaign).filter_by(**filter_data).delete(synchronize_session=False)
            logger.info('Deleted %s campaigns' % count)
        transaction.commit()
        session.close()
        if kwargs.get('refresh_mat_view', True):
            if count > 0:
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_campaigns_by_blocking_block')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                self.refresh_mat_view('mv_cron')

    def load_campaign_price(self, id=None, *args, **kwargs):
        try:
            self.delete_campaign_price(id, refresh_mat_view=False)
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        try:
            cols = ['id_cam', 'id_block', 'click_cost', 'impression_cost']
            rows = []
            rows_count = 0
            filter_data = {}
            if id:
                filter_data['id'] = id
            session = self.session()
            parent_session = self.parent_session()
            with transaction.manager:
                prices = parent_session.query(ParentCampaignBlockPrice).filter_by(**filter_data).all()
                for price in prices:
                    try:
                        rows.append([
                            price.id,
                            price.id_block,
                            price.click_cost,
                            price.impression_cost,
                        ])
                        rows_count += 1
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))

                upsert(session, Campaign2BlockPrice, rows, cols)

            if kwargs.get('refresh_mat_view', True) and rows_count > 0:
                self.refresh_mat_view('mv_campaigns_by_block_price')

            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def delete_campaign_price(self, id=None, *args, **kwargs):
        filter_data = {}
        if id:
            filter_data['id_cam'] = id
        session = self.session()
        with transaction.manager:
            count = session.query(Campaign2BlockPrice).filter_by(**filter_data).delete(synchronize_session=False)
            logger.info('Deleted %s campaign prices' % count)
        transaction.commit()
        session.close()
        if kwargs.get('refresh_mat_view', True):
            if count > 0:
                self.refresh_mat_view('mv_campaigns_by_block_price')

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
            cols_categories = ['id_offer', 'path']
            rows = []
            rows_categories = []
            filter_data = {}
            if id:
                filter_data['id'] = id
            if id_campaign:
                filter_data['id_campaign'] = id_campaign
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
                        title = trim_by_words(offer.title, 35)
                        description = trim_by_words(offer.description, 70)
                        price = trim_by_words(offer.price, 35)
                        rows.append([
                            offer.id,
                            offer.id_campaign,
                            offer.id_account,
                            title,
                            description,
                            offer.url,
                            price,
                            offer.currency,
                            offer.id_retargeting,
                            offer.recommended,
                            offer.images,
                            offer.campaign_type,
                            offer.campaign_style,
                            offer.remarketing_type,
                            offer.campaign_range_number
                        ])
                        if offer.categories:
                            rows_categories.append([
                                offer.id,
                                offer.categories
                            ])
                    except Exception as e:
                        logger.error(exception_message(exc=str(e)))
                    if len(rows) > 1000:
                        upsert(session, Offer, rows, cols)
                        upsert(session, OfferCategories, rows_categories, cols_categories)
                        rows = []
                        rows_categories = []

                upsert(session, Offer, rows, cols)
                upsert(session, OfferCategories, rows_categories, cols_categories)
            if kwargs.get('refresh_mat_view', True):
                if offer_place:
                    self.refresh_mat_view('mv_offer_place')
                if offer_social:
                    self.refresh_mat_view('mv_offer_social')
                if offer_account_retargeting:
                    self.refresh_mat_view('mv_offer_account_retargeting')
                if offer_dynamic_retargeting:
                    self.refresh_mat_view('mv_offer_dynamic_retargeting')
                if offer_place or offer_social:
                    self.refresh_mat_view('mv_offer_categories')
                    self.refresh_mat_view('mv_offer2block_rating')
                    self.refresh_mat_view('mv_offer_social2block_rating')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def delete_offer(self, id=None, id_campaign=None, id_account=None, *args, **kwargs):
        filter_data = {}
        if id:
            filter_data['id'] = id
        if id_campaign:
            filter_data['id_cam'] = id_campaign
        if id_account:
            filter_data['id_acc'] = id_account
        session = self.session()
        with transaction.manager:
            count = session.query(Offer).filter_by(**filter_data).delete(synchronize_session=False)
            logger.info('Deleted %s offers' % count)
        transaction.commit()
        session.close()
        if kwargs.get('refresh_mat_view', True):
            if count > 0:
                self.refresh_mat_view('mv_offer_place')
                self.refresh_mat_view('mv_offer_social')
                self.refresh_mat_view('mv_offer_account_retargeting')
                self.refresh_mat_view('mv_offer_dynamic_retargeting')

    def load_rating(self, *args, **kwargs):
        cols = ['id_offer', 'id_block', 'is_deleted', 'rating']
        rows = []
        session = self.session()
        with transaction.manager:
            session.query(Offer2BlockRating).update({Offer2BlockRating.is_deleted: True})
            session.query(OfferSocial2BlockRating).update({OfferSocial2BlockRating.is_deleted: True})
            session.flush()
        session.close()

        session = self.session()
        parent_session = self.parent_session()
        with transaction.manager:
            ratings = parent_session.query(ParentRatingOffer).all()
            for rating in ratings:
                rows.append([
                    rating.id_offer,
                    rating.id_block,
                    False,
                    rating.rating

                ])
            upsert(session, Offer2BlockRating, rows, cols)
            rows = []
            ratings = parent_session.query(ParentRatingSocialOffer).all()
            for rating in ratings:
                rows.append([
                    rating.id_offer,
                    rating.id_block,
                    False,
                    rating.rating

                ])
            upsert(session, OfferSocial2BlockRating, rows, cols)

        session.close()

        session = self.session()
        with transaction.manager:
            session.query(Offer2BlockRating).filter(
                Offer2BlockRating.is_deleted == True
            ).delete(synchronize_session=False)
            session.query(OfferSocial2BlockRating).filter(
                OfferSocial2BlockRating.is_deleted == True
            ).delete(synchronize_session=False)
        transaction.commit()
        session.close()

        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_offer2block_rating')
            self.refresh_mat_view('mv_offer_social2block_rating')
