import re

from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import ARRAY


class ArrayOfCustomType(ARRAY):

    def bind_expression(self, bindvalue):
        return cast(bindvalue, self)

    def result_processor(self, dialect, coltype):
        super_rp = super(ArrayOfCustomType, self).result_processor(dialect, coltype)

        def handle_raw_string(value):
            inner = re.match(r"^{(.*)}$", value).group(1)
            return inner.split(",")

        def process(value):
            return super_rp(handle_raw_string(value))

        return process
