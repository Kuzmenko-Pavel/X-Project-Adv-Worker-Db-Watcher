from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, Boolean)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import LtreeType

from .__libs__.sql_view import create_view
from .meta import Base


class CampaignThematic(Base):
    __tablename__ = 'campaign_thematics'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    path = Column(ARRAY(LtreeType))
    change = Column(Boolean, default=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaignThematic(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign_thematics',
        select([
            CampaignThematic.id_cam,
            CampaignThematic.path,
        ]).select_from(CampaignThematic),
        is_mat=True)


Index('ix_mv_campaign_thematics_id_cam', MVCampaignThematic.id_cam, unique=True)
Index('ix_mv_campaign_thematics_path', MVCampaignThematic.path, postgresql_using="gist")
