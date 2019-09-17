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
    def __iter__(self):
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                yield (key, value)

    def __repr__(self):
        rep = u"<" + self.__class__.__name__ + u" %s >" % ' '.join(['%s=%s' % (
            p, getattr(self, p)) for p in get_primary_keys(self)])
        return rep.encode('utf-8')

    def __str__(self):
        rep = u"<" + self.__class__.__name__ + u" %s >" % ' '.join(['%s=%s' % (
            p, getattr(self, p)) for p in get_primary_keys(self)])
        return rep.encode('utf-8')


ParentBase = declarative_base(cls=ClsBase, metadata=parent_metadata)

ParentDBSession = scoped_session(sessionmaker(autocommit=True, autoflush=False))
