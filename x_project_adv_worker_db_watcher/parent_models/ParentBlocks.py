# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'

from sqlalchemy import Column, String, Integer, Boolean, Float, BigInteger
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy_utils import force_auto_coercion, force_instant_defaults, ChoiceType, UUIDType, LtreeType
from x_project_adv_worker_db_watcher.choiceTypes import BlockType

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentBlock(ParentBase):
    __tablename__ = 'v_worker_blocks'
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
    site_name = Column(String)
    block_adv_category = Column(ARRAY(LtreeType))
    click_cost_min = Column(Float)
    click_cost_proportion = Column(Integer)
    click_cost_max = Column(Float)
    impression_cost_min = Column(Float)
    impression_cost_proportion = Column(Integer)
    impression_cost_max = Column(Float)
    cost_percent = Column(Integer)
    disable_filter = Column(Boolean)
    time_filter = Column(Integer)
