# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__author__ = 'kuzmenko-pavel'
from sqlalchemy import event
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement


class CreateDDLFunction(DDLElement):
    def __init__(self, name, argument, returns, body, language, optimizer, *args, **kwargs):
        self.name = name
        self.argument = argument
        self.returns = returns
        self.body = body
        self.language = language
        self.optimizer = optimizer


@compiler.compiles(CreateDDLFunction)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('CREATE OR REPLACE FUNCTION')
    sql.append(element.name)
    sql.append('(%s)' % element.argument)
    sql.append('RETURNS %s' % element.returns)
    sql.append('AS $body$ %s $body$' % element.body)
    sql.append('LANGUAGE %s' % element.language)
    sql.append(element.optimizer)
    sql.append(';')
    return ' '.join(sql)


class DropDDLFunction(DDLElement):
    def __init__(self, name, argument, *args, **kwargs):
        self.name = name
        self.argument = argument


@compiler.compiles(DropDDLFunction)
def compile(element, compiler, **kw):
    sql = list()
    sql.append('DROP FUNCTION IF EXISTS')
    sql.append(element.name)
    sql.append('(%s)' % element.argument)
    sql.append('CASCADE')
    return ' '.join(sql)


def create_function(metadata, function):
    if not isinstance(function, dict):
        return
    name = function['name']
    argument = function.get('argument', '')
    drop_argument = function.get('drop_argument', argument)
    returns = function['returns']
    body = function['body']
    language = function.get('language', 'plpgsql')
    optimizer = function.get('optimizer', 'VOLATILE')
    event.listen(
        metadata,
        'before_create',
        CreateDDLFunction(name, argument, returns, body, language, optimizer)
    )
    event.listen(
        metadata,
        'after_drop',
        DropDDLFunction(name, drop_argument, returns, body, language, optimizer)
    )
