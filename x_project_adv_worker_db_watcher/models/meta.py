from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
from x_project_adv_worker_db_watcher.models.__libs__.sql_function.function import create_function
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

create_function(metadata, {
    'name': 'RefreshAllMaterializedViewsConcurrently',
    'argument': "schema_arg TEXT DEFAULT 'public'",
    'drop_argument': 'schema_arg TEXT',
    'returns': 'INT',
    'body': '''
                DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN SELECT matviewname FROM pg_matviews WHERE schemaname = schema_arg
                    LOOP
                        EXECUTE 'REFRESH MATERIALIZED VIEW CONCURRENTLY ' || schema_arg || '.' || r.matviewname;
                    END LOOP;

                    RETURN 1;
                END
            ''',
    'language': 'plpgsql'
})
#
# create_function(metadata, {
#     'name': 'recommended_offer_to_json',
#     'argument': 'ANYARRAY',
#     'returns': 'ANYARRAY',
#     'body': '''
#         SELECT json_build_object(t.id, t.offer_json)
#             from (
#                 SELECT t1.id , row_to_json(t1) as offer_json
#                 from (
#                     SELECT offer_sub.id, offer_sub.guid, offer_sub.image  from offer as offer_sub where offer_sub.id =ANY($1)
#                      ) as t1
#                  ) as t
#         );
#     ''',
#     'language': 'SQL'
# })
