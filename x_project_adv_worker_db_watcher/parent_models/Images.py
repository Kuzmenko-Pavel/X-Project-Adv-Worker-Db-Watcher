# -*- coding: UTF-8 -*-
from sqlalchemy import (Column, BigInteger)
from sqlalchemy_utils import URLType

from .meta import ParentBase


class Image(ParentBase):
    __tablename__ = 'images'
    id = Column(BigInteger, primary_key=True)
    url = Column(URLType)
