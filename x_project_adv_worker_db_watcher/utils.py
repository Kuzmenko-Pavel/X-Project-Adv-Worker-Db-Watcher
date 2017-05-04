import linecache
import sys

import trafaret as T

TRAFARET_CONF = T.Dict({
    T.Key('database'): T.String(),
    T.Key('amqp'): T.String(),
})


def exception_message():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
