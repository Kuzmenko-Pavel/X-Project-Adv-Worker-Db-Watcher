from datetime import datetime

import transaction
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import or_
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Accounts, Device, Informer, Campaign,
                                                    GeoLiteCity, Cron, Offer, Offer2Informer)
from x_project_adv_worker_db_watcher.parent_models.choiceTypes import AccountType, ProjectType
from x_project_adv_worker_db_watcher.parent_models import (ParentAccount, ParentDevice)
from .adv_settings import AdvSetting
from .block_settings import BlockSetting


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
        logger.info('Starting Load Account')
        self.load_account(refresh_mat_view=False)
        logger.info('Stopping Load Account')
        logger.info('Starting Load Device')
        self.load_device(refresh_mat_view=False)
        logger.info('Stopping Load Device')
        logger.info('Starting Load Domain')
        self.load_domain(refresh_mat_view=False)
        self.load_domain_all(refresh_mat_view=False)
        logger.info('Stopping Load Domain')
        logger.info('Starting Load Categories')
        self.load_categories(refresh_mat_view=False)
        logger.info('Stopping Load Categories')
        logger.info('Starting Load Domain-Categories')
        self.load_domain_category(refresh_mat_view=False)
        logger.info('Stopping Load Domain-Categories')
        logger.info('Starting Load Informer')
        self.load_informer(refresh_mat_view=False)
        logger.info('Stopping Load Informer')
        logger.info('Starting Load Campaign')
        self.load_campaign(refresh_mat_view=False)
        logger.info('Stopping Load Campaign')
        logger.info('Starting Load Informer Rating')
        self.load_offer_informer_rating(refresh_mat_view=False)
        logger.info('Stopping Load Informer Rating')
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
        cursor = connection.cursor()
        logger.info('VACUUM')
        cursor.execute("VACUUM VERBOSE ANALYZE;")

    @staticmethod
    def __to_int(val):
        if val is None:
            val = 0
        elif isinstance(val, str):
            if val == 'auto':
                val = 0
            elif val == '':
                val = 0
            else:
                val = val.replace('px', '')
                val = val.replace('x', '')
        return int(float(val))

    @staticmethod
    def __to_color(val):
        if isinstance(val, str) and len(val) == 6:
            val = '#' + val
        else:
            val = '#ffffff'
        return val

    @staticmethod
    def __to_str(val):
        return val

    @staticmethod
    def __to_float(val):
        if isinstance(val, float):
            return val
        if isinstance(val, int):
            val = float(val)
        else:
            val = 0.0
        return val

    @staticmethod
    def __to_bool(val):
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            if val in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']:
                val = True
            else:
                val = False
        elif isinstance(val, int) or isinstance(val, float):
            val = bool(val)
        else:
            val = False
        return val

    def create_adv_setting(self, data, name=None):
        if name is None:
            name = ''
        try:
            adv = AdvSetting()
            adv.width = self.__to_int(data.get('Advertise', {}).get('width'))
            adv.height = self.__to_int(data.get('Advertise', {}).get('height'))
            adv.top = self.__to_int(data.get('Advertise', {}).get('top'))
            adv.left = self.__to_int(data.get('Advertise', {}).get('left'))
            adv.border_radius = [
                self.__to_int(data.get('Advertise', {}).get('border_top_left_radius')),
                self.__to_int(data.get('Advertise', {}).get('border_top_right_radius')),
                self.__to_int(data.get('Advertise', {}).get('border_bottom_right_radius')),
                self.__to_int(data.get('Advertise', {}).get('border_bottom_left_radius'))
            ]
            adv.margin = [
                self.__to_int(data.get('Advertise', {}).get('margin_top')),
                self.__to_int(data.get('Advertise', {}).get('margin_right')),
                self.__to_int(data.get('Advertise', {}).get('margin_bottom')),
                self.__to_int(data.get('Advertise', {}).get('margin_left'))
            ]
            adv.border = self.__to_int(data.get('Advertise', {}).get('borderWidth%s' % name))
            adv.border_color = self.__to_color(data.get('Advertise', {}).get('borderColor%s' % name))
            background_color_transparent = data.get('Advertise', {}).get('backgroundColor%sStatus' % name, True)
            adv.background_color = 'transparent' if background_color_transparent else self.__to_color(
                data.get('Advertise', {}).get('backgroundColor%s' % name)
            )
            hide_header = self.__to_bool(data.get('%sHeader' % name, {}).get('hide', False))
            if not hide_header:
                adv.header.width = self.__to_int(data.get('%sHeader' % name, {}).get('width'))
                adv.header.height = self.__to_int(data.get('%sHeader' % name, {}).get('height'))
                adv.header.top = self.__to_int(data.get('%sHeader' % name, {}).get('top'))
                adv.header.left = self.__to_int(data.get('%sHeader' % name, {}).get('left'))
            adv.header.font.size = self.__to_int(data.get('%sHeader' % name, {}).get('fontSize'))
            adv.header.font.color = self.__to_color(data.get('%sHeader' % name, {}).get('fontColor'))
            adv.header.font.align = self.__to_str(data.get('%sHeader' % name, {}).get('align'))
            adv.header.font.weight = self.__to_int(data.get('%sHeader' % name, {}).get('fontBold'))
            adv.header.font.letter = self.__to_float(data.get('%sHeader' % name, {}).get('letter_spacing'))
            adv.header.font.line = self.__to_float(data.get('%sHeader' % name, {}).get('line_height'))
            adv.header.font.variant = self.__to_bool(data.get('%sHeader' % name, {}).get('font_variant'))
            adv.header.font.decoration = self.__to_bool(data.get('%sHeader' % name, {}).get('fontUnderline'))
            adv.header.font.family = self.__to_str(
                data.get('%sHeader' % name, {}).get('fontFamily', 'arial, sans serif'))
            hide_description = self.__to_bool(data.get('%sDescription' % name, {}).get('hide', False))
            if not hide_description:
                adv.description.width = self.__to_int(data.get('%sDescription' % name, {}).get('width'))
                adv.description.height = self.__to_int(data.get('%sDescription' % name, {}).get('height'))
                adv.description.top = self.__to_int(data.get('%sDescription' % name, {}).get('top'))
                adv.description.left = self.__to_int(data.get('%sDescription' % name, {}).get('left'))
            adv.description.font.size = self.__to_int(data.get('%sDescription' % name, {}).get('fontSize'))
            adv.description.font.color = self.__to_color(data.get('%sDescription' % name, {}).get('fontColor'))
            adv.description.font.align = self.__to_str(data.get('%sDescription' % name, {}).get('align'))
            adv.description.font.weight = self.__to_int(data.get('%sDescription' % name, {}).get('fontBold'))
            adv.description.font.letter = self.__to_float(data.get('%sDescription' % name, {}).get('letter_spacing'))
            adv.description.font.line = self.__to_float(data.get('%sDescription' % name, {}).get('line_height'))
            adv.description.font.variant = self.__to_bool(data.get('%sDescription' % name, {}).get('font_variant'))
            adv.description.font.decoration = self.__to_bool(data.get('%sDescription' % name, {}).get('fontUnderline'))
            adv.description.font.family = self.__to_str(
                data.get('%sDescription' % name, {}).get('fontFamily', 'arial, sans serif'))
            hide_cost = self.__to_bool(data.get('%sCost' % name, {}).get('hide', False))
            if not hide_cost:
                adv.cost.width = self.__to_int(data.get('%sCost' % name, {}).get('width'))
                adv.cost.height = self.__to_int(data.get('%sCost' % name, {}).get('height'))
                adv.cost.top = self.__to_int(data.get('%sCost' % name, {}).get('top'))
                adv.cost.left = self.__to_int(data.get('%sCost' % name, {}).get('left'))
            adv.cost.font.size = self.__to_int(data.get('%sCost' % name, {}).get('fontSize'))
            adv.cost.font.color = self.__to_color(data.get('%sCost' % name, {}).get('fontColor'))
            adv.cost.font.align = self.__to_str(data.get('%sCost' % name, {}).get('align'))
            adv.cost.font.weight = self.__to_int(data.get('%sCost' % name, {}).get('fontBold'))
            adv.cost.font.letter = self.__to_float(data.get('%sCost' % name, {}).get('letter_spacing'))
            adv.cost.font.line = self.__to_float(data.get('%sCost' % name, {}).get('line_height'))
            adv.cost.font.variant = self.__to_bool(data.get('%sCost' % name, {}).get('font_variant'))
            adv.cost.font.decoration = self.__to_bool(data.get('%sCost' % name, {}).get('fontUnderline'))
            adv.cost.font.family = self.__to_str(data.get('%sCost' % name, {}).get('fontFamily', 'arial, sans serif'))
            hide_button = self.__to_bool(data.get('%sButton' % name, {}).get('hide', False))
            if not hide_button:
                adv.button.width = self.__to_int(data.get('%sButton' % name, {}).get('width'))
                adv.button.height = self.__to_int(data.get('%sButton' % name, {}).get('height'))
                adv.button.top = self.__to_int(data.get('%sButton' % name, {}).get('top'))
                adv.button.left = self.__to_int(data.get('%sButton' % name, {}).get('left'))
            adv.button.border = self.__to_int(data.get('%sButton' % name, {}).get('borderWidth'))
            adv.button.border_color = self.__to_color(data.get('%sButton' % name, {}).get('borderColor'))
            adv.button.border_radius = [
                self.__to_int(data.get('%sButton' % name, {}).get('border_top_left_radius')),
                self.__to_int(data.get('%sButton' % name, {}).get('border_top_right_radius')),
                self.__to_int(data.get('%sButton' % name, {}).get('border_bottom_right_radius')),
                self.__to_int(data.get('%sButton' % name, {}).get('border_bottom_left_radius'))
            ]
            adv.button.background_color = self.__to_color(data.get('%sButton' % name, {}).get('backgroundColor'))
            adv.button.font.size = self.__to_int(data.get('%sButton' % name, {}).get('fontSize'))
            adv.button.font.color = self.__to_color(data.get('%sButton' % name, {}).get('fontColor'))
            adv.button.font.align = self.__to_str(data.get('%sButton' % name, {}).get('align'))
            adv.button.font.weight = self.__to_int(data.get('%sButton' % name, {}).get('fontBold'))
            adv.button.font.letter = self.__to_float(data.get('%sButton' % name, {}).get('letter_spacing'))
            adv.button.font.line = self.__to_float(data.get('%sButton' % name, {}).get('line_height'))
            adv.button.font.variant = self.__to_bool(data.get('%sButton' % name, {}).get('font_variant'))
            adv.button.font.decoration = self.__to_bool(data.get('%sButton' % name, {}).get('fontUnderline'))
            adv.button.font.family = self.__to_str(
                data.get('%sButton' % name, {}).get('fontFamily', 'arial, sans serif'))
            hide_image = self.__to_bool(data.get('%sImage' % name, {}).get('hide', False))
            if not hide_image:
                adv.image.width = self.__to_int(data.get('%sImage' % name, {}).get('width'))
                adv.image.height = self.__to_int(data.get('%sImage' % name, {}).get('height'))
                adv.image.top = self.__to_int(data.get('%sImage' % name, {}).get('top'))
                adv.image.left = self.__to_int(data.get('%sImage' % name, {}).get('left'))
            adv.image.border = self.__to_int(data.get('%sImage' % name, {}).get('borderWidth'))
            adv.image.border_color = self.__to_color(data.get('%sImage' % name, {}).get('borderColor'))
            adv.image.border_radius = [
                self.__to_int(data.get('%sImage' % name, {}).get('border_top_left_radius')),
                self.__to_int(data.get('%sImage' % name, {}).get('border_top_right_radius')),
                self.__to_int(data.get('%sImage' % name, {}).get('border_bottom_right_radius')),
                self.__to_int(data.get('%sImage' % name, {}).get('border_bottom_left_radius'))
            ]
        except Exception as e:
            logger.error(exception_message(exc=str(e), data=data))
            raise
        return adv

    def ad_style(self, data=None):
        adv_data = None
        if data is not None:
            try:
                adv_data = dict()
                block = BlockSetting()
                block.width = self.__to_int(data.get('Main', {}).get('width'))
                block.height = self.__to_int(data.get('Main', {}).get('height'))
                block.border = self.__to_int(data.get('Main', {}).get('borderWidth'))
                block.border_color = self.__to_color(data.get('Main', {}).get('borderColor'))
                background_color_transparent = data.get('Main', {}).get('backgroundColorStatus', True)
                block.background_color = 'transparent' if background_color_transparent else self.__to_color(
                    data.get('Main', {}).get('backgroundColor')
                )
                block.border_radius = [
                    self.__to_int(data.get('Main', {}).get('border_top_left_radius')),
                    self.__to_int(data.get('Main', {}).get('border_top_right_radius')),
                    self.__to_int(data.get('Main', {}).get('border_bottom_right_radius')),
                    self.__to_int(data.get('Main', {}).get('border_bottom_left_radius'))
                ]

                block.default_button.block = self.__to_str(
                    data.get('Button', {}).get('content', block.default_button.block))
                block.default_button.ret_block = self.__to_str(
                    data.get('RetButton', {}).get('content', block.default_button.ret_block))
                block.default_button.rec_block = self.__to_str(
                    data.get('RecButton', {}).get('content', block.default_button.rec_block))

                block.header.width = self.__to_int(data.get('MainHeader', {}).get('width'))
                block.header.height = self.__to_int(data.get('MainHeader', {}).get('height'))
                block.header.top = self.__to_int(data.get('MainHeader', {}).get('top'))
                block.header.left = self.__to_int(data.get('MainHeader', {}).get('left'))

                block.footer.width = self.__to_int(data.get('MainFooter', {}).get('width'))
                block.footer.height = self.__to_int(data.get('MainFooter', {}).get('height'))
                block.footer.top = self.__to_int(data.get('MainFooter', {}).get('top'))
                block.footer.left = self.__to_int(data.get('MainFooter', {}).get('left'))

                block.default_adv.count_adv = self.__to_int(data.get('Main', {}).get('itemsNumber'))

                adv_data['block'] = dict(block)
                adv_data['adv'] = dict()
                adv_data['adv']['Block'] = dict(self.create_adv_setting(data))
                adv_data['adv']['RetBlock'] = dict(self.create_adv_setting(data, 'Ret'))
                adv_data['adv']['RecBlock'] = dict(self.create_adv_setting(data, 'Rec'))
            except Exception as e:
                logger.error(exception_message(exc=str(e), data=data))
                raise
        return adv_data

    def stop_informer(self, guid=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_informer(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain(self, query=None, *args, **kwargs):
        result = []
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def stop_domain(self, name=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain_all(self, query=None, *args, **kwargs):
        result = []
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def stop_account(self, id=None, *args, **kwargs):
        try:
            if id:
                session = self.session()
                with transaction.manager:
                    session.query(Accounts).filtel(Accounts.id == id).delete()
                session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_account(self, id=None, *args, **kwargs):
        try:
            parent_session = self.parent_session()
            session = self.session()
            with transaction.manager:
                q = parent_session.query(ParentAccount).filter(or_(ParentAccount.project == ProjectType.Getmyad,
                                                                   ParentAccount.project == ProjectType.Adload),
                                                               ParentAccount.account_type == AccountType.Customer)
                if id:
                    q = q.filter(ParentAccount.id == id)
                for parent_account in q.all():
                    Accounts.upsert(session, {'id': parent_account.id, 'guid': parent_account.guid, 'blocked': False})

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_accounts')

            parent_session.close()
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_categories(self, query=None, *args, **kwargs):
        result = []
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def load_domain_category_by_account(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain_category(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def stop_campaign(self, guid=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def thematic_range(self, started_time, thematic_day_new_auditory, thematic_day_off_new_auditory):
        range = 0
        now = datetime.now()
        days = (now - started_time).days
        if days > thematic_day_new_auditory:
            thematic_persent = (100.0 / thematic_day_off_new_auditory) * (days - thematic_day_new_auditory)
            if thematic_persent > 90:
                thematic_persent = 90
            range = int(thematic_persent)
        return range

    def thematic_campaign(self, guid=None, *args, **kwargs):
        try:
            session = self.session()
            if guid is None:
                guid = ''
            with transaction.manager:
                campaign = session.query(Campaign).filter(Campaign.guid == guid).one_or_none()
                if campaign is not None:
                    campaign.thematic_range = self.thematic_range(campaign.started_time,
                                                                  campaign.thematic_day_new_auditory,
                                                                  campaign.thematic_day_off_new_auditory)
                    session.flush()
                    transaction.commit()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_campaign')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_campaign(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_offer(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_device(self, *args, **kwargs):
        try:
            parent_session = self.parent_session()
            session = self.session()
            with transaction.manager:
                q = parent_session.query(ParentDevice)
                for parent_device in q.all():
                    print(parent_device)

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_accounts')

            parent_session.close()
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_offer_rating(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_campaign_rating(self, query=None, *args, **kwargs):
        pass

    def load_offer_informer_rating(self, query=None, *args, **kwargs):
        try:
            pass
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
