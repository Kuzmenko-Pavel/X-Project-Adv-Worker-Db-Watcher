# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import event
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement


class CreateDDLSchema(DDLElement):
    def __init__(self, name, *args, **kwargs):
        self.name = name


@compiler.compiles(CreateDDLSchema)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('CREATE SCHEMA IF NOT EXISTS')
    sql.append(element.name)
    sql.append(';')
    return ' '.join(sql)


class DropDDLSchema(DDLElement):
    def __init__(self, name, *args, **kwargs):
        self.name = name


@compiler.compiles(DropDDLSchema)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('DROP SCHEMA IF EXISTS')
    sql.append(element.name)
    sql.append('CASCADE')
    sql.append(';')
    return ' '.join(sql)


def create_schema(metadata, schema):
    if not isinstance(schema, dict):
        return
    name = schema['name']
    event.listen(
        metadata,
        'before_create',
        CreateDDLSchema(name)
    )
    event.listen(
        metadata,
        'after_drop',
        DropDDLSchema(name)
    )
