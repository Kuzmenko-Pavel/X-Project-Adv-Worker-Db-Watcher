from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.schema import MetaData
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

create_function(metadata, {
    'name': 'recommended_to_json',
    'argument': 'recommended_id character varying[],  offer_id_cam bigint',
    'returns': 'json',
    'body': '''
       DECLARE
        recommended json;
       BEGIN
            IF array_length(recommended_id, 1) > 0  THEN
                recommended = json_agg(T.offer_json)
                    FROM (
                         SELECT
                           TT.id,
                           ROW_TO_JSON(TT) AS offer_json
                         FROM (
                         SELECT
                                offer_sub_u.id,
                                offer_sub_u.guid,
                                offer_sub_u.title,
                                offer_sub_u.description,
                                offer_sub_u.image,
                                offer_sub_u.price,
                                offer_sub_u.url
                                FROM 
                                (
                                    SELECT
                                      offer_sub.id,
                                      offer_sub.guid,
                                      offer_sub.title,
                                      offer_sub.description,
                                      offer_sub.image,
                                      offer_sub.price,
                                      offer_sub.url,
                                      row_number() OVER (PARTITION BY offer_sub.retid) AS range_number
                                    FROM public.offer AS offer_sub
                                    WHERE offer_sub.retid = ANY (recommended_id) and offer_sub.id_cam = offer_id_cam
                                ) as offer_sub_u where offer_sub_u.range_number = 1
                              ) AS TT
                       ) AS T;    
            ELSE
                recommended = json_agg(T.offer_json)
                        FROM (
                             SELECT
                               TT.id,
                               ROW_TO_JSON(TT) AS offer_json
                             FROM (
                                    SELECT
                                      offer_sub.id,
                                      offer_sub.guid,
                                      offer_sub.title,
                                      offer_sub.description,
                                      offer_sub.image,
                                      offer_sub.price,
                                      offer_sub.url
                                    FROM public.offer AS offer_sub
                                    WHERE offer_sub.id_cam = offer_id_cam
                                    ORDER BY RANDOM() LIMIT 10
                                  ) AS TT
                           ) AS T;
            END IF;
        RETURN recommended;
        END
    ''',
    'optimizer': 'STABLE',
    'language': 'plpgsql'
})

create_function(metadata, {
    'name': 'create_recommended',
    'argument': 'offer_id_cam bigint',
    'returns': 'INT',
    'body': '''
       DECLARE
            brending boolean := false;
            styling boolean := false;
        BEGIN
            SELECT campaign.brending, campaign.styling INTO brending, styling FROM campaign WHERE id = offer_id_cam;
            
            IF brending OR styling THEN
                UPDATE offer
                SET recommended = recommended_to_json(subquery.recommended_ids, offer_id_cam)
                FROM (SELECT
                        offer_sub.id,
                        offer_sub.recommended_ids
                      FROM offer AS offer_sub
                      WHERE offer_sub.id_cam = offer_id_cam) AS subquery
                WHERE offer.id = subquery.id;
            END IF;
            RETURN 1;
        END
    ''',
    'optimizer': 'VOLATILE',
    'language': 'plpgsql'
})

create_function(metadata, {
    'name': 'offer_informer_rating_update',
    'argument': 'v_id_ofr bigint, v_id_inf bigint, v_rating double precision',
    'returns': 'INT',
    'body': '''
        DECLARE
        BEGIN
            INSERT INTO offer2informer (id_ofr, id_inf, rating)
            VALUES (v_id_ofr, v_id_inf, v_rating)
            ON CONFLICT (id_ofr, id_inf)
            DO UPDATE SET
            rating=v_rating;
            RETURN 1;
        EXCEPTION WHEN OTHERS THEN
            RETURN 1;
        END
    ''',
    'language': 'plpgsql'
})

create_function(metadata, {
    'name': 'offer_rating_update',
    'argument': 'v_id_ofr bigint, v_rating double precision',
    'returns': 'INT',
    'body': '''
        DECLARE
        BEGIN
            UPDATE offer
                SET rating=v_rating
            WHERE id=v_id_ofr;
            RETURN 1;
        EXCEPTION WHEN OTHERS THEN
            RETURN 1;
        END
    ''',
    'language': 'plpgsql'
})
