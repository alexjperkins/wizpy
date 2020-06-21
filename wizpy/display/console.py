import functools


def _pprint(*args, msg: str, **kwargs):
    print(msg)


@functools.singledispatch
def prettyprint(msg):
    raise NotImplementedError('Unsupported Type')


@prettyprint.register(str)
def _(msg):
    _pprint(msg=msg)


@prettyprint.register(list)
def _(msg):
    _msg = '\n'.join(element for element in msg)
    _pprint(msg=_msg)


@prettyprint.register(dict)
def _(msg):
    for key, value in msg.items():
        _pprint(msg=f'{key}\t{value}\n')


@prettyprint.register(Exception)
def _(msg):
    _pprint(msg=msg)
