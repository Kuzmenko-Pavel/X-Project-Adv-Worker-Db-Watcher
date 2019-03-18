from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import MetaData

NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

parent_metadata = MetaData(naming_convention=NAMING_CONVENTION)


class ClsBase(object):
    pass


ParentBase = declarative_base(cls=ClsBase, metadata=parent_metadata)

ParentDBSession = scoped_session(sessionmaker(autocommit=True, autoflush=False))
