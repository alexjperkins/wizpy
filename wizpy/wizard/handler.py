import collections
import functools
import inspect
from typing import Any, Set

from display.console import prettyprint
from wizard.constants import (
    EMPTY_RETRY_INPUT_MSG,
    INVALID_RETRY_INPUT_MSG,
    OPERATION_INPUT_MSG,
    SERVICE_INPUT_MSG,
    WELCOME_MSG,
    WIZARD_MENU_CLASS_ATTR_NAME
)
from wizard.commands import BaseCommand, Quit
from wizard.registry import GlobalWizardRegistry


class WizardHandler:

    apis = GlobalWizardRegistry.registry()
    commands = {Quit}
    # history = collections.deque()

    @classmethod
    def handle(cls) -> None:
        services = cls.build_services_menu()
        current_menu = services

        prettyprint(WELCOME_MSG)

        while True:
            cls.printmenu(menu=current_menu)
            service_key = cls._handle_input(
                msg=SERVICE_INPUT_MSG,
                menu=current_menu
            )

            api = services.get(service_key)['service']

            # better handling
            if issubclass(api, BaseCommand):
                api.execute()

            api_menu = cls.build_api_menu(api=api)
            cls.printmenu(menu=api_menu)

            operation_key = cls._handle_input(
                msg=OPERATION_INPUT_MSG,
                menu=api_menu
            )

            operation = api_menu.get(operation_key)['service']

            kwargs = cls._gather_kwargs_from_func_signature(
                func=operation
            )

            try:
                execution = operation(**kwargs)
            except Exception as error:
                prettyprint(error)
                prettyprint("Sending user back to the original menu")
            else:
                prettyprint('\n')
                prettyprint(f'result: ')
                prettyprint(execution)
                prettyprint('\n')

    @classmethod
    def printmenu(
        cls, *, menu: collections.abc.Mapping, logmethod: callable = prettyprint
    ) -> None:
        logmethod(
            '\n'.join(
                f"{index}: {service.get('name')} \t {service.get('help')}"
                for index, service in menu.items()
            )
        )

    @classmethod
    def build_services_menu(cls) -> collections.abc.Mapping:
        apis = {
            str(index): {
                "help": api.__doc__,
                "name": f"{api.__name__.replace('API', '')}",
                "service": api,
            }
            for index, api in enumerate(sorted(cls.apis, key=lambda api: api.__name__), 1)  # NOQA
        }

        commands = cls.build_command_options()

        return collections.OrderedDict({
            **apis,
            **commands
        })

    @classmethod
    def build_api_menu(cls, *, api) -> collections.abc.Mapping:

        operations = {
            str(index): operation
            for index, operation in getattr(api,  WIZARD_MENU_CLASS_ATTR_NAME).items()
        }

        commands = cls.build_command_options()

        return collections.OrderedDict({
            **operations,
            **commands,
        })

    @classmethod
    @functools.lru_cache(maxsize=2)
    def build_command_options(cls):
        od = collections.OrderedDict()
        for command in cls.commands:
            od.update(cls._build_option_from_command(command=command))

        return od

    @classmethod
    def _handle_input(cls, *, msg: str, menu: collections.abc.Mapping) -> str:
        value = input(msg)

        if value is None:
            cls.printmenu(menu=menu)
            prettyprint(EMPTY_RETRY_INPUT_MSG)
            return cls._handle_input(msg=msg, menu=menu)

        if value not in menu:
            cls.printmenu(menu=menu)
            prettyprint(INVALID_RETRY_INPUT_MSG)
            return cls._handle_input(msg=msg, menu=menu)

        return value

    @classmethod
    def _gather_kwargs_from_func_signature(
        cls, *, func: callable
    ) -> collections.abc.Mapping:

        kwargs = {}
        params = inspect.signature(func).parameters

        for key, param in params.items():
            if param.default is not inspect._empty:
                kwargs.update(
                    cls._handle_default_arg(key=key, default_value=param.default)  # NOQA
                )
            else:
                kwargs.update(cls._handle_arg(key=key))

        return kwargs

    @classmethod
    def _handle_arg(cls, *, key: str) -> collections.abc.Mapping:
        value = input(f"{key.replace('_', ' ').title()}: ")
        if value is None:
            prettyprint('Please provide a value, this argument is required')
            cls._handle_arg(key=key)

        return {
            key: value
        }

    @classmethod
    def _handle_default_arg(cls, *, key: str, default_value: Any):
        value = input(f'{key}: (default={default_value})')
        return {
            key: value or default_value
        }

    # move to util
    @classmethod
    def _build_option_from_command(
        cls, command: BaseCommand
    ) -> collections.abc.Mapping:
        return {
            command.key: {
                "service": command,
                "name": command.__name__,
                "help": command.__doc__,
            }
        }
