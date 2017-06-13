import transaction
from zope.sqlalchemy import mark_changed

from x_project_adv_worker_db_watcher.models import (Accounts, Device, Domains, Categories, Informer, Campaign,
                                                    GeoLiteCity, Cron, Campaign2Accounts, Campaign2Informer,
                                                    Campaign2Domains, Offer)


class Loader(object):
    def __init__(self, DBSession, ParentDBSession):
        self.session = DBSession
        self.parent_session = ParentDBSession['getmyad_db']

    def all(self):
        self.load_account(refresh_mat_view=False)
        self.load_device(refresh_mat_view=False)
        self.load_domain(refresh_mat_view=False)
        self.load_categories(refresh_mat_view=False)
        self.load_domain_category(refresh_mat_view=False)
        self.load_informer(refresh_mat_view=False)
        self.load_campaign(refresh_mat_view=False)
        self.load_offer_informer_rating(refresh_mat_view=False)
        self.refresh_mat_view()

    def refresh_mat_view(self, name=None):
        with transaction.manager:
            session = self.session()
            session.flush()
            conn = session.connection()
            if name:
                conn.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY %s' % name)
            else:
                conn.execute('SELECT RefreshAllMaterializedViewsConcurrently()')
            mark_changed(session)
            session.flush()

    def load_informer(self, query=None, *args, **kwargs):
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
                data['headerHtml'] = informer.get('admaker', {}).get('MainHeader', {}).get('html', '')
                data['footerHtml'] = informer.get('admaker', {}).get('MainFooter', {}).get('html', '')
                data['ad_style'] = informer.get('admaker', {})
                data['auto_reload'] = informer.get('auto_reload')
                data['blinking'] = informer.get('blinking')
                data['shake'] = informer.get('shake')
                data['blinking_reload'] = informer.get('blinking_reload')
                data['shake_reload'] = informer.get('shake_reload')
                data['shake_mouse'] = informer.get('shake_mouse')
                data['html_notification'] = informer.get('html_notification')
                data['place_branch'] = informer.get('place_branch')
                data['retargeting_branch'] = informer.get('retargeting_branch')
                data['social_branch'] = informer.get('social_branch')
                data['rating_division'] = informer.get('rating_division')

                result.append(Informer.upsert(self.session(), data=data))
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_informer')
        return result

    def load_domain(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            query = {}
        informers = self.parent_session['informer'].find(query, {'domain': 1})
        with transaction.manager:
            for informer in informers:
                name = informer.get('domain', '')
                result.append(Domains.upsert(self.session(), {'name': name}))
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_domains')
        return result

    def load_account(self, query=None, *args, **kwargs):
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

        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_accounts')
        return result

    def load_categories(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            query = {}
        categories = self.parent_session['advertise.category'].find(query)
        with transaction.manager:
            for category in categories:
                guid = category.get('guid', '')
                title = category.get('title', '')
                result.append(Categories.upsert(self.session(), {'guid': guid, 'title': title}))
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_categories')
        return result

    def load_domain_category(self, query=None, *args, **kwargs):
        domain_categories = self.parent_session['domain.categories'].find(query)
        with transaction.manager:
            for domain_category in domain_categories:
                domains = self.session.query(Domains).filter(Domains.name == domain_category.get('domain', '')).all()
                categories = self.session.query(Categories).filter(
                    Categories.guid.in_(domain_category.get('categories', []))).all()
                for domain in domains:
                    domain.categories = categories
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_categories2domain')

    def load_campaign(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            query = {'status': 'working'}
        print(query)
        campaigns = self.parent_session['campaign'].find(query)
        with transaction.manager:
            for campaign in campaigns:
                print(campaign)
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
                data['showCoverage'] = conditions.get('showCoverage')
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
                        geos = geos + self.session.query(GeoLiteCity).filter(
                            GeoLiteCity.country == country, GeoLiteCity.city.in_(region_targeting)).all()

                    new_campaign.geos = geos

                    # ------------------------deviceTargeting-----------------------
                    device = conditions.get('device', [])
                    if len(device) <= 0:
                        device.append('**')
                    new_campaign.devices = self.session.query(Device).filter(Device.name.in_(device)).all()

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
                        new_campaign.categories = self.session.query(Categories).filter(
                            Categories.guid.in_(categories)).all()

                        for dom in self.session.query(Domains).filter(Domains.name.in_(allowed_domains)).all():
                            all_allowed_domains.append(Campaign2Domains(id_cam=new_campaign.id,
                                                                        id_dom=dom.id, allowed=True))
                        for inf in self.session.query(Informer).filter(Informer.guid.in_(allowed_informers)).all():
                            all_allowed_informer.append(Campaign2Informer(id_cam=new_campaign.id,
                                                                          id_inf=inf.id, allowed=True))

                        for acc in self.session.query(Accounts).filter(Accounts.name.in_(allowed_accounts)).all():
                            all_allowed_accounts.append(Campaign2Accounts(id_cam=new_campaign.id,
                                                                          id_acc=acc.id, allowed=True))
                        for dom in self.session.query(Domains).filter(Domains.name.in_(ignored_domains)).all():
                            all_ignored_domains.append(Campaign2Domains(id_cam=new_campaign.id,
                                                                        id_dom=dom.id, allowed=False))
                        for inf in self.session.query(Informer).filter(Informer.guid.in_(ignored_informers)).all():
                            all_ignored_informer.append(Campaign2Informer(id_cam=new_campaign.id,
                                                                          id_inf=inf.id, allowed=False))

                        for acc in self.session.query(Accounts).filter(Accounts.name.in_(ignored_accounts)).all():
                            all_ignored_accounts.append(Campaign2Accounts(id_cam=new_campaign.id,
                                                                          id_acc=acc.id, allowed=False))
                    elif new_campaign.showCoverage == 'allowed':
                        for dom in self.session.query(Domains).filter(Domains.name.in_(allowed_domains)).all():
                            all_allowed_domains.append(Campaign2Domains(id_cam=new_campaign.id,
                                                                        id_dom=dom.id, allowed=True))
                        for inf in self.session.query(Informer).filter(Informer.guid.in_(allowed_informers)).all():
                            all_allowed_informer.append(Campaign2Informer(id_cam=new_campaign.id,
                                                                          id_inf=inf.id, allowed=True))

                        for acc in self.session.query(Accounts).filter(Accounts.name.in_(allowed_accounts)).all():
                            all_allowed_accounts.append(Campaign2Accounts(id_cam=new_campaign.id,
                                                                          id_acc=acc.id, allowed=True))
                    else:
                        all_allowed_accounts.append(Campaign2Accounts(id_cam=new_campaign.id, id_acc=1, allowed=True))

                        for dom in self.session.query(Domains).filter(Domains.name.in_(ignored_domains)).all():
                            all_ignored_domains.append(Campaign2Domains(id_cam=new_campaign.id,
                                                                        id_dom=dom.id, allowed=False))
                        for inf in self.session.query(Informer).filter(Informer.guid.in_(ignored_informers)).all():
                            all_ignored_informer.append(Campaign2Informer(id_cam=new_campaign.id,
                                                                          id_inf=inf.id, allowed=False))

                        for acc in self.session.query(Accounts).filter(Accounts.name.in_(ignored_accounts)).all():
                            all_ignored_accounts.append(Campaign2Accounts(id_cam=new_campaign.id,
                                                                          id_acc=acc.id, allowed=False))
                    self.session.add_all(all_allowed_domains)
                    self.session.add_all(all_allowed_informer)
                    self.session.add_all(all_allowed_accounts)
                    self.session.add_all(all_ignored_domains)
                    self.session.add_all(all_ignored_informer)
                    self.session.add_all(all_ignored_accounts)

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
                    self.session.flush()
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_campaign')
            self.refresh_mat_view('mv_geo')
            self.refresh_mat_view('mv_campaign2device')
            self.refresh_mat_view('mv_campaign2accounts')
            self.refresh_mat_view('mv_campaign2categories')
            self.refresh_mat_view('mv_campaign2domains')
            self.refresh_mat_view('mv_campaign2informer')
            self.refresh_mat_view('mv_cron')
        for camp_id in result:
            self.load_offer(query={'campaignId_int': camp_id}, **kwargs)

    def load_offer(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            return result
        offers = self.parent_session['offer'].find(query)
        for offer in offers:
            data = dict()
            rec = offer.get('Recommended')
            if isinstance(rec, str) and len(rec) > 0:
                recommended = [str(x) for x in rec.split(',')]
            else:
                recommended = []
            data['id'] = offer.get('guid_int')
            data['guid'] = offer.get('guid', '')
            data['id_cam'] = offer.get('campaignId_int')
            data['retid'] = offer.get('RetargetingID', '')
            data['image'] = offer.get('image', '').split(',')
            data['description'] = offer.get('description')
            data['url'] = offer.get('url')
            data['title'] = offer.get('title')
            data['rating'] = offer.get('full_rating', 0)
            data['recommended'] = recommended
            if len(data['image']) > 0:
                result.append(Offer(**data))
        with transaction.manager:
            self.session.add_all(result)
        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_offer_place')
            self.refresh_mat_view('mv_offer_social')
            self.refresh_mat_view('mv_offer_account_retargeting')
            self.refresh_mat_view('mv_offer_dynamic_retargeting')
        return result

    def load_device(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            query = {}
        devices = self.parent_session['device'].find(query)
        with transaction.manager:
            for device in devices:
                name = device.get('name', '')
                result.append(Device.upsert(self.session(), {'name': name}))

        if kwargs.get('refresh_mat_view', True):
            self.refresh_mat_view('mv_device')
        return result

    def load_offer_informer_rating(self, query=None, *args, **kwargs):
        result = []
        if query is None:
            query = {}
        query['full_rating'] = {'$exists': True}
        offer_informer_ratings = self.parent_session['stats_daily.rating'].find(query)
        with transaction.manager:
            session = self.session()
            session.flush()
            conn = session.connection()
            for offer_informer_rating in offer_informer_ratings:
                data = {}
                id_ofr = offer_informer_rating.get('guid_int')
                id_inf = offer_informer_rating.get('adv_int')
                rating = offer_informer_rating.get('full_rating', 0.0)
                if id_ofr and id_inf:
                    result.append(conn.execute('SELECT offer_informer_rating_update(%d,%d,%d);' %
                                               (id_ofr, id_inf, rating)))

            mark_changed(session)
            session.flush()

        # if kwargs.get('refresh_mat_view', True):
        #     self.refresh_mat_view('mv_device')
        return result
