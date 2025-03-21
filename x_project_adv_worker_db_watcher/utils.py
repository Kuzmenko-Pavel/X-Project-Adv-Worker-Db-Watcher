import trafaret as t

TRAFARET_CONF = t.Dict({
    t.Key('postgres'): t.Dict({
        t.Key('uri'): t.String(),
    }),
    t.Key('parent_postgres'): t.Dict({
        t.Key('uri'): t.String(),
    }),
    t.Key('amqp'): t.String(),
    t.Key('loader'): t.Dict({
        t.Key('offer'): t.Dict({
            t.Key('limit'): t.Int(gte=1, lte=2000000),
        }),
    }),
})


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        self[k] = Map(v)
                    else:
                        self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    self[k] = Map(v)
                else:
                    self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]
