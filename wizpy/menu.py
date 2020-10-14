import abc
import functools
import logging
import sys
from collections import OrderedDict, UserDict
from typing import Any, Callable, Dict, FrozenSet, Set, Union

from . display import prettyprint, light_purple, green
from . constants import WIZARD_MENU_CLASS_ATTR_NAME


logger = logging.getLogger(__file__)


def command_options_factory(*, commands: Set) -> Dict:
    od = OrderedDict()
    for command in commands:
        od.update(
            {
                command.key: {
                    "service": command,
                    "name": command.__name__,
                    "help": command.__doc__ or '',
                }
            }
        )
    return od


class IMenu(abc.ABC):
    @abc.abstractmethod
    def display(self):
        pass


class Menu(UserDict, IMenu):
    def __init__(self, logmethod: Callable = prettyprint):
        self._logmethod = logmethod
        super().__init__()

    def display(self) -> None:
        self._logmethod(
            '\n'.join(
                f"{green(index)}:\t{service.get('name'):^16}"
                f"\t{light_purple(service.get('help')):^10}"
                for index, service in self.items()
            )
        )
        self._logmethod('\n')


class MenuFactory:
    @classmethod
    def build(
        cls,
        *,
        to_build_from: Union[type, FrozenSet[type]],
        commands: Set,
        logmethod: Callable = prettyprint
    ) -> Menu:

        build_method = {
            type: cls.build_menu_dict_from_api,  # type of objects
            frozenset: cls.build_menu_dict_from_apis,
        }

        mapping = build_method.get(
            type(to_build_from), cls._fallback
        )(to_build_from, commands)

        menu = Menu(logmethod=logmethod)
        menu.update(mapping)
        return menu

    @staticmethod
    def build_menu_dict_from_api(api: object, commands: Set, /) -> OrderedDict:
        operations = {
            str(index): operation
            for index, operation in getattr(api,  WIZARD_MENU_CLASS_ATTR_NAME).items()  # NOQA
        }

        command_options = command_options_factory(commands=commands)

        return OrderedDict({
            **operations,
            **command_options,
        })

    @staticmethod
    def build_menu_dict_from_apis(apis: FrozenSet, commands: Set, /) -> OrderedDict:
        api_menu = {
            str(index): {
                "help": api.__doc__ or '',
                "name": f"{api.__name__.replace('API', '')}",
                "service": api,
            }
            for index, api in enumerate(sorted(apis, key=lambda api: api.__name__), 1)  # NOQA
        }

        command_options = command_options_factory(commands=commands)

        return OrderedDict({
            **api_menu,
            **command_options
        })

    @classmethod
    def _fallback(cls, *args, **kwargs) -> None:
        logger.error('Failed to handle menu type: %s %s', args, kwargs)
        prettyprint(
            RuntimeError(
                'Failed to handler event exiting. See logs for more detail.'
            )
        )
        sys.exit(1)
