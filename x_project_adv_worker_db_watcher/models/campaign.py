from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, Index)
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True)
    title = Column(String(length=100))
    project = Column(String(length=70))
    social = Column(Boolean, default=False)
    impressions_per_day_limit = Column(SmallInteger)
    showCoverage = Column(SmallInteger)
    retargeting = Column(Boolean, default=False)
    cost = Column(SmallInteger, default=0)
    gender = Column(SmallInteger, default=0)
    retargeting_type = Column(String(length=10), default='offer')
    brending = Column(Boolean, default=False)
    recomendet_type = Column(String(length=3))
    recomendet_count = Column(SmallInteger)
    account = Column(String(length=64), default='')
    target = Column(String(length=100), default='')
    offer_by_campaign_unique = Column(SmallInteger, default=1)
    unique_impression_lot = Column(SmallInteger, default=1)
    html_notification = Column(Boolean, default=True)
    disabled_retargiting_style = Column(Boolean, default=False)
    disabled_recomendet_style = Column(Boolean, default=False)

    __table_args__ = (Index('idx_Campaign_query', 'id', 'gender', 'cost', 'retargeting', 'social'),)
