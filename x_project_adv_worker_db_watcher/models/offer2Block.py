__all__ = ['Offer2Informer', 'MVOfferPlace2Informer', 'MVOfferSocial2Informer']
from sqlalchemy import (Column, BigInteger, Float, ForeignKey, select, Index, Boolean)
from sqlalchemy.sql.expression import func, join, true, false, and_

from .__libs__.sql_view import create_view
from .block import Block
from .campaign import Campaign
from .meta import Base
from .offer import Offer


class Offer2Block(Base):
    __tablename__ = 'offer2informer'
    id_ofr = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_block = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    is_deleted = Column(Boolean, default=False)
    rating = Column(Float)
    __table_args__ = (
        Index('ix_offer2informer_rating', rating.desc().nullslast()),
        {'prefixes': ['UNLOGGED']}
    )


off_place = select([
    Offer.id,
    Offer.rating
]).select_from(join(
    Offer,
    Campaign,
    and_(Offer.id_cam == Campaign.id, Campaign.retargeting == false(), Campaign.social == false())
)
).alias('off_social')

off_to_inf_place = select([
    off_place.c.id.label('offer'),
    Block.id.label('block'),
    off_place.c.rating.label('rating')
]).alias('off_to_inf')

j_place = join(off_to_inf_place, Offer2Block,
               and_(off_to_inf_place.c.offer == Offer2Block.id_ofr, off_to_inf_place.c.block == Offer2Block.id_block),
               isouter=True)

off_social = select([
    Offer.id,
    Offer.rating
]).select_from(join(
    Offer,
    Campaign,
    and_(Offer.id_cam == Campaign.id, Campaign.retargeting == false(), Campaign.social == true())
)
).alias('off_social')

off_to_inf_social = select([
    off_social.c.id.label('offer'),
    Block.id.label('block'),
    off_social.c.rating.label('rating')
]).alias('off_to_inf')

j_social = join(off_to_inf_social, Offer2Block,
                and_(off_to_inf_social.c.offer == Offer2Block.id_ofr,
                     off_to_inf_social.c.block == Offer2Block.id_block), isouter=True)


class MVOfferPlace2Block(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_place2informer',
        select([
            off_to_inf_place.c.offer,
            off_to_inf_place.c.block,
            func.COALESCE(Offer2Block.rating, off_to_inf_place.c.rating, 0).label('rating')
        ]).select_from(j_place).order_by(Offer2Block.rating.desc().nullslast())
        , is_mat=True)


Index('ix_mv_offer_place2informer_offer_inf', MVOfferPlace2Block.offer, MVOfferPlace2Block.block, unique=True)
Index('ix_mv_offer_place2informer_rating', MVOfferPlace2Block.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})


class MVOfferSocial2Block(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social2informer',
        select([
            off_to_inf_social.c.offer,
            off_to_inf_social.c.block,
            func.COALESCE(Offer2Block.rating, off_to_inf_social.c.rating, 0).label('rating')
        ]).select_from(j_social).order_by(Offer2Block.rating.desc().nullslast())
        , is_mat=True)


Index('ix_mv_offer_social2informer_offer_inf', MVOfferSocial2Block.offer, MVOfferSocial2Block.block, unique=True)
Index('ix_mv_offer_social2informer_rating', MVOfferSocial2Block.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})
