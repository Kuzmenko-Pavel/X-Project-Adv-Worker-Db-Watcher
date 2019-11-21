# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import event
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement


class CreateDDLExtension(DDLElement):
    def __init__(self, name, *args, **kwargs):
        self.name = name


@compiler.compiles(CreateDDLExtension)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('CREATE EXTENSION IF NOT EXISTS')
    sql.append(element.name)
    sql.append(';')
    return ' '.join(sql)


class CreateDDLCallBack(DDLElement):
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback


@compiler.compiles(CreateDDLCallBack)
def compile(element, compiler, **kw):
    return element.callback


class DropDDLExtension(DDLElement):
    def __init__(self, name, *args, **kwargs):
        self.name = name


@compiler.compiles(DropDDLExtension)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('DROP EXTENSION IF EXISTS')
    sql.append(element.name)
    sql.append('CASCADE')
    sql.append(';')
    return ' '.join(sql)


def create_extension(metadata, extension):
    if not isinstance(extension, dict):
        return
    name = extension['name']
    sql_callback = extension.get('sql_callback', 'SELECT 1;')
    event.listen(
        metadata,
        'before_create',
        CreateDDLExtension(name)
    )
    event.listen(
        metadata,
        'after_create',
        CreateDDLCallBack(sql_callback)
    )

    event.listen(
        metadata,
        'after_drop',
        DropDDLExtension(name)
    )
