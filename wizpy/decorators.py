import collections
import inspect
import functools
from typing import Callable, List, Optional, Union
import types

from . constants import (
    DESCRIPTION_ATTR_NAME,
    WIZARD_MENU_CLASS_ATTR_NAME
)
from . registry import GlobalWizardRegistry
from . util import build_wizard_api_definition

from . exceptions import AddingParamDescriptionToMissingParamError


_AVAILABLE_FUNCS = (
    types.FunctionType,
    types.MethodType
)


def register_wizard(cls=None, *, definition: Optional[List[str]] = None):
    if cls is None:
        return functools.partial(register_wizard, definition=definition)

    api = (
        getattr(cls, funcname) for funcname in definition
    ) if definition else (
        func for funcname in dir(cls)
        if isinstance(
            (func := getattr(cls, funcname)),
            _AVAILABLE_FUNCS
        )
    )

    setattr(
        cls,
        WIZARD_MENU_CLASS_ATTR_NAME,
        {i: build_wizard_api_definition(func) for i, func in enumerate(api, 1)}  # NOQA
    )
    GlobalWizardRegistry.register(cls)
    return cls


def add_parameter_description(
        func=None, *, parameter: str, description: str,
        options: Optional[Union[Callable, List]] = None
):
    def decorator(func):
        if parameter not in inspect.signature(func).parameters:
            raise AddingParamDescriptionToMissingParamError(
                f"`{parameter}` is not defined in `{func.__name__}` signature"
            )

        if not hasattr(func, DESCRIPTION_ATTR_NAME):
            setattr(func, DESCRIPTION_ATTR_NAME, collections.OrderedDict())

        to_update = getattr(func, DESCRIPTION_ATTR_NAME)
        to_update.update(
            {
                parameter: {
                    "description": description,
                    "options": options,
                }
            }
        )
        return func

    return decorator
