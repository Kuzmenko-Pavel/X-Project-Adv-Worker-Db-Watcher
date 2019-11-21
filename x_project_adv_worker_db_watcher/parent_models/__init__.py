import os
import socket

from sqlalchemy import create_engine

from .ParentBlocks import ParentBlock
from .ParentCampaignBlockPrices import ParentCampaignBlockPrice
from .ParentCampaigns import ParentCampaign
from .ParentDevices import ParentDevice
from .ParentGeoLite import ParentGeo
from .ParentOffers import ParentOffer
from .ParentRatingOffers import ParentRatingOffer
from .ParentRatingSocialOffers import ParentRatingSocialOffer
from .meta import ParentDBSession, parent_metadata

server_name = socket.gethostname()


def get_parent_engine(config):
    application_name = 'AdvWorkerDbWatcher on %s pid=%s' % (server_name, os.getpid())
    engine = create_engine(config['parent_postgres']['uri'], echo=False, pool_recycle=300, pool_pre_ping=True,
                           max_overflow=5, connect_args={"application_name": application_name})
    ParentDBSession.configure(bind=engine)
    parent_metadata.bind = engine
    return engine
