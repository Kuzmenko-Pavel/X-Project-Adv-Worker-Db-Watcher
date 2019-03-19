__all__ = ['Offer2Informer', 'MVOfferPlace2Informer', 'MVOfferSocial2Informer']
from sqlalchemy import (Column, BigInteger, Float, ForeignKey, select, Index, Boolean)
from sqlalchemy.sql.expression import func, join, true, false, and_

from .__libs__.sql_view import create_view
from .campaign import Campaign
from .informer import Informer
from .meta import Base
from .offer import Offer


class Offer2Informer(Base):
    __tablename__ = 'offer2informer'
    id_ofr = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_inf = Column(BigInteger, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
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
    and_(Offer.campaign == Campaign.id, Campaign.retargeting == false(), Campaign.social == false())
)
).alias('off_social')

off_to_inf_place = select([
    off_place.c.id.label('offer'),
    Informer.id.label('inf'),
    off_place.c.rating.label('rating')
]).alias('off_to_inf')

j_place = join(off_to_inf_place, Offer2Informer,
               and_(off_to_inf_place.c.offer == Offer2Informer.id_ofr, off_to_inf_place.c.inf == Offer2Informer.id_inf),
               isouter=True)

off_social = select([
    Offer.id,
    Offer.rating
]).select_from(join(
    Offer,
    Campaign,
    and_(Offer.campaign == Campaign.id, Campaign.retargeting == false(), Campaign.social == true())
)
).alias('off_social')

off_to_inf_social = select([
    off_social.c.id.label('offer'),
    Informer.id.label('inf'),
    off_social.c.rating.label('rating')
]).alias('off_to_inf')

j_social = join(off_to_inf_social, Offer2Informer,
                and_(off_to_inf_social.c.offer == Offer2Informer.id_ofr,
                     off_to_inf_social.c.inf == Offer2Informer.id_inf), isouter=True)


class MVOfferPlace2Informer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_place2informer',
        select([
            off_to_inf_place.c.offer,
            off_to_inf_place.c.inf,
            func.COALESCE(Offer2Informer.rating, off_to_inf_place.c.rating, 0).label('rating')
        ]).select_from(j_place).order_by(Offer2Informer.rating.desc().nullslast())
        , is_mat=True)


Index('ix_mv_offer_place2informer_offer_inf', MVOfferPlace2Informer.offer, MVOfferPlace2Informer.inf, unique=True)
Index('ix_mv_offer_place2informer_rating', MVOfferPlace2Informer.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})


class MVOfferSocial2Informer(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer_social2informer',
        select([
            off_to_inf_social.c.offer,
            off_to_inf_social.c.inf,
            func.COALESCE(Offer2Informer.rating, off_to_inf_social.c.rating, 0).label('rating')
        ]).select_from(j_social).order_by(Offer2Informer.rating.desc().nullslast())
        , is_mat=True)


Index('ix_mv_offer_social2informer_offer_inf', MVOfferSocial2Informer.offer, MVOfferSocial2Informer.inf, unique=True)
Index('ix_mv_offer_social2informer_rating', MVOfferSocial2Informer.rating.desc().nullslast(),
      postgresql_using='btree', postgresql_with={"fillfactor": 50})
