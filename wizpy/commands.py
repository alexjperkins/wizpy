import abc
import functools
import logging
import sys

from typing import Any, Dict, Optional

from . console import prettyprint
from . history import MenuHistory
from . menu import IMenu


class BaseCommand(abc.ABC):
    """Base Command."""
    key: Optional[str] = None

    def __init_subclass__(cls):
        if cls.key is None:
            raise AttributeError(
                f"All classes extending {cls.__name__} "
                "must define the attribute ``key``"
            )


class Quit(BaseCommand):
    """Exits the Wizard."""
    key = "q"


class GoBack(BaseCommand):
    """Go Back."""
    key = "b"


class GoForward(BaseCommand):
    """Go Forward."""
    key = 'f'


class CommandHandler:
    def __init__(self, history: MenuHistory):
        self._log = logging.getLogger(self.__class__.__name__)
        self._history = history
        self._handlers = {
            Quit: self._handle_quit,
            GoBack: self._handle_go_back,
            GoForward: self._handle_go_forward
        }

    def __call__(self, command: BaseCommand, *args):
        return self._handlers.get(
            command,
            functools.partial(self._fallback, command=command)
        )(*args)

    def _handle_go_forward(self, *_) -> IMenu:
        prettyprint('\nGoing forward...\n')
        return self._history.go_forward()

    def _handle_go_back(self, *_) -> IMenu:
        prettyprint('\nGoing back...\n')
        return self._history.go_back()

    @classmethod
    def _handle_quit(cls, *_) -> None:
        prettyprint('\nExiting the wizard, bye for now...\n')
        sys.exit(1)

    def _fallback(self, command: Any, *args) -> None:
        self._log.error(
            "%s command isn't handled: \t "
            "args passed: %s \t"
            "Ignoring...",
            command,
            args
        )
        return None
