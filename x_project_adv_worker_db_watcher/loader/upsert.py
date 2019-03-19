# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, division

__all__ = ['upsert']
__author__ = 'kuzmenko-pavel'

from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert
from zope.sqlalchemy import mark_changed


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


def upsert(session, model, rows, update_cols):
    if not rows or not update_cols:
        return
    try:
        with session.begin_nested():
            _upsert(session, model, rows, update_cols)
    except exc.IntegrityError as e:
        print(e)
        if len(rows) > 1:
            a_rows, b_rows = split_list(rows)
            with session.begin_nested():
                upsert(session, model, a_rows, update_cols)
            with session.begin_nested():
                upsert(session, model, b_rows, update_cols)
        else:
            try:
                with session.begin_nested():
                    _upsert(session, model, rows, update_cols)
            except exc.IntegrityError:
                pass


def _upsert(session, model, rows, update_cols):
    table = model.__table__
    values = [dict(zip(update_cols, x)) for x in rows]
    stmt = insert(table).values(values)
    update_cols = [c.name for c in table.c
                   if c not in list(table.primary_key.columns)
                   and c.name in update_cols]

    on_conflict_stmt = stmt.on_conflict_do_update(
        index_elements=table.primary_key.columns,
        set_={col: getattr(stmt.excluded, col) for col in update_cols}
    )

    session.execute(on_conflict_stmt)
    mark_changed(session)
