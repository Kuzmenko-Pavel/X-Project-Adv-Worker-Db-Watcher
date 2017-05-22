# -*- coding: utf-8 -*-
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement
import sqlalchemy as db

__author__ = 'kuzmenko-pavel'


class CreateDDLViews(DDLElement):
    def __init__(self, name, selectable, is_mat=False, if_exists=False, or_replace=False,
                 tablespace_name=False):
        self.name = name
        self.selectable = selectable
        self.is_mat = is_mat
        self.or_replace = or_replace
        self.tablespace_name = tablespace_name
        self.if_exists = if_exists


@compiler.compiles(CreateDDLViews)
def compile(element, compiler, **kw):
    # Could use "CREATE OR REPLACE MATERIALIZED VIEW..."
    # but I'd rather have noisy errors
    sql = list()
    sql.append('CREATE')
    if element.or_replace and not element.is_mat:
        sql.append('OR REPLACE')
    if element.is_mat:
        sql.append('MATERIALIZED')
    sql.append('VIEW')
    if element.is_mat and element.if_exists:
        sql.append('IF NOT EXISTS')
    sql.append('%s %s AS %s' % (
        element.name,
        'TABLESPACE %s' % element.tablespace_name if element.tablespace_name else '',
        compiler.sql_compiler.process(element.selectable, literal_binds=True),
    ))
    return ' '.join(sql)


class DropDDLViews(DDLElement):
    def __init__(self, name, is_mat=False, cascade=False, if_exists=True):
        self.name = name
        self.is_mat = is_mat
        self.cascade = cascade
        self.if_exists = if_exists


@compiler.compiles(DropDDLViews)
def compile(element, compiler, **kw):
    # Could use "DROP VIEW..."
    # but I'd rather have noisy errors
    sql = list()
    sql.append('DROP')
    if element.is_mat:
        sql.append('MATERIALIZED')
    sql.append('VIEW')
    if element.if_exists:
        sql.append('IF EXISTS')
    sql.append(element.name)
    if element.cascade:
        sql.append('CASCADE')
    return ' '.join(sql)


def create_view(metadata, name, selectable, is_mat=False, if_exists=True, cascade=True, or_replace=False,
                tablespace_name=False):
    _mt = db.MetaData()
    t = db.Table(name, _mt)
    primary_key_exists = False
    for c in selectable.c:
        if '_pk' in c.name:
            primary_key_exists = True

    for c in selectable.c:
        primary_key = False
        if primary_key_exists:
            if '_pk' in c.name:
                primary_key = True
        else:
            primary_key = c.primary_key
        t.append_column(db.Column(c.name, c.type, primary_key=primary_key))

    db.event.listen(
        metadata, "after_create",
        CreateDDLViews(name, selectable, is_mat=is_mat, if_exists=if_exists, or_replace=or_replace,
                       tablespace_name=tablespace_name)
    )

    @db.event.listens_for(metadata, "after_create")
    def create_indexes(target, connection, **kw):
        if is_mat:
            for idx in t.indexes:
                idx.create(connection)

    db.event.listen(
        metadata, "before_drop",
        DropDDLViews(name, is_mat=is_mat, if_exists=if_exists, cascade=cascade)
    )
    return t
