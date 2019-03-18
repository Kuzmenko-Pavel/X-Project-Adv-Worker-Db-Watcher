__all__ = ['Campaign', 'MVCampaign']
from sqlalchemy import (Column, BigInteger, String, Boolean, SmallInteger, select, Index, func, join, text, table,
                        DateTime, ForeignKey)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from datetime import datetime

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True), unique=True)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(length=100))
    social = Column(Boolean, default=False)
    retargeting = Column(Boolean, default=False)
    capacity = Column(SmallInteger, default=1)
    retargeting_type = Column(String(length=10), default='offer')
    brending = Column(Boolean, default=False)
    styling = Column(Boolean, default=False)
    style_data = Column(JSONB, default=lambda: {'img': '', 'head_title': '', 'button_title': ''})
    style_type = Column(String(length=50), default='default')
    style_class = Column(String(length=50), default='Block')
    style_class_recommendet = Column(String(length=50), default='RecBlock')
    recomendet_type = Column(String(length=3))
    recomendet_count = Column(SmallInteger)
    account = Column(String(length=64), default='')
    target = Column(String(length=100), default='')
    offer_by_campaign_unique = Column(SmallInteger, default=1)
    unique_impression_lot = Column(SmallInteger, default=1)
    html_notification = Column(Boolean, default=True)
    disabled_retargiting_style = Column(Boolean, default=False)
    disabled_recomendet_style = Column(Boolean, default=False)
    started_time = Column(DateTime, default=datetime.now)
    thematic = Column(Boolean, default=False)
    thematic_range = Column(SmallInteger, default=1)
    thematics = Column(ARRAY(String), default=[])
    thematic_day_new_auditory = Column(SmallInteger, default=10)
    thematic_day_off_new_auditory = Column(SmallInteger, default=10)
    geos = relationship('GeoLiteCity', secondary='geo', back_populates="campaigns", passive_deletes=True)
    devices = relationship('Device', secondary='campaign2device', back_populates="campaigns", passive_deletes=True)
    cron = relationship('Cron', back_populates="campaign", passive_deletes=True)
    offers = relationship('Offer', back_populates="campaigns", passive_deletes=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign',
        select([
            func.count('offer.id').over(partition_by=Campaign.id).label('offer_count'),
            Campaign.id,
            Campaign.guid,
            Campaign.account,
            Campaign.social,
            Campaign.retargeting,
            Campaign.capacity,
            Campaign.retargeting_type,
            Campaign.brending,
            Campaign.styling,
            Campaign.style_data,
            Campaign.style_type,
            Campaign.style_class,
            Campaign.style_class_recommendet,
            Campaign.recomendet_type,
            Campaign.recomendet_count,
            Campaign.offer_by_campaign_unique,
            Campaign.unique_impression_lot,
            Campaign.html_notification,
            Campaign.thematic,
            Campaign.thematics,
            Campaign.thematic_range
        ], distinct=Campaign.id).select_from(
            join(Campaign, table('offer'), Campaign.id == text('offer.id_cam'), isouter=True)
        )
        ,
        is_mat=True)


Index('ix_mv_campaign_id', MVCampaign.id, unique=True)
