from sqlalchemy import (Column, Integer, String, Boolean, BigInteger, select, Index, Float)
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import UUIDType

from x_project_adv_worker_db_watcher.choiceTypes import BlockType
from .__libs__.sql_view import create_view
from .meta import Base


class Block(Base):
    __tablename__ = 'block'
    id = Column(BigInteger, primary_key=True)
    guid = Column(UUIDType(binary=True))
    id_account = Column(BigInteger)
    id_site = Column(BigInteger)
    block_type = Column(ChoiceType(BlockType, impl=Integer()), nullable=False)
    headerHtml = Column(String)
    footerHtml = Column(String)
    userCode = Column(String)
    ad_style = Column(JSONB)
    place_branch = Column(Boolean)
    retargeting_branch = Column(Boolean)
    social_branch = Column(Boolean)
    rating_division = Column(Integer)
    rating_hard_limit = Column(Boolean)
    name = Column(String)
    block_adv_category = Column(ARRAY(BigInteger))
    click_cost_min = Column(Float)
    click_cost_proportion = Column(Integer)
    click_cost_max = Column(Float)
    impression_cost_min = Column(Float)
    impression_cost_proportion = Column(Integer)
    impression_cost_max = Column(Float)
    cost_percent = Column(Integer)
    disable_filter = Column(Boolean)
    time_filter = Column(Integer)

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
            Block.id_account,
            Block.id_site,
            Block.block_type,
            Block.headerHtml,
            Block.footerHtml,
            Block.userCode,
            Block.ad_style,
            Block.place_branch,
            Block.retargeting_branch,
            Block.social_branch,
            Block.rating_division,
            Block.rating_hard_limit,
            Block.name,
            Block.block_adv_category,
            Block.click_cost_min,
            Block.click_cost_proportion,
            Block.click_cost_max,
            Block.impression_cost_min,
            Block.impression_cost_proportion,
            Block.impression_cost_max,
            Block.cost_percent,
            Block.disable_filter,
            Block.time_filter,
        ]).select_from(Block),
        is_mat=True)


Index('ix_mv_informer_id', MVBlock.id, unique=True)
Index('ix_mv_informer_guid', MVBlock.guid, unique=True)
