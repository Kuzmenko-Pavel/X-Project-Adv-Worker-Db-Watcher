from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class ClsBase(object):

    def __json__(self, request):
        json_exclude = getattr(self, '__json_exclude__', set())
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_') and key not in json_exclude:
                result[key] = value
        return result

    def __iter__(self):
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                yield (key, value)

    def __repr__(self):
        rep = u"<" + self.__class__.__name__ + u">"
        return rep.encode('utf-8')

    def __str__(self):
        rep = u"<" + self.__class__.__name__ + u">"
        return rep.encode('utf-8')


Base = declarative_base(cls=ClsBase, metadata=metadata)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

