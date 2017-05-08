from sqlalchemy import (Column, Integer, Float, ForeignKey)
from .meta import Base


class Offer2Informer(Base):
    __tablename__ = 'offer2informer'
    id_ofr = Column(Integer, ForeignKey('campaign.id'), primary_key=True)
    id_inf = Column(Integer, ForeignKey('informer.id'), primary_key=True)
    rating = Column(Float)
