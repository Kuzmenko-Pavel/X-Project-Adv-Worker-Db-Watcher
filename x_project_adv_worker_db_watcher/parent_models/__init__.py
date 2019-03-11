import os

from sqlalchemy import create_engine

from .meta import ParentDBSession, parent_metadata
from .Accounts import Account
from .AccountsRates import AccountRates
from .AdvCategories import AdvCategory
from .Blocks import Block
from .BlocksPricing import BlockPricing
from .Campaigns import Campaign
from .CampaignsByBlockingBlock import CampaignByBlockingBlock
from .CampaignsByDevices import CampaignByDevices
from .CampaignsByGeos import CampaignsByGeo
from .CampaignsByThematicCategories import CampaignByThematicCategories
from .CampaignsCron import CampaignCron
from .Devices import Device
from .GeoLite import Geo
from .Images import Image
from .Offers import Offer
from .OffersBody import OfferBody
from .OffersByAdvCategories import OfferByAdvCategories
from .OffersByImages import OfferByImages
from .Sites import Site
from .SitesByBlockingAdvCategories import SiteByBlockingAdvCategory
from .SitesPricing import SitePricing


def get_parent_engine(config):
    application_name = 'AdvWorkerDbWatcher pid=%s' % os.getpid()
    engine = create_engine(config['parent_postgres']['uri'], echo=False, pool_recycle=300, pool_pre_ping=True,
                           max_overflow=5, connect_args={"application_name": application_name})
    ParentDBSession.configure(bind=engine)
    parent_metadata.bind = engine
    return engine
