import transaction
from zope.sqlalchemy import mark_changed
from x_project_adv_worker_db_watcher.logger import *
from x_project_adv_worker_db_watcher.models import (Accounts, Device, Domains, Categories, Informer, Campaign,
                                                    GeoLiteCity, Cron, Campaign2Accounts, Campaign2Informer,
                                                    Campaign2Domains, Offer)
from .adv_settings import AdvSetting
from .block_settings import BlockSetting


class Loader(object):
    __slots__ = ['session', 'parent_session']

    def __init__(self, db_session, parent_db_session):
        self.session = db_session
        self.parent_session = parent_db_session['getmyad_db']

    def all(self):
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
        return int(val)

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
            session = self.session()
            if guid is None:
                session.close()
                return
            with transaction.manager:
                old_informer = session.query(Informer).filter(Informer.guid == guid).one_or_none()
                if old_informer is not None:
                    session.delete(old_informer)
                    session.flush()
                    transaction.commit()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_informer')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_informer(self, query=None, *args, **kwargs):
        try:
            if query is None:
                query = {}
            fields = {
                'guid_int': 1,
                'guid': 1,
                'domain': 1,
                'user': 1,
                'title': 1,
                'dynamic': 1,
                'admaker': 1,
                'auto_reload': 1,
                'blinking': 1,
                'shake': 1,
                'blinking_reload': 1,
                'shake_reload': 1,
                'shake_mouse': 1,
                'html_notification': 1,
                'plase_branch': 1,
                'retargeting_branch': 1,
                'social_branch': 1,
                'rating_division': 1
            }
            informers = self.parent_session['informer'].find(query, fields)
            session = self.session()
            with transaction.manager:
                for informer in informers:
                    try:
                        data = dict()
                        domains = session.query(Domains).filter(Domains.name == informer.get('domain', '')).first()
                        account = session.query(Accounts).filter(Accounts.name == informer.get('user', '')).first()
                        data['id'] = informer.get('guid_int', 1)
                        data['guid'] = informer.get('guid', '')
                        data['domain'] = domains.id
                        data['account'] = account.id
                        data['title'] = informer.get('title', '')
                        data['headerHtml'] = informer.get('admaker', {}).get('MainHeader', {}).get('html', '')
                        data['footerHtml'] = informer.get('admaker', {}).get('MainFooter', {}).get('html', '')
                        data['dynamic'] = informer.get('dynamic', False)
                        if not data['dynamic']:
                            data['ad_style'] = self.ad_style(informer.get('admaker', {}))
                        else:
                            data['ad_style'] = None
                        data['auto_reload'] = informer.get('auto_reload')
                        data['blinking'] = informer.get('blinking')
                        data['shake'] = informer.get('shake')
                        data['blinking_reload'] = informer.get('blinking_reload')
                        data['shake_reload'] = informer.get('shake_reload')
                        data['shake_mouse'] = informer.get('shake_mouse')
                        data['html_notification'] = informer.get('html_notification', True)
                        data['place_branch'] = informer.get('plase_branch', True)
                        data['retargeting_branch'] = informer.get('retargeting_branch', True)
                        data['social_branch'] = informer.get('social_branch', True)
                        data['rating_division'] = informer.get('rating_division')

                        Informer.upsert(session, data=data)
                    except Exception as e:
                        print(e)
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_informer')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain(self, query=None, *args, **kwargs):
        result = []
        try:
            session = self.session()
            if query is None:
                query = {}
            fields = {
                'domain': 1
            }
            informers = self.parent_session['informer'].find(query, fields)
            with transaction.manager:
                for informer in informers:
                    name = informer.get('domain', '')
                    result.append(Domains.upsert(session, {'name': name}))
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_domains')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def stop_domain(self, name=None, *args, **kwargs):
        try:
            session = self.session()
            if name is None:
                session.close()
                return
            with transaction.manager:
                old_domain = session.query(Domains).filter(Domains.name == name).one_or_none()
                if old_domain is not None:
                    session.delete(old_domain)
                    session.flush()
                    transaction.commit()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_categories2domain')
                self.refresh_mat_view('mv_domains')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain_all(self, query=None, *args, **kwargs):
        result = []
        try:
            session = self.session()
            if query is None:
                query = {}
            fields = {
                'domains': 1
            }
            domains = self.parent_session['domain'].find(query, fields)
            with transaction.manager:
                for domain in domains:
                    for _, name in domain.get('domains', {}).items():
                        result.append(Domains.upsert(session, {'name': name}))
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_domains')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def stop_account(self, name=None, *args, **kwargs):
        try:
            session = self.session()
            if name is None:
                name = ''
            with transaction.manager:
                old_account = session.query(Accounts).filter(Accounts.name == name).one_or_none()
                if old_account is not None:
                    session.delete(old_account)
                    session.flush()
                    transaction.commit()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_accounts')
                self.refresh_mat_view('mv_informer')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_account(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            if query is None:
                query = {}
            query['manager'] = False
            fields = {
                'login': 1,
                'blocked': 1
            }
            accounts = self.parent_session['users'].find(query, fields)
            if accounts.count() <= 0 and 'login' in query:
                self.stop_account(name=query['login'])
            with transaction.manager:
                for account in accounts:
                    name = account.get('login', '')
                    blocked = True if account.get('blocked') == ('banned' or 'light') else False
                    Accounts.upsert(session, {'name': name, 'blocked': blocked})

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_accounts')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_categories(self, query=None, *args, **kwargs):
        result = []
        try:
            session = self.session()
            if query is None:
                query = {}
            fields = {
                'guid': 1,
                'title': 1
            }
            categories = self.parent_session['advertise.category'].find(query, fields)
            with transaction.manager:
                for category in categories:
                    guid = category.get('guid', '')
                    title = category.get('title', '')
                    result.append(Categories.upsert(session, {'guid': guid, 'title': title}))
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_categories')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
        return result

    def load_domain_category_by_account(self, query=None, *args, **kwargs):
        try:
            if query is None:
                query = {}
            domains = []
            cursor = self.load_domain_all(query)
            for domain in cursor:
                domains.append(domain.get('name', ''))
            self.load_domain_category({'domain': {'$in': list(set(domains))}})
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_domain_category(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            if query is None:
                query = {}
            fields = {
                'domain': 1,
                'categories': 1
            }
            domain_categories = self.parent_session['domain.categories'].find(query, fields)
            with transaction.manager:
                for domain_category in domain_categories:
                    domains = session.query(Domains).filter(Domains.name == domain_category.get('domain', '')).all()
                    categories = session.query(Categories).filter(
                        Categories.guid.in_(domain_category.get('categories', []))).all()
                    for domain in domains:
                        domain.categories = categories
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_categories2domain')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def stop_campaign(self, guid=None, *args, **kwargs):
        try:
            session = self.session()
            if guid is None:
                guid = ''
            with transaction.manager:
                old_campaign = session.query(Campaign).filter(Campaign.guid == guid).one_or_none()
                if old_campaign is not None:
                    session.delete(old_campaign)
                    session.flush()
                    transaction.commit()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                self.refresh_mat_view('mv_campaign2accounts')
                self.refresh_mat_view('mv_campaign2categories')
                self.refresh_mat_view('mv_campaign2domains')
                self.refresh_mat_view('mv_campaign2informer')
                self.refresh_mat_view('mv_cron')
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_campaign(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            result = []
            offer_place = False
            offer_social = False
            offer_account_retargeting = False
            offer_dynamic_retargeting = False
            if query is None:
                query = {}
            fields = {
                'guid': 1,
                'guid_int': 1,
                'title': 1,
                'social': 1,
                'impressions_per_day_limit': 1,
                'showConditions': 1,
                'disabled_retargiting_style': 1,
                'disabled_recomendet_style': 1,
                'status': 1,
                'account': 1
            }
            campaigns = self.parent_session['campaign'].find(query, fields)
            with transaction.manager:
                for campaign in campaigns:
                    id = campaign.get('guid_int')
                    guid = campaign.get('guid')
                    conditions = campaign.get('showConditions', False)
                    old_campaign = session.query(Campaign).filter(Campaign.guid == guid).one_or_none()
                    if old_campaign is not None:
                        session.delete(old_campaign)
                        session.flush()
                    if not conditions:
                        continue
                    data = dict()
                    data['id'] = id
                    data['guid'] = guid
                    data['title'] = campaign.get('title')
                    data['social'] = campaign.get('social')
                    data['showCoverage'] = conditions.get('showCoverage')
                    data['retargeting'] = conditions.get('retargeting', False)
                    data['cost'] = conditions.get('cost', 0)
                    data['gender'] = conditions.get('gender', 0)
                    data['retargeting_type'] = conditions.get('retargeting_type')
                    data['brending'] = conditions.get('brending')
                    data['recomendet_type'] = conditions.get('recomendet_type')
                    data['recomendet_count'] = conditions.get('recomendet_count')
                    data['account'] = campaign.get('account')
                    data['target'] = conditions.get('target')
                    data['offer_by_campaign_unique'] = conditions.get('offer_by_campaign_unique')
                    data['unique_impression_lot'] = conditions.get('UnicImpressionLot')
                    data['html_notification'] = conditions.get('html_notification')
                    data['styling'] = False
                    data['style_data'] = None
                    data['style_type'] = conditions.get('style_type', 'default')
                    data['style_class'] = 'Block'
                    data['style_class_recommendet'] = 'RecBlock'
                    data['capacity'] = 1
                    if data['style_type'] not in ['default', 'Block', 'RetBlock', 'RecBlock']:
                        data['style_class'] = str(data['id'])
                        data['style_data'] = conditions.get('style_data',
                                                            {'img': '', 'head_title': '', 'button_title': ''})
                        data['style_class_recommendet'] = str(data['id'])
                        data['capacity'] = 2
                        data['offer_by_campaign_unique'] = 10
                        data['styling'] = True
                    elif data['style_type'] in ['Block', 'RetBlock', 'RecBlock']:
                        data['style_class'] = data['style_type']
                        data['style_class_recommendet'] = data['style_type']
                    else:
                        if data['retargeting']:
                            data['style_class'] = 'RetBlock'

                    if campaign.get('status') == 'working':
                        new_campaign = Campaign(**data)
                        session.add(new_campaign)
                        if new_campaign.social:
                            offer_social = True
                        elif new_campaign.retargeting:
                            if new_campaign.retargeting_type == 'offer':
                                offer_dynamic_retargeting = True
                            else:
                                offer_account_retargeting = True
                        else:
                            offer_place = True

                        session.flush()
                        result.append(new_campaign.id)

                        # ------------------------regionTargeting-----------------------
                        country_targeting = conditions.get('geoTargeting', [])
                        region_targeting = conditions.get('regionTargeting', [])
                        if len(country_targeting) <= 0:
                            country_targeting.append('*')
                        if len(region_targeting) <= 0:
                            region_targeting.append('*')
                        geos = list()
                        for country in country_targeting:
                            geos = geos + session.query(GeoLiteCity).filter(
                                GeoLiteCity.country == country, GeoLiteCity.city.in_(region_targeting)).all()

                        new_campaign.geos = geos

                        # ------------------------deviceTargeting-----------------------
                        device = conditions.get('device', [])
                        if len(device) <= 0:
                            device.append('**')
                        new_campaign.devices = session.query(Device).filter(Device.name.in_(device)).all()

                        # ------------------------sites----------------------
                        categories = conditions.get('categories', [])
                        allowed_domains = conditions.get('allowed', {'domains': []}).get('domains', [])
                        allowed_informers = conditions.get('allowed', {'informers': []}).get('informers', [])
                        allowed_accounts = conditions.get('allowed', {'accounts': []}).get('accounts', [])
                        ignored_domains = conditions.get('ignored', {'domains': []}).get('domains', [])
                        ignored_informers = conditions.get('ignored', {'informers': []}).get('informers', [])
                        ignored_accounts = conditions.get('ignored', {'accounts': []}).get('accounts', [])

                        all_allowed_domains = []
                        all_allowed_informer = []
                        all_allowed_accounts = []
                        all_ignored_domains = []
                        all_ignored_informer = []
                        all_ignored_accounts = []
                        if new_campaign.showCoverage == 'thematic':
                            # Тематические и разрешённые, кроме запрещённых
                            new_campaign.categories = session.query(Categories).filter(
                                Categories.guid.in_(categories)).all()

                            for dom in session.query(Domains).filter(Domains.name.in_(allowed_domains)).all():
                                all_allowed_domains.append(dict(id_cam=new_campaign.id,
                                                                id_dom=dom.id, allowed=True))
                            for inf in session.query(Informer).filter(Informer.guid.in_(allowed_informers)).all():
                                all_allowed_informer.append(dict(id_cam=new_campaign.id,
                                                                 id_inf=inf.id, allowed=True))
                            for acc in session.query(Accounts).filter(Accounts.name.in_(allowed_accounts)).all():
                                all_allowed_accounts.append(dict(id_cam=new_campaign.id,
                                                                 id_acc=acc.id, allowed=True))
                            for dom in session.query(Domains).filter(Domains.name.in_(ignored_domains)).all():
                                all_ignored_domains.append(dict(id_cam=new_campaign.id,
                                                                id_dom=dom.id, allowed=False))
                            for inf in session.query(Informer).filter(Informer.guid.in_(ignored_informers)).all():
                                all_ignored_informer.append(dict(id_cam=new_campaign.id,
                                                                 id_inf=inf.id, allowed=False))
                            for acc in session.query(Accounts).filter(Accounts.name.in_(ignored_accounts)).all():
                                all_ignored_accounts.append(dict(id_cam=new_campaign.id,
                                                                 id_acc=acc.id, allowed=False))
                        elif new_campaign.showCoverage == 'allowed':
                            # Только разрешённые
                            for dom in session.query(Domains).filter(Domains.name.in_(allowed_domains)).all():
                                all_allowed_domains.append(dict(id_cam=new_campaign.id,
                                                                id_dom=dom.id, allowed=True))
                            for inf in session.query(Informer).filter(Informer.guid.in_(allowed_informers)).all():
                                all_allowed_informer.append(dict(id_cam=new_campaign.id,
                                                                 id_inf=inf.id, allowed=True))
                            for acc in session.query(Accounts).filter(Accounts.name.in_(allowed_accounts)).all():
                                all_allowed_accounts.append(dict(id_cam=new_campaign.id,
                                                                 id_acc=acc.id, allowed=True))
                        else:
                            # Все, кроме запрещённых
                            all_allowed_accounts.append(dict(id_cam=new_campaign.id, id_acc=1, allowed=True))

                            for dom in session.query(Domains).filter(Domains.name.in_(ignored_domains)).all():
                                all_ignored_domains.append(dict(id_cam=new_campaign.id,
                                                                id_dom=dom.id, allowed=False))
                            for inf in session.query(Informer).filter(Informer.guid.in_(ignored_informers)).all():
                                all_ignored_informer.append(dict(id_cam=new_campaign.id,
                                                                 id_inf=inf.id, allowed=False))
                            for acc in session.query(Accounts).filter(Accounts.name.in_(ignored_accounts)).all():
                                all_ignored_accounts.append(dict(id_cam=new_campaign.id,
                                                                 id_acc=acc.id, allowed=False))

                        session.bulk_insert_mappings(Campaign2Domains, all_allowed_domains)
                        session.bulk_insert_mappings(Campaign2Informer, all_allowed_informer)
                        session.bulk_insert_mappings(Campaign2Accounts, all_allowed_accounts)
                        session.bulk_insert_mappings(Campaign2Domains, all_ignored_domains)
                        session.bulk_insert_mappings(Campaign2Informer, all_ignored_informer)
                        session.bulk_insert_mappings(Campaign2Accounts, all_ignored_accounts)
                        mark_changed(session)

                        # ------------------------cron-----------------------
                        startShowTimeHours = int(conditions.get('startShowTime', {'hours': 0}).get('hours', 0))
                        startShowTimeMinutes = int(conditions.get('startShowTime', {'minutes': 0}).get('minutes', 0))
                        endShowTimeHours = int(conditions.get('endShowTime', {'hours': 0}).get('hours', 0))
                        endShowTimeMinutes = int(conditions.get('endShowTime', {'minutes': 0}).get('minutes', 0))
                        if startShowTimeHours == 0 and startShowTimeMinutes == 0 and endShowTimeHours == 0 and endShowTimeMinutes == 0:
                            endShowTimeHours = 24

                        daysOfWeek = conditions.get('daysOfWeek', [])
                        if len(daysOfWeek) == 0:
                            daysOfWeek = range(1, 8)

                        cron = list()
                        for x in daysOfWeek:
                            cron.append(Cron(day=x, hour=startShowTimeHours, min=startShowTimeMinutes, start_stop=True))
                            cron.append(Cron(day=x, hour=endShowTimeHours, min=endShowTimeMinutes, start_stop=False))

                        new_campaign.cron = cron
                        session.flush()
            logger.info('Starting Load Offer')

            for camp_id in result:
                self.load_offer(query={'campaignId_int': camp_id}, **kwargs)
            logger.info('Stop Load Offer')

            logger.info('Starting Create Recommended Offer')
            with transaction.manager:
                session.flush()
                conn = session.connection()
                for camp_id in result:
                    conn.execute('SELECT create_recommended(%d);' % camp_id)
                mark_changed(session)
                session.flush()
            logger.info('Stop Create Recommended Offer')

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_campaign')
                self.refresh_mat_view('mv_geo')
                self.refresh_mat_view('mv_campaign2device')
                self.refresh_mat_view('mv_campaign2accounts')
                self.refresh_mat_view('mv_campaign2categories')
                self.refresh_mat_view('mv_campaign2domains')
                self.refresh_mat_view('mv_campaign2informer')
                self.refresh_mat_view('mv_cron')
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

    def load_offer(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            result = []
            if query is None:
                return result
            fields = {
                'guid': 1,
                'guid_int': 1,
                'campaignId_int': 1,
                'RetargetingID': 1,
                'image': 1,
                'description': 1,
                'url': 1,
                'title': 1,
                'price': 1,
                'full_rating': 1,
                'Recommended': 1
            }
            offers = self.parent_session['offer'].find(query, fields).limit(200000)
            for offer in offers:
                data = dict()
                rec = offer.get('Recommended', '')
                if isinstance(rec, str) and len(rec) > 0:
                    recommended = [str(x) for x in rec.split(',')]
                else:
                    recommended = []
                data['id'] = offer.get('guid_int')
                data['guid'] = offer.get('guid', '')
                data['id_cam'] = offer.get('campaignId_int')
                data['retid'] = offer.get('RetargetingID', '')
                data['description'] = offer.get('description', '')[:70]
                data['url'] = offer.get('url', '')
                data['title'] = offer.get('title', '')[:35]
                data['price'] = offer.get('price', '')[:35]
                data['rating'] = float(offer.get('full_rating', 0.0))
                data['recommended_ids'] = recommended[:10]
                images = offer.get('image', '')
                if len(images) > 5:
                    data['image'] = images.split(',')[:5]
                    result.append(data)
            with transaction.manager:
                session.bulk_insert_mappings(Offer, result)
                mark_changed(session)
            session.close()
            del result
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_device(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            if query is None:
                query = {}
            devices = self.parent_session['device'].find(query)
            with transaction.manager:
                for device in devices:
                    name = device.get('name', '')
                    Device.upsert(session, {'name': name})

            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_device')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    def load_offer_rating(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            if query is None:
                query = {}
            query['full_rating'] = {'$exists': True}
            fields = {'guid_int': 1, 'full_rating': 1}
            offer_ratings = self.parent_session['offer'].find(query, fields)
            with transaction.manager:

                session.flush()
                conn = session.connection()
                for offer_rating in offer_ratings:
                    id_ofr = offer_rating.get('guid_int')
                    rating = offer_rating.get('full_rating', 0.0)
                    if id_ofr:
                        conn.execute('SELECT offer_rating_update(%d::bigint,%f);' % (id_ofr, rating))

                mark_changed(session)
                session.flush()
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))

    # def load_campaign_rating(self, query=None, *args, **kwargs):
    #     result = []
    #     if query is None:
    #         query = {}
    #     query['full_rating'] = {'$exists': True}
    #     offer_informer_ratings = self.parent_session['stats_daily.rating'].find(query)
    #     with transaction.manager:
    #         session = self.session()
    #         session.flush()
    #         conn = session.connection()
    #         for offer_informer_rating in offer_informer_ratings:
    #             data = {}
    #             id_ofr = offer_informer_rating.get('guid_int')
    #             id_inf = offer_informer_rating.get('adv_int')
    #             rating = offer_informer_rating.get('full_rating', 0.0)
    #             if id_ofr and id_inf:
    #                 result.append(conn.execute('SELECT campaign_informer_rating_update(%d,%d,%d);' %
    #                                            (id_ofr, id_inf, rating)))
    #
    #         mark_changed(session)
    #         session.flush()

    def load_offer_informer_rating(self, query=None, *args, **kwargs):
        try:
            session = self.session()
            if query is None:
                query = {}
            query['full_rating'] = {'$exists': True}
            fields = {'guid_int': 1, 'adv_int': 1, 'full_rating': 1}
            offer_informer_ratings = self.parent_session['stats_daily.rating'].find(query, fields)
            with transaction.manager:
                session.flush()
                conn = session.connection()
                for offer_informer_rating in offer_informer_ratings:
                    id_ofr = offer_informer_rating.get('guid_int')
                    id_inf = offer_informer_rating.get('adv_int')
                    rating = offer_informer_rating.get('full_rating', 0.0)
                    if id_ofr and id_inf:
                        conn.execute('SELECT offer_informer_rating_update(%d,%d,%f);' % (id_ofr, id_inf, rating))

                mark_changed(session)
                session.flush()
            if kwargs.get('refresh_mat_view', True):
                self.refresh_mat_view('mv_offer_place')
                self.refresh_mat_view('mv_offer_social')
                self.refresh_mat_view('mv_offer_place2informer')
                self.refresh_mat_view('mv_offer_social2informer')
            session.close()
        except Exception as e:
            logger.error(exception_message(exc=str(e)))
