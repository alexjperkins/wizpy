import collections
import functools
import inspect
import sys
from typing import (
    Any, Callable, Dict, FrozenSet, List, Set, Union,
    get_origin
)

from . commands import (
    BaseCommand,
    CommandHandler,
    GoBack,
    GoForward,
    Quit
)
from . constants import (
    DESCRIPTION_ATTR_NAME,
)
from . display import cyan, green, red, prettyprint
from . execution import ExecutionHandler
from . history import MenuHistory
from . messages import (
    CONTINUE_AFTER_EXECUTION_MSG,
    DEFAULT_INPUT_MSG,
    EMPTY_RETRY_INPUT_MSG,
    EXIT_WIZARD_MSG,
    INVALID_RETRY_INPUT_MSG,
    WELCOME_MSG,
)
from . menu import MenuFactory, IMenu
from . registry import GlobalWizardRegistry


class WizardHandler:
    apis: FrozenSet = GlobalWizardRegistry.registry()
    history = MenuHistory()
    commands: Set = {GoBack, GoForward, Quit}
    command_handler = CommandHandler(history=history)  # TODO dep inj log
    execution_handler = ExecutionHandler(log=prettyprint)
    menu_factory = functools.partial(MenuFactory.build, commands=commands)

    @classmethod
    def handle(cls) -> None:
        prettyprint(cyan(WELCOME_MSG))
        cls.history.push(
            menu=cls.menu_factory(to_build_from=cls.apis)
        )

        while True:
            cls.history.current.display()

            user_input = cls._handle_input(
                msg=DEFAULT_INPUT_MSG,
                menu=cls.history.current
            )

            operation = cls.history.current.get(user_input)['service']

            # if class
            if isinstance(operation, type):
                # if command
                if issubclass(operation, BaseCommand):
                    cls.command_handler(command=operation)
                    continue

                # if class & registered to the wizard
                latest_menu = cls.menu_factory(to_build_from=operation)
                cls.history.push(menu=latest_menu)
                continue

            # if not callable, don't attempt to handle
            if callable(operation):
                cls.execution_handler.handle(func=operation)
                continue

            raise RuntimeError('Event cannot be handled')

    @classmethod
    def _handle_input(cls, *, msg: str, menu: IMenu) -> Any:
        try:
            value = input(msg)
        except EOFError:
            # keyboard interrupt
            sys.exit(1)

        if value is None:
            menu.display()
            prettyprint(EMPTY_RETRY_INPUT_MSG)
            return cls._handle_input(msg=msg, menu=menu)

        if value not in menu:
            menu.display()
            prettyprint(
                f"{INVALID_RETRY_INPUT_MSG}\n{value} is not an option.\n"
            )
            return cls._handle_input(msg=msg, menu=menu)

        return value
