from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, BigInteger, ForeignKey, select, Index, cast)
from sqlalchemy.dialects.postgresql import insert, JSON
from sqlalchemy.orm import relationship
from zope.sqlalchemy import mark_changed

from .__libs__.sql_view import create_view
from .meta import Base


class Informer(Base):
    __tablename__ = 'informer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(String(length=64), unique=True, index=True)
    title = Column(String(length=100))
    domain = Column(Integer, ForeignKey('domains.id', ondelete='CASCADE'), nullable=False)
    account = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    headerHtml = Column(String, default='')
    footerHtml = Column(String, default='')
    userCode = Column(String, default='')
    ad_style = Column(JSON, default=lambda: {})
    auto_reload = Column(SmallInteger, default=0)
    blinking = Column(SmallInteger, default=0)
    shake = Column(SmallInteger, default=0)
    dynamic = Column(Boolean, default=False)
    blinking_reload = Column(Boolean, default=True)
    shake_reload = Column(Boolean, default=True)
    shake_mouse = Column(Boolean, default=True)
    html_notification = Column(Boolean, default=True)
    place_branch = Column(Boolean, default=True)
    retargeting_branch = Column(Boolean, default=True)
    social_branch = Column(Boolean, default=True)
    rating_division = Column(Integer, default=1000)
    rating_hard_limit = Column(Boolean, default=False)

    campaigns_allowed = relationship('Campaign', secondary='campaign2informer_allowed',
                                     back_populates="informers_allowed",
                                     passive_deletes=True)
    campaigns_disallowed = relationship('Campaign', secondary='campaign2informer_disallowed',
                                        back_populates="informers_disallowed",
                                        passive_deletes=True)

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
                    domain=data['domain'],
                    account=data['account'],
                    headerHtml=data['headerHtml'],
                    footerHtml=data['footerHtml'],
                    userCode=data['userCode'],
                    ad_style=data['ad_style'],
                    auto_reload=data['auto_reload'],
                    blinking=data['blinking'],
                    shake=data['shake'],
                    dynamic=data['dynamic'],
                    blinking_reload=data['blinking_reload'],
                    shake_reload=data['shake_reload'],
                    shake_mouse=data['shake_mouse'],
                    html_notification=data['html_notification'],
                    place_branch=data['place_branch'],
                    retargeting_branch=data['retargeting_branch'],
                    social_branch=data['social_branch'],
                    rating_division=data['rating_division'],
                    rating_hard_limit=data['rating_hard_limit']
                )
            ).values(dict(
                id=data['id'],
                guid=data['guid'],
                title=data['title'],
                domain=data['domain'],
                account=data['account'],
                headerHtml=data['headerHtml'],
                footerHtml=data['footerHtml'],
                userCode=data['userCode'],
                ad_style=data['ad_style'],
                auto_reload=data['auto_reload'],
                blinking=data['blinking'],
                shake=data['shake'],
                dynamic=data['dynamic'],
                blinking_reload=data['blinking_reload'],
                shake_reload=data['shake_reload'],
                shake_mouse=data['shake_mouse'],
                html_notification=data['html_notification'],
                place_branch=data['place_branch'],
                retargeting_branch=data['retargeting_branch'],
                social_branch=data['social_branch'],
                rating_division=data['rating_division'],
                rating_hard_limit=data['rating_hard_limit']
            )).returning()
        )
        mark_changed(session)
        session.flush()


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
            Informer.headerHtml,
            Informer.footerHtml,
            Informer.userCode,
            Informer.ad_style,
            Informer.auto_reload,
            Informer.blinking,
            Informer.shake,
            Informer.dynamic,
            Informer.blinking_reload,
            Informer.shake_reload,
            Informer.shake_mouse,
            Informer.html_notification,
            Informer.place_branch,
            Informer.retargeting_branch,
            Informer.social_branch,
            Informer.rating_division,
            Informer.rating_hard_limit,
        ]).select_from(Informer),
        is_mat=True)


Index('ix_mv_informer_id', MVInformer.id, unique=True)
Index('ix_mv_informer_guid', MVInformer.guid, unique=True)
