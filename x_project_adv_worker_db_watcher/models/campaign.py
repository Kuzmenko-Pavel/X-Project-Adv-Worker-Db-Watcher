from sqlalchemy import (Column, Integer, BigInteger, String, Boolean, SmallInteger, Index)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True)
    title = Column(String(length=100))
    project = Column(String(length=70))
    social = Column(Boolean, default=False)
    impressions_per_day_limit = Column(SmallInteger)
    showCoverage = Column(String(length=70))
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
    geos = relationship('GeoLiteCity', secondary='geo', back_populates="campaigns")
    devices = relationship('Device', secondary='campaign2device', back_populates="campaigns")
    cron = relationship('Cron', back_populates="campaign")
    accounts = relationship('Accounts', secondary='campaign2accounts', back_populates="campaigns")
    categories = relationship('Categories', secondary='campaign2categories', back_populates="campaigns")
    offers = relationship('Offer', back_populates="campaign")

    __table_args__ = (Index('idx_Campaign_query', 'id', 'gender', 'cost', 'retargeting', 'social'),)

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['id'],
                set_=dict(
                    guid=data['guid'],
                    title=data['title'],
                    project=data['project'],
                    social=data['social'],
                    impressions_per_day_limit=data['impressions_per_day_limit'],
                    showCoverage=data['showCoverage'],
                    retargeting=data['retargeting'],
                    cost=data['cost'],
                    gender=data['gender'],
                    retargeting_type=data['retargeting_type'],
                    brending=data['brending'],
                    recomendet_type=data['recomendet_type'],
                    recomendet_count=data['recomendet_count'],
                    account=data['account'],
                    target=data['target'],
                    offer_by_campaign_unique=data['offer_by_campaign_unique'],
                    unique_impression_lot=data['unique_impression_lot'],
                    html_notification=data['html_notification'],
                    disabled_retargiting_style=data['disabled_retargiting_style'],
                    disabled_recomendet_style=data['disabled_recomendet_style']
                )
            ).values(dict(
                id=data['id'],
                guid=data['guid'],
                title=data['title'],
                project=data['project'],
                social=data['social'],
                impressions_per_day_limit=data['impressions_per_day_limit'],
                showCoverage=data['showCoverage'],
                retargeting=data['retargeting'],
                cost=data['cost'],
                gender=data['gender'],
                retargeting_type=data['retargeting_type'],
                brending=data['brending'],
                recomendet_type=data['recomendet_type'],
                recomendet_count=data['recomendet_count'],
                account=data['account'],
                target=data['target'],
                offer_by_campaign_unique=data['offer_by_campaign_unique'],
                unique_impression_lot=data['unique_impression_lot'],
                html_notification=data['html_notification'],
                disabled_retargiting_style=data['disabled_retargiting_style'],
                disabled_recomendet_style=data['disabled_recomendet_style']

            )).returning()
        )
        mark_changed(session)
        session.flush()
        return dict(
            id=acc.inserted_primary_key[0],
            guid=data['guid'],
            title=data['title'],
            project=data['project'],
            social=data['social'],
            impressions_per_day_limit=data['impressions_per_day_limit'],
            showCoverage=data['showCoverage'],
            retargeting=data['retargeting'],
            cost=data['cost'],
            gender=data['gender'],
            retargeting_type=data['retargeting_type'],
            brending=data['brending'],
            recomendet_type=data['recomendet_type'],
            recomendet_count=data['recomendet_count'],
            account=data['account'],
            target=data['target'],
            offer_by_campaign_unique=data['offer_by_campaign_unique'],
            unique_impression_lot=data['unique_impression_lot'],
            html_notification=data['html_notification'],
            disabled_retargiting_style=data['disabled_retargiting_style'],
            disabled_recomendet_style=data['disabled_recomendet_style']
        )