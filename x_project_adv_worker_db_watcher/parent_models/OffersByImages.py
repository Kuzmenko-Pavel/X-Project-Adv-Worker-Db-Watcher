# -*- coding: UTF-8 -*-
from sqlalchemy import (Column, ForeignKey)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy_utils import (force_auto_coercion, force_instant_defaults)

from .meta import ParentBase

force_auto_coercion()
force_instant_defaults()


class OfferByImages(ParentBase):
    __tablename__ = 'offers_by_images'

    id_offer = Column(ForeignKey('offers.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    offer = relationship('Offer', foreign_keys=[id_offer], uselist=False, passive_deletes=True)
    id_image = Column(ForeignKey('images.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    image = relationship('Image', foreign_keys=[id_image], passive_deletes=True)

    @hybrid_property
    def image_url(self):
        return self.image.url

    def __hash__(self):
        return hash((self.id_offer, self.id_image, self.offer, self.image))

    def __eq__(self, other):
        return all([getattr(self, x) == getattr(other, x) for x in
                    ['id_offer', 'id_image', 'offer', 'image']])
