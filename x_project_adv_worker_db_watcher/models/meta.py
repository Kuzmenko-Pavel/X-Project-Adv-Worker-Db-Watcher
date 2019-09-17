from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import MetaData
from zope.sqlalchemy import ZopeTransactionExtension

from x_project_adv_worker_db_watcher.models.__libs__.sql_extension import create_extension
from x_project_adv_worker_db_watcher.models.__libs__.sql_function import create_function
from x_project_adv_worker_db_watcher.models.__libs__.sql_schema import create_schema

NAMING_CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class ClsBase(object):
    pass


Base = declarative_base(cls=ClsBase, metadata=metadata)

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

create_schema(metadata, {
    'name': 'public',
})

create_extension(metadata, {
    'name': 'ltree',
})


create_function(metadata, {
    'name': 'RefreshAllMaterializedViewsConcurrently',
    'argument': "schema_arg TEXT DEFAULT 'public'",
    'drop_argument': 'schema_arg TEXT',
    'returns': 'INT',
    'body': '''
            DECLARE
              r RECORD;
            BEGIN
              FOR r IN SELECT matviewname
                       FROM pg_matviews
                       WHERE schemaname = schema_arg
              LOOP
                EXECUTE 'REFRESH MATERIALIZED VIEW CONCURRENTLY ' || schema_arg || '.' || r.matviewname;
              END LOOP;
            
              RETURN 1;
            END
            ''',
    'language': 'plpgsql'
})
