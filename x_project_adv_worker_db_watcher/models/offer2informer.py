from sqlalchemy import (Column, Integer, Float, ForeignKey)
from .meta import Base


class Offer2Informer(Base):
    __tablename__ = 'offer2informer'
    id_ofr = Column(Integer, ForeignKey('offer_place.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    id_inf = Column(Integer, ForeignKey('informer.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(Float)
    __table_args__ = (
        # {'prefixes': ['UNLOGGED']}
    )
