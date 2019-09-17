from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index)

from .__libs__.sql_view import create_view
from .meta import Base


class OfferAdvCategorie(Base):
    __tablename__ = 'offer2adv_category'
    id_ofr = Column(BigInteger, ForeignKey('offer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_adv_category = Column(Integer, ForeignKey('adv_categories.id', ondelete='CASCADE'), primary_key=True,
                             nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVOfferAdvCategorie(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_offer2adv_category',
        select([
            OfferAdvCategorie.id_ofr,
            OfferAdvCategorie.id_adv_category
        ]).select_from(OfferAdvCategorie),
        is_mat=True)


Index('ix_mv_campaign2device__id_cam__id_dev', MVOfferAdvCategorie.id_ofr, MVOfferAdvCategorie.id_adv_category,
      unique=True)
