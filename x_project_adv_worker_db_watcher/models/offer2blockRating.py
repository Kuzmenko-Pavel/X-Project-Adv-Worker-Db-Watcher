from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index, Float, Boolean)
from .__libs__.sql_view import create_view
from .meta import Base


class Offer2BlockRating(Base):
    __tablename__ = 'offer2block_rating'
    id_offer = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_block = Column(BigInteger, nullable=False, primary_key=True)
    is_deleted = Column(Boolean, default=False)
    rating = Column(Float)
    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVOfferPlace2Informer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer2block_rating',
        select([
            Offer2BlockRating.id_offer,
            Offer2BlockRating.id_block,
            Offer2BlockRating.rating
        ]).select_from(Offer2BlockRating)
        , is_mat=True)


Index('ix_mv_offer2block_rating_id_offer_id_block',
      MVOfferPlace2Informer.id_offer, MVOfferPlace2Informer.id_block, unique=True)
Index('ix_mv_offer2block_rating_id_block', MVOfferPlace2Informer.id_block)
Index('ix_mv_offer2block_rating_rating', MVOfferPlace2Informer.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})


class OfferSocial2BlockRating(Base):
    __tablename__ = 'offer_social2block_rating'
    id_offer = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_block = Column(BigInteger, nullable=False, primary_key=True)
    is_deleted = Column(Boolean, default=False)
    rating = Column(Float)
    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVOfferSocialPlace2Informer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social2block_rating',
        select([
            OfferSocial2BlockRating.id_offer,
            OfferSocial2BlockRating.id_block,
            OfferSocial2BlockRating.rating
        ]).select_from(OfferSocial2BlockRating)
        , is_mat=True)


Index('ix_mv_offer_social2block_rating_id_offer_id_block',
      MVOfferSocialPlace2Informer.id_offer, MVOfferSocialPlace2Informer.id_block, unique=True)
Index('ix_mv_offer_social2block_rating_id_block', MVOfferSocialPlace2Informer.id_block)
Index('ix_mv_offer_social2block_rating_rating', MVOfferSocialPlace2Informer.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})
