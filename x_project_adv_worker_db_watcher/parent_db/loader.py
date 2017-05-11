import transaction
from x_project_adv_worker_db_watcher.logger import logger
from x_project_adv_worker_db_watcher.models import (Accounts, Device, Domains, Categories, Informer, Campaign,
                                                    GeoLiteCity, Cron)


class Loader(object):
    def __init__(self, DBSession, ParentDBSession):
        self.session = DBSession
        self.parent_session = ParentDBSession['getmyad_db']

    def all(self):
        self.load_account()
        self.load_device()
        self.load_domain()
        self.load_categories()
        self.load_domain_category()
        self.load_informer()
        self.load_campaign()

    def load_informer(self, query=None):
        result = []
        if query is None:
            query = {}
        informers = self.parent_session['informer'].find(query)
        with transaction.manager:
            for informer in informers:
                data = dict()
                domains = self.session.query(Domains).filter(Domains.name == informer.get('domain', '')).first()
                account = self.session.query(Accounts).filter(Accounts.name == informer.get('user', '')).first()
                data['id'] = informer.get('guid_int')
                data['guid'] = informer.get('guid')
                data['domain'] = domains.id
                data['account'] = account.id
                data['title'] = informer.get('title')
                data['teasersCss'] = informer.get('css')
                data['headerHtml'] = informer.get('admaker', {}).get('MainHeader', {}).get('html', '')
                data['footerHtml'] = informer.get('admaker', {}).get('MainFooter', {}).get('html', '')
                data['nonrelevant'] = informer.get('nonRelevant', {}).get('action', 'social')
                data['user_code'] = informer.get('nonRelevant', {}).get('user_code', '')
                data['auto_reload'] = informer.get('auto_reload')
                data['blinking'] = informer.get('blinking')
                data['shake'] = informer.get('shake')
                data['blinking_reload'] = informer.get('blinking_reload')
                data['shake_reload'] = informer.get('shake_reload')
                data['shake_mouse'] = informer.get('shake_mouse')
                data['capacity'] = informer.get('admaker', {}).get('Main', {}).get('itemsNumber', 0)
                data['valid'] = True
                data['html_notification'] = informer.get('html_notification')
                data['place_branch'] = informer.get('place_branch')
                data['retargeting_branch'] = informer.get('retargeting_branch')
                data['social_branch'] = informer.get('social_branch')
                data['height'] = informer.get('height')
                data['width'] = informer.get('width')
                data['height_banner'] = informer.get('height_banner')
                data['width_banner'] = informer.get('width_banner')
                data['range_short_term'] = informer.get('range_short_term')
                data['range_long_term'] = informer.get('range_long_term')
                data['range_context'] = informer.get('range_context')
                data['range_search'] = informer.get('range_search')
                data['retargeting_capacity'] = informer.get('retargeting_capacity')
                data['rating_division'] = informer.get('rating_division')

                result.append(Informer.upsert(self.session(), data=data))
        return result

    def load_domain(self, query=None):
        result = []
        if query is None:
            query = {}
        informers = self.parent_session['informer'].find(query, {'domain': 1})
        with transaction.manager:
            for informer in informers:
                name = informer.get('domain', '')
                result.append(Domains.upsert(self.session(), {'name': name}))
        return result

    def load_account(self, query=None):
        result = []
        if query is None:
            query = {}
        query['manager'] = False
        accounts = self.parent_session['users'].find(query)
        with transaction.manager:
            for account in accounts:
                name = account.get('login', '')
                blocked = True if account.get('blocked') == ('banned' or 'light') else False
                result.append(Accounts.upsert(self.session(), {'name': name, 'blocked': blocked}))
        return result

    def load_categories(self, query=None):
        result = []
        if query is None:
            query = {}
        categories = self.parent_session['advertise.category'].find(query)
        with transaction.manager:
            for category in categories:
                guid = category.get('guid', '')
                title = category.get('title', '')
                result.append(Categories.upsert(self.session(), {'guid': guid, 'title': title}))
        return result

    def load_domain_category(self, query=None):
        domain_categories = self.parent_session['domain.categories'].find(query)
        with transaction.manager:
            for domain_category in domain_categories:
                domains = self.session.query(Domains).filter(Domains.name == domain_category.get('domain', '')).all()
                categories = self.session.query(Categories).filter(
                    Categories.guid.in_(domain_category.get('categories', []))).all()
                for domain in domains:
                    domain.categories = categories

    def load_campaign(self, query=None):
        result = []
        if query is None:
            query = {'status': 'working'}
        campaigns = self.parent_session['campaign'].find(query)
        with transaction.manager:
            for campaign in campaigns:
                id = campaign.get('guid_int')
                conditions = campaign.get('showConditions')
                old_campaign = self.session.query(Campaign).get(id)
                if old_campaign is not None:
                    self.session.delete(old_campaign)
                    self.session.flush()
                    transaction.commit()
                    transaction.begin()
                data = dict()
                data['id'] = id
                data['guid'] = campaign.get('guid')
                data['title'] = campaign.get('title')
                data['project'] = campaign.get('project')
                data['social'] = campaign.get('social')
                data['impressions_per_day_limit'] = campaign.get('impressionsPerDayLimit')
                data['showCoverage'] = 0
                data['retargeting'] = conditions.get('retargeting')
                data['cost'] = conditions.get('cost')
                data['gender'] = conditions.get('gender')
                data['retargeting_type'] = conditions.get('retargeting_type')
                data['brending'] = conditions.get('brending')
                data['recomendet_type'] = conditions.get('recomendet_type')
                data['recomendet_count'] = conditions.get('recomendet_count')
                data['account'] = campaign.get('account')
                data['target'] = conditions.get('target')
                data['offer_by_campaign_unique'] = conditions.get('offer_by_campaign_unique')
                data['unique_impression_lot'] = conditions.get('UnicImpressionLot')
                data['html_notification'] = conditions.get('html_notification')
                data['disabled_retargiting_style'] = campaign.get('disabled_retargiting_style')
                data['disabled_recomendet_style'] = campaign.get('disabled_recomendet_style')

                if campaign.get('status') == 'working':
                    new_campaign = Campaign(**data)
                    self.session.add(new_campaign)
                    self.session.flush()
                    result.append(new_campaign)

                    # ------------------------regionTargeting - ----------------------
                    country_targeting = conditions.get('geoTargeting', ['*'])
                    region_targeting = conditions.get('regionTargeting', ['*'])
                    geos = list()
                    for country in country_targeting:
                        geos = geos + self.session.query(GeoLiteCity).filter(
                            GeoLiteCity.country == country, GeoLiteCity.city.in_(region_targeting)).all()

                    new_campaign.geos = geos

                    #------------------------deviceTargeting - ----------------------
                    device = conditions.get('device', ['**'])
                    new_campaign.devices = self.session.query(Device).filter(Device.name.in_(device)).all()

                    #------------------------sites----------------------

                    #------------------------cron-----------------------
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
                        cron.append(Cron(day=x, hour=startShowTimeHours, min=startShowTimeMinutes, startStop=True))
                        cron.append(Cron(day=x, hour=endShowTimeHours, min=endShowTimeMinutes, startStop=False))

                    new_campaign.cron = cron
                    self.session.flush()

    def load_device(self, query=None):
        result = []
        if query is None:
            query = {}
        devices = self.parent_session['device'].find(query)
        with transaction.manager:
            for device in devices:
                name = device.get('name', '')
                result.append(Device.upsert(self.session(), {'name': name}))
        return result
