import functools


red = lambda tx: f"\033[91m{tx}\033[00m"  # NOQA
green = lambda tx: f"\033[92m{tx}\033[00m"  # NOQA
yellow = lambda tx: f"\033[93m{tx}\033[00m"  # NOQA
light_purple = lambda tx: f"\033[94m{tx}\033[00m"  # NOQA
purple = lambda tx: f"\033[95m{tx}\033[00m"  # NOQA
cyan = lambda tx: f"\033[96m{tx}\033[00m"  # NOQA
light_grey = lambda tx: f"\033[97m{tx}\033[00m"  # NOQA
black = lambda tx: f"\033[98m{tx}\033[00m"  # NOQA

ptab = lambda tx: f"    {tx}"  # NOQA


def _pprint(msg: str) -> None:
    print(msg)


@functools.singledispatch
def prettyprint(msg):
    try:
        _pprint(str(msg))
    except Exception:
        raise NotImplementedError('Unsupported Type')


@prettyprint.register(str)
def _(msg):
    _pprint(msg=msg)


@prettyprint.register(list)
def _(msg):
    for item in msg:
        prettyprint(item)

    print()


@prettyprint.register(dict)
def _(msg):
    print()
    for key, value in msg.items():
        prettyprint(f"{light_purple(key)}: ")
        prettyprint(value)


@prettyprint.register(Exception)
def _(msg):
    _pprint(msg=red(msg))
