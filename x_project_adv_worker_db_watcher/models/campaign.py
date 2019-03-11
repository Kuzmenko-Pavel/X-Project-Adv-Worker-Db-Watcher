__all__ = ['Campaign', 'MVCampaign']
from sqlalchemy import (Column, BigInteger, String, Boolean, SmallInteger, select, Index, func, join, text, table,
                        DateTime)
from sqlalchemy.dialects.postgresql import insert, JSON, ARRAY
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed
from datetime import datetime

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64), index=True)
    title = Column(String(length=100))
    social = Column(Boolean, default=False)
    showCoverage = Column(String(length=70))
    retargeting = Column(Boolean, default=False)
    capacity = Column(SmallInteger, default=1)
    cost = Column(SmallInteger, default=0)
    gender = Column(SmallInteger, default=0)
    retargeting_type = Column(String(length=10), default='offer')
    brending = Column(Boolean, default=False)
    styling = Column(Boolean, default=False)
    style_data = Column(JSON, default=lambda: {'img': '', 'head_title': '', 'button_title': ''})
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

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['id'],
                set_=dict(
                    guid=data['guid'],
                    title=data['title'],
                    social=data['social'],
                    showCoverage=data['showCoverage'],
                    retargeting=data['retargeting'],
                    capacity=data['capacity'],
                    cost=data['cost'],
                    gender=data['gender'],
                    retargeting_type=data['retargeting_type'],
                    brending=data['brending'],
                    styling=data['styling'],
                    style_data=data['style_data'],
                    style_type=data['style_type'],
                    style_class=data['style_class'],
                    style_class_recommendet=data['style_class_recommendet'],
                    recomendet_type=data['recomendet_type'],
                    recomendet_count=data['recomendet_count'],
                    account=data['account'],
                    target=data['target'],
                    offer_by_campaign_unique=data['offer_by_campaign_unique'],
                    unique_impression_lot=data['unique_impression_lot'],
                    html_notification=data['html_notification'],
                    started_time=data['started_time'],
                    thematic=data['thematic'],
                    thematic_range=data['thematic'],
                    thematics=data['thematics'],
                    thematic_day_new_auditory=data['thematic_day_new_auditory'],
                    thematic_day_off_new_auditory=data['thematic_day_off_new_auditory']
                )
            ).values(dict(
                id=data['id'],
                guid=data['guid'],
                title=data['title'],
                social=data['social'],
                showCoverage=data['showCoverage'],
                retargeting=data['retargeting'],
                capacity=data['capacity'],
                cost=data['cost'],
                gender=data['gender'],
                retargeting_type=data['retargeting_type'],
                brending=data['brending'],
                styling=data['styling'],
                style_data=data['style_data'],
                style_type=data['style_type'],
                style_class=data['style_class'],
                style_class_recommendet=data['style_class_recommendet'],
                recomendet_type=data['recomendet_type'],
                recomendet_count=data['recomendet_count'],
                account=data['account'],
                target=data['target'],
                offer_by_campaign_unique=data['offer_by_campaign_unique'],
                unique_impression_lot=data['unique_impression_lot'],
                html_notification=data['html_notification'],
                started_time=data['started_time'],
                thematic=data['thematic'],
                thematic_range=data['thematic'],
                thematics=data['thematics'],
                thematic_day_new_auditory=data['thematic_day_new_auditory'],
                thematic_day_off_new_auditory=data['thematic_day_off_new_auditory']

            )).returning()
        )
        mark_changed(session)
        session.flush()
        return dict(
            id=acc.inserted_primary_key[0],
            guid=data['guid'],
            title=data['title'],
            social=data['social'],
            showCoverage=data['showCoverage'],
            retargeting=data['retargeting'],
            capacity=data['capacity'],
            cost=data['cost'],
            gender=data['gender'],
            retargeting_type=data['retargeting_type'],
            brending=data['brending'],
            styling=data['styling'],
            style_data=data['style_data'],
            style_type=data['style_type'],
            style_class=data['style_class'],
            style_class_recommendet=data['style_class_recommendet'],
            recomendet_type=data['recomendet_type'],
            recomendet_count=data['recomendet_count'],
            account=data['account'],
            target=data['target'],
            offer_by_campaign_unique=data['offer_by_campaign_unique'],
            unique_impression_lot=data['unique_impression_lot'],
            html_notification=data['html_notification'],
            started_time=data['started_time'],
            thematic=data['thematic'],
            thematic_range=data['thematic'],
            thematics=data['thematics'],
            thematic_day_new_auditory=data['thematic_day_new_auditory'],
            thematic_day_off_new_auditory=data['thematic_day_off_new_auditory']
        )


class MVCampaign(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign',
        select([
            func.count('offer.id').over(partition_by=Campaign.id).label('offer_count'),
            Campaign.id,
            Campaign.guid,
            Campaign.social,
            Campaign.retargeting,
            Campaign.capacity,
            Campaign.cost,
            Campaign.gender,
            Campaign.retargeting_type,
            Campaign.brending,
            Campaign.styling,
            Campaign.style_data,
            Campaign.style_type,
            Campaign.style_class,
            Campaign.style_class_recommendet,
            Campaign.recomendet_type,
            Campaign.recomendet_count,
            Campaign.account,
            Campaign.target,
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
