from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import LtreeType

from .__libs__.sql_view import create_view
from .meta import Base


class OfferCategories(Base):
    __tablename__ = 'offer_categories'
    id_offer = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    path = Column(ARRAY(LtreeType))

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVOfferCategories(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_categories',
        select([
            OfferCategories.id_offer,
            OfferCategories.path,
        ]).select_from(OfferCategories),
        is_mat=True)


Index('ix_mv_offer_categories_id_offer', MVOfferCategories.id_offer, unique=True)
Index('ix_mv_offer_categories_path', MVOfferCategories.path, postgresql_using="gist")
