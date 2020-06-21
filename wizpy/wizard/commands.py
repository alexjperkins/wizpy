import abc
import sys


class BaseCommand(abc.ABC):

    key = None

    def __init_subclass__(cls):
        if cls.key is None:
            raise AttributeError(
                f"All classes extending {cls.__name__} "
                "must define the attribute ``key``"
            )

    @classmethod
    @abc.abstractmethod
    def execute(cls, **kwargs):
        pass


class Quit(BaseCommand):
    """Exits the Wizard."""

    key = 'q'

    @classmethod
    def execute(cls, **kwargs):
        sys.exit(0)
