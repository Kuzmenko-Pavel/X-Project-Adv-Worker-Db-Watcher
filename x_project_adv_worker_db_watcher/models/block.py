from sqlalchemy import (Column, Integer, String, Boolean, SmallInteger, BigInteger, ForeignKey, select, Index, Float)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import UUIDType

from x_project_adv_worker_db_watcher.choiceTypes import BlockType
from .__libs__.sql_view import create_view
from .meta import Base


class Block(Base):
    __tablename__ = 'block'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True))
    site = Column(BigInteger, ForeignKey('site.id', ondelete='CASCADE'), nullable=False)
    account = Column(BigInteger, ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False)
    block_type = Column(ChoiceType(BlockType, impl=Integer()), nullable=False)
    headerHtml = Column(String, default='', server_default='')
    footerHtml = Column(String, default='', server_default='')
    userCode = Column(String, default='', server_default='')
    ad_style = Column(JSONB, default=lambda: {})
    auto_reload = Column(SmallInteger, default=0, server_default='0')
    blinking = Column(SmallInteger, default=0, server_default='0')
    shake = Column(SmallInteger, default=0, server_default='0')
    dynamic = Column(Boolean, default=False)
    blinking_reload = Column(Boolean, default=True)
    shake_reload = Column(Boolean, default=True)
    shake_mouse = Column(Boolean, default=True)
    html_notification = Column(Boolean, default=True)
    place_branch = Column(Boolean, default=True)
    retargeting_branch = Column(Boolean, default=True)
    social_branch = Column(Boolean, default=True)
    rating_division = Column(Integer, default=1000, server_default='1000')
    rating_hard_limit = Column(Boolean, default=False)
    disable_filter = Column(Boolean, default=False)
    time_filter = Column(Integer, nullable=True)
    click_cost_min = Column(Float, default=0, server_default='0')
    click_cost_proportion = Column(Integer, default=50, server_default='50')
    click_cost_max = Column(Float, default=100, server_default='100')
    impression_cost_min = Column(Float, default=0.1, server_default='0.1')
    impression_cost_proportion = Column(Integer, default=50, server_default='50')
    impression_cost_max = Column(Float, default=100, server_default='100')
    cost_percent = Column(Integer, default=100, server_default='100')

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVBlock(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_block',
        select([
            Block.id,
            Block.guid,
            Block.site,
            Block.account,
            Block.headerHtml,
            Block.footerHtml,
            Block.userCode,
            Block.ad_style,
            Block.auto_reload,
            Block.blinking,
            Block.shake,
            Block.dynamic,
            Block.blinking_reload,
            Block.shake_reload,
            Block.shake_mouse,
            Block.html_notification,
            Block.place_branch,
            Block.retargeting_branch,
            Block.social_branch,
            Block.rating_division,
            Block.rating_hard_limit,
            Block.disable_filter,
            Block.time_filter,
            Block.click_cost_min,
            Block.click_cost_proportion,
            Block.click_cost_max,
            Block.impression_cost_min,
            Block.impression_cost_proportion,
            Block.impression_cost_max,
            Block.cost_percent
        ]).select_from(Block),
        is_mat=True)


Index('ix_mv_informer_id', MVBlock.id, unique=True)
Index('ix_mv_informer_guid', MVBlock.guid, unique=True)
