from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, BigInteger, ForeignKey, select, Index, cast)
from sqlalchemy.dialects.postgresql import insert
from zope.sqlalchemy import mark_changed
from .meta import Base
from .__libs__.sql_view import create_view


class Informer(Base):
    __tablename__ = 'informer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True, index=True)
    title = Column(String(length=100))
    domain = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), nullable=False)
    account = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    teasersCss = Column(String, default='')
    headerHtml = Column(String, default='')
    footerHtml = Column(String, default='')
    nonrelevant = Column(String(length=64))
    user_code = Column(String, default='')
    auto_reload = Column(SmallInteger)
    blinking = Column(SmallInteger)
    shake = Column(SmallInteger)
    blinking_reload = Column(Boolean, default=True)
    shake_reload = Column(Boolean, default=True)
    shake_mouse = Column(Boolean, default=True)
    capacity = Column(SmallInteger)
    valid = Column(Boolean)
    html_notification = Column(Boolean, default=True)
    place_branch = Column(Boolean, default=True)
    retargeting_branch = Column(Boolean, default=True)
    social_branch = Column(Boolean, default=True)
    height = Column(SmallInteger)
    width = Column(SmallInteger)
    height_banner = Column(SmallInteger)
    width_banner = Column(SmallInteger)
    range_short_term = Column(SmallInteger)
    range_long_term = Column(SmallInteger)
    range_context = Column(SmallInteger)
    range_search = Column(SmallInteger)
    retargeting_capacity = Column(SmallInteger)
    rating_division = Column(Integer, default=1000)

    @classmethod
    def upsert(cls, session, data):
        acc = session.execute(
            insert(cls.__table__).on_conflict_do_update(
                index_elements=['id'],
                set_=dict(
                    guid=data['guid'],
                    title=data['title'],
                    domain=data['domain'],
                    account=data['account'],
                    teasersCss=data['teasersCss'],
                    headerHtml=data['headerHtml'],
                    footerHtml=data['footerHtml'],
                    nonrelevant=data['nonrelevant'],
                    user_code=data['user_code'],
                    auto_reload=data['auto_reload'],
                    blinking=data['blinking'],
                    shake=data['shake'],
                    blinking_reload=data['blinking_reload'],
                    shake_reload=data['shake_reload'],
                    shake_mouse=data['shake_mouse'],
                    capacity=data['capacity'],
                    valid=data['valid'],
                    html_notification=data['html_notification'],
                    place_branch=data['place_branch'],
                    retargeting_branch=data['retargeting_branch'],
                    social_branch=data['social_branch'],
                    height=data['height'],
                    width=data['width'],
                    height_banner=data['height_banner'],
                    width_banner=data['width_banner'],
                    range_short_term=data['range_short_term'],
                    range_long_term=data['range_long_term'],
                    range_context=data['range_context'],
                    range_search=data['range_search'],
                    retargeting_capacity=data['retargeting_capacity'],
                    rating_division=data['rating_division']
                )
            ).values(dict(
                id=data['id'],
                guid=data['guid'],
                title=data['title'],
                domain=data['domain'],
                account=data['account'],
                teasersCss=data['teasersCss'],
                headerHtml=data['headerHtml'],
                footerHtml=data['footerHtml'],
                nonrelevant=data['nonrelevant'],
                user_code=data['user_code'],
                auto_reload=data['auto_reload'],
                blinking=data['blinking'],
                shake=data['shake'],
                blinking_reload=data['blinking_reload'],
                shake_reload=data['shake_reload'],
                shake_mouse=data['shake_mouse'],
                capacity=data['capacity'],
                valid=data['valid'],
                html_notification=data['html_notification'],
                place_branch=data['place_branch'],
                retargeting_branch=data['retargeting_branch'],
                social_branch=data['social_branch'],
                height=data['height'],
                width=data['width'],
                height_banner=data['height_banner'],
                width_banner=data['width_banner'],
                range_short_term=data['range_short_term'],
                range_long_term=data['range_long_term'],
                range_context=data['range_context'],
                range_search=data['range_search'],
                retargeting_capacity=data['retargeting_capacity'],
                rating_division=data['rating_division']
            )).returning()
        )
        mark_changed(session)
        session.flush()
        return dict(
            id=acc.inserted_primary_key[0],
            guid=data['guid'],
            title=data['title'],
            domain=data['domain'],
            account=data['account'],
            teasersCss=data['teasersCss'],
            headerHtml=data['headerHtml'],
            footerHtml=data['footerHtml'],
            nonrelevant=data['nonrelevant'],
            user_code=data['user_code'],
            auto_reload=data['auto_reload'],
            blinking=data['blinking'],
            shake=data['shake'],
            blinking_reload=data['blinking_reload'],
            shake_reload=data['shake_reload'],
            shake_mouse=data['shake_mouse'],
            capacity=data['capacity'],
            valid=data['valid'],
            html_notification=data['html_notification'],
            place_branch=data['place_branch'],
            retargeting_branch=data['retargeting_branch'],
            social_branch=data['social_branch'],
            height=data['height'],
            width=data['width'],
            height_banner=data['height_banner'],
            width_banner=data['width_banner'],
            range_short_term=data['range_short_term'],
            range_long_term=data['range_long_term'],
            range_context=data['range_context'],
            range_search=data['range_search'],
            retargeting_capacity=data['retargeting_capacity'],
            rating_division=data['rating_division']
        )


class MVInformer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_informer',
        select([
            Informer.id,
            Informer.guid,
            Informer.title,
            cast(Informer.domain, Integer).label('domain'),
            cast(Informer.account, Integer).label('account'),
            Informer.teasersCss,
            Informer.headerHtml,
            Informer.footerHtml,
            Informer.nonrelevant,
            Informer.user_code,
            Informer.auto_reload,
            Informer.blinking,
            Informer.shake,
            Informer.blinking_reload,
            Informer.shake_reload,
            Informer.shake_mouse,
            Informer.capacity,
            Informer.valid,
            Informer.html_notification,
            Informer.place_branch,
            Informer.retargeting_branch,
            Informer.social_branch,
            Informer.height,
            Informer.width,
            Informer.height_banner,
            Informer.width_banner,
            Informer.range_short_term,
            Informer.range_long_term,
            Informer.range_context,
            Informer.range_search,
            Informer.retargeting_capacity,
            Informer.rating_division,
        ]).select_from(Informer),
        is_mat=True)


Index('ix_mv_informer_id', MVInformer.id, unique=True)
