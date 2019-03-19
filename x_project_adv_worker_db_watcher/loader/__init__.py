from datetime import datetime

import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT, ISOLATION_LEVEL_DEFAULT
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Accounts, Device, GeoLiteCity, Site, Informer, Campaign, Offer,
                                                    Cron, Campaign2Device, Geo)
from x_project_adv_worker_db_watcher.parent_models import (ParentAccount, ParentDevice, ParentGeo, ParentSite,
                                                           ParentBlock, ParentCampaign, ParentOffer)
from x_project_adv_worker_db_watcher.parent_models.choiceTypes import (CampaignType, BlockType,
                                                                       CampaignRemarketingType, CampaignStylingType,
                                                                       CampaignRecommendedAlgorithmType)
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
                None if x.block_type == BlockType.adaptive else ad_style(x.ad_style),
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

    def load_campaign(self, id=None, *args, **kwargs):
        try:
            offer_place = False
            offer_social = False
            offer_account_retargeting = False
            offer_dynamic_retargeting = False
            cols = ['id', 'guid', 'account', 'title', 'social', 'retargeting', 'capacity', 'retargeting_type',
                    'styling', 'style_data', 'style_type', 'style_class', 'style_class_recommendet', 'recomendet_type',
                    'recomendet_count', 'offer_by_campaign_unique', 'unique_impression_lot',
                    'started_time', 'thematic',
                    'thematic_range', 'thematics', 'thematic_day_new_auditory', 'thematic_day_off_new_auditory']
            camps = {}
            parent_session = self.parent_session()
            campaigns = parent_session.query(ParentCampaign)
            if id:
                campaigns = campaigns.filter(ParentCampaign.id == id)
            for campaign in campaigns.all():
                data = {}
                data['id'] = campaign.id
                data['guid'] = campaign.guid
                data['account'] = campaign.id_account
                data['title'] = campaign.name
                data['social'] = False
                data['retargeting'] = False
                data['thematic'] = False
                data['capacity'] = 1
                data['offer_by_campaign_unique'] = campaign.lot_concurrency
                data['unique_impression_lot'] = campaign.unique_impression_lot
                data['recomendet_count'] = campaign.recommended_count
                data['recomendet_type'] = 'all'
                if campaign.recommended_algorithm == CampaignRecommendedAlgorithmType.descending:
                    data['recomendet_type'] = 'min'
                elif campaign.recommended_algorithm == CampaignRecommendedAlgorithmType.ascending:
                    data['recomendet_type'] = 'max'

                if campaign.campaign_type == CampaignType.remarketing:
                    data['retargeting'] = True
                elif campaign.campaign_type == CampaignType.thematic:
                    data['thematic'] = True
                elif campaign.campaign_type == CampaignType.social:
                    data['social'] = True
                data['retargeting_type'] = 'offer'
                if campaign.remarketing_type == CampaignRemarketingType.account:
                    data['retargeting_type'] = 'account'
                data['styling'] = False
                data['style_data'] = None
                data['style_type'] = 'default'
                if campaign.campaign_style == CampaignStylingType.common:
                    data['style_type'] = 'Block'
                elif campaign.campaign_style == CampaignStylingType.remarketing:
                    data['style_type'] = 'RetBlock'
                elif campaign.campaign_style == CampaignStylingType.recommended:
                    data['style_type'] = 'RecBlock'
                elif campaign.campaign_style == CampaignStylingType.style_1:
                    data['style_type'] = 'Style_1'
                elif campaign.campaign_style == CampaignStylingType.style_2:
                    data['style_type'] = 'Style_2'
                elif campaign.campaign_style == CampaignStylingType.style_3:
                    data['style_type'] = 'Style_3'

                data['style_class'] = 'Block'
                data['style_class_recommendet'] = 'RecBlock'
                data['capacity'] = 1
                if data['style_type'] not in ['default', 'Block', 'RetBlock', 'RecBlock']:
                    data['style_class'] = str(data['id'])
                    data['style_data'] = {
                        'img': campaign.campaign_style_logo,
                        'head_title': campaign.campaign_style_head_title,
                        'button_title': campaign.campaign_style_button_title}
                    data['style_class_recommendet'] = str(data['id'])
                    data['capacity'] = 2
                    data['offer_by_campaign_unique'] = 1
                    data['styling'] = True
                elif data['style_type'] in ['Block', 'RetBlock', 'RecBlock']:
                    data['style_class'] = data['style_type']
                    data['style_class_recommendet'] = data['style_type']
                else:
                    if data['retargeting']:
                        data['style_class'] = 'RetBlock'

                data['started_time'] = datetime.now()
                data['thematic_day_new_auditory'] = campaign.thematic_day_new_auditory
                data['thematic_day_off_new_auditory'] = campaign.thematic_day_off_new_auditory
                data['thematic_range'] = thematic_range(data['started_time'],
                                                        data['thematic_day_new_auditory'],
                                                        data['thematic_day_off_new_auditory'])
                data['thematics'] = []

                data['cron'] = {
                    '1': campaign.cron.monday,
                    '2': campaign.cron.tuesday,
                    '3': campaign.cron.wednesday,
                    '4': campaign.cron.thursday,
                    '5': campaign.cron.friday,
                    '6': campaign.cron.saturday,
                    '7': campaign.cron.sunday,
                }
                data['device'] = [x.id_device for x in campaign.devices]
                data['geo'] = [x.id_geo for x in campaign.geos]
                camps[str(campaign.id)] = data
                if data['social']:
                    offer_social = True
                elif data['retargeting']:
                    if data['retargeting_type'] == 'offer':
                        offer_dynamic_retargeting = True
                    else:
                        offer_account_retargeting = True
                else:
                    offer_place = True

            rows = [[
                v['id'],
                v['guid'],
                v['account'],
                v['title'],
                v['social'],
                v['retargeting'],
                v['capacity'],
                v['retargeting_type'],
                v['styling'],
                v['style_data'],
                v['style_type'],
                v['style_class'],
                v['style_class_recommendet'],
                v['recomendet_type'],
                v['recomendet_count'],
                v['offer_by_campaign_unique'],
                v['unique_impression_lot'],
                v['started_time'],
                v['thematic'],
                v['thematic_range'],
                v['thematics'],
                v['thematic_day_new_auditory'],
                v['thematic_day_off_new_auditory'],
            ] for k, v in camps.items()]
            parent_session.close()

            session = self.session()
            with transaction.manager:
                upsert(session, Campaign, rows, cols)
            session.flush()
            session.close()

            # ------------------------regionTargeting-----------------------
            try:
                for k, v in camps.items():
                    session = self.session()
                    with transaction.manager:
                        for id_geo in v['geo']:
                            id_cam = int(k)
                            g = Geo(id_cam=id_cam, id_geo=id_geo)
                            session.add(g)
                    session.flush()
                    session.close()
            except Exception as e:
                print(e)
            # ------------------------deviceTargeting-----------------------
            try:
                for k, v in camps.items():
                    session = self.session()
                    with transaction.manager:
                        for id_device in v['device']:
                            id_cam = int(k)
                            d = Campaign2Device(id_cam=id_cam, id_dev=id_device)
                            session.add(d)
                    session.flush()
                    session.close()
            except Exception as e:
                print(e)
            # ------------------------cron-----------------------
            try:
                for k, v in camps.items():
                    session = self.session()
                    with transaction.manager:
                        for d, t in v['cron'].items():
                            id_cam = int(k)
                            day = int(d)
                            hour = to_hour(t[0])
                            min = to_min(t[0])
                            c = Cron(id_cam=id_cam, day=day, hour=hour, min=min, start_stop=True)
                            session.add(c)
                            hour = to_hour(t[1])
                            min = to_min(t[1])
                            c = Cron(id_cam=id_cam, day=day, hour=hour, min=min, start_stop=False)
                            session.add(c)
                            hour = to_hour(t[2])
                            min = to_min(t[2])
                            c = Cron(id_cam=id_cam, day=day, hour=hour, min=min, start_stop=True)
                            session.add(c)
                            hour = to_hour(t[3])
                            min = to_min(t[3])
                            c = Cron(id_cam=id_cam, day=day, hour=hour, min=min, start_stop=False)
                            session.add(c)
                    session.flush()
                    session.close()
            except Exception as e:
                print(e)

            logger.info('Start Load Offer')
            for camp_id in camps:
                try:
                    self.load_offer(id_campaign=camp_id, **kwargs)
                except Exception as e:
                    print(e)
            logger.info('Stop Load Offer')

            logger.info('Starting Create Recommended Offer')
            session = self.session()
            with transaction.manager:
                session.flush()
                conn = session.connection()
                for camp_id in camps:
                    try:
                        conn.execute('SELECT create_recommended(%s);' % camp_id)
                    except Exception as e:
                        print(e)
                mark_changed(session)
                session.flush()
            logger.info('Stop Create Recommended Offer')

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                self.refresh_mat_view('mv_campaign2accounts_allowed')
                self.refresh_mat_view('mv_campaign2accounts_disallowed')
                self.refresh_mat_view('mv_campaign2categories')
                self.refresh_mat_view('mv_campaign2domains_allowed')
                self.refresh_mat_view('mv_campaign2domains_disallowed')
                self.refresh_mat_view('mv_campaign2informer_allowed')
                self.refresh_mat_view('mv_campaign2informer_disallowed')
                self.refresh_mat_view('mv_cron')
                if offer_place:
                    self.refresh_mat_view('mv_offer_place')
                    self.refresh_mat_view('mv_offer_place2informer')
                if offer_social:
                    self.refresh_mat_view('mv_offer_social')
                    self.refresh_mat_view('mv_offer_social2informer')
                if offer_account_retargeting:
                    self.refresh_mat_view('mv_offer_account_retargeting')
                if offer_dynamic_retargeting:
                    self.refresh_mat_view('mv_offer_dynamic_retargeting')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_offer(self, id=None, id_campaign=None, *args, **kwargs):
        try:
            limit = self.config.get('offer', {}).get('limit', 1000)
            cols = ['id', 'guid', 'id_cam',
                    'retid', 'description', 'url', 'title', 'price', 'rating',
                    'images', 'recommended_ids', 'recommended'
                    ]
            parent_session = self.parent_session()
            offers = parent_session.query(ParentOffer)
            if id_campaign:
                offers = offers.filter(ParentOffer.id_campaign == id_campaign)
            if id:
                offers = offers.filter(ParentOffer.id == id)

            rows = [[
                x.id,
                x.guid,
                x.id_campaign,
                x.body.id_retargeting,
                trim_by_words(x.body.description, 70),
                x.body.url,
                trim_by_words(x.body.title, 35),
                x.body.price,
                0,
                [],
                [],
                []
            ] for x in offers.limit(limit).all()]
            parent_session.close()

            if rows:
                session = self.session()
                with transaction.manager:
                    upsert(session, Offer, rows, cols)
                session.close()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_informer')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
