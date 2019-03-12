import os

from sqlalchemy import create_engine

from .ParentAccounts import ParentAccount
from .ParentAccountsRates import ParentAccountRates
from .ParentAdvCategories import ParentAdvCategory
from .ParentBlocks import ParentBlock
from .ParentBlocksPricing import ParentBlockPricing
from .ParentCampaigns import ParentCampaign
from .ParentCampaignsByBlockingBlock import ParentCampaignByBlockingBlock
from .ParentCampaignsByDevices import ParentCampaignByDevices
from .ParentCampaignsByGeos import ParentCampaignsByGeo
from .ParentCampaignsByThematicCategories import ParentCampaignByThematicCategories
from .ParentCampaignsCron import ParentCampaignCron
from .ParentDevices import ParentDevice
from .ParentGeoLite import ParentGeo
from .ParentImages import ParentImage
from .ParentOffers import ParentOffer
from .ParentOffersBody import ParentOfferBody
from .ParentOffersByAdvCategories import ParentOfferByAdvCategories
from .ParentOffersByImages import ParentOfferByImages
from .ParentSites import ParentSite
from .ParentSitesByBlockingAdvCategories import ParentSiteByBlockingAdvCategory
from .ParentSitesPricing import ParentSitePricing
from .meta import ParentDBSession, parent_metadata


def get_parent_engine(config):
    application_name = 'AdvWorkerDbWatcher pid=%s' % os.getpid()
    engine = create_engine(config['parent_postgres']['uri'], echo=False, pool_recycle=300, pool_pre_ping=True,
                           max_overflow=5, connect_args={"application_name": application_name})
    ParentDBSession.configure(bind=engine)
    parent_metadata.bind = engine
    return engine
