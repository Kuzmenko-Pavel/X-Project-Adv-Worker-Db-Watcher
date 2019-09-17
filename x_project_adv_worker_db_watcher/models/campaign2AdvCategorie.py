from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2AdvCategorie(Base):
    __tablename__ = 'campaign2adv_category'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_adv_category = Column(Integer, ForeignKey('adv_categories.id', ondelete='CASCADE'), primary_key=True,
                             nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2AdvCategorie(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2adv_category',
        select([
            Campaign2AdvCategorie.id_cam,
            Campaign2AdvCategorie.id_adv_category
        ]).select_from(Campaign2AdvCategorie),
        is_mat=True)


Index('ix_mv_campaign2device__id_cam__id_dev', MVCampaign2AdvCategorie.id_cam,
      MVCampaign2AdvCategorie.id_adv_category, unique=True)
