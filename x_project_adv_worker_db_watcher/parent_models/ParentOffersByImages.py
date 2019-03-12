# -*- coding: UTF-8 -*-
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class ParentOfferByImages(ParentBase):
    __tablename__ = 'offers_by_images'
    id_offer = Column(ForeignKey('offers.id'), primary_key=True)
    offer = relationship('ParentOffer', foreign_keys=[id_offer], uselist=False)
    id_image = Column(ForeignKey('images.id'), primary_key=True)
    image = relationship('ParentImage', foreign_keys=[id_image], uselist=False)
