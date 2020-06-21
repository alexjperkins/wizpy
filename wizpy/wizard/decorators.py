import functools
from typing import List, Optional
import types

from wizard.constants import WIZARD_MENU_CLASS_ATTR_NAME
from wizard.registry import GlobalWizardRegistry
from wizard.util import build_wizard_api_definition


AVAILABLE_FUNCS = (
    types.FunctionType,
    types.MethodType
)


def register_wizard(cls=None, *, definition: Optional[List[str]] = None):

    if cls is None:
        return functools.partial(register_wizard, definition=definition)

    _api = (
        getattr(cls, funcname) for funcname in definition
    ) if definition else (
        func for funcname in dir(cls)
        if isinstance(
            (func := getattr(cls, funcname)),
            AVAILABLE_FUNCS
        )
    )

    setattr(
        cls,
        WIZARD_MENU_CLASS_ATTR_NAME,
        {i: build_wizard_api_definition(func) for i, func in enumerate(_api, 1)}  # NOQA
    )

    GlobalWizardRegistry.register(cls)

    return cls
