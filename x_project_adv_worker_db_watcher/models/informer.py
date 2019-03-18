from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, BigInteger, ForeignKey, select, Index, cast,
                        Float)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import UUIDType

from .__libs__.sql_view import create_view
from .meta import Base


class Informer(Base):
    __tablename__ = 'informer'
    id = Column(BigInteger, primary_key=True, unique=True)
    guid = Column(UUIDType(binary=True), unique=True)
    title = Column(String(length=100))
    site = Column(BigInteger, ForeignKey('site.id', ondelete='CASCADE'), nullable=False)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    headerHtml = Column(String, default='')
    footerHtml = Column(String, default='')
    userCode = Column(String, default='')
    ad_style = Column(JSONB, default=lambda: {})
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
    disable_filter = Column(Boolean, default=False)
    click_cost_min = Column(Float, default=0.1)
    click_cost_proportion = Column(Integer, default=50)
    click_cost_max = Column(Float, default=100)
    impression_cost_min = Column(Float, default=0.1)
    impression_cost_proportion = Column(Integer, default=50)
    impression_cost_max = Column(Float, default=100)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVInformer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_informer',
        select([
            Informer.id,
            Informer.guid,
            Informer.title,
            Informer.site,
            Informer.account,
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
