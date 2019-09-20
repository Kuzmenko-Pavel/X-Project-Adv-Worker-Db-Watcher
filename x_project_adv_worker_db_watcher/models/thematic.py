from sqlalchemy import (Column, BigInteger, ForeignKey, select, Index)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils import LtreeType

from .__libs__.sql_view import create_view
from .meta import Base


class Thematic(Base):
    __tablename__ = 'thematics'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    path = Column(ARRAY(LtreeType))

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVThematic(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_thematics',
        select([
            Thematic.id_cam,
            Thematic.path,
        ]).select_from(Thematic),
        is_mat=True)


Index('ix_mv_thematics_id_cam', MVThematic.id_cam, unique=True)
Index('ix_mv_thematics_path', MVThematic.path, postgresql_using="gist")
