import logging
from typing import FrozenSet, Set

from . constants import WIZARD_MENU_CLASS_ATTR_NAME

logger = logging.getLogger(__file__)


class GlobalWizardRegistry():

    _registry: Set[type] = set()

    @classmethod
    def register(cls, api):
        if not hasattr(api, WIZARD_MENU_CLASS_ATTR_NAME):
            logger.warning(
                "Attempting to register %s without "
                "`_wizard` class attribute", api
            )
            return None

        if api not in cls._registry:
            cls._registry.add(api)
            logger.info(
                "%s registered", api.__name__
            )
            return api

        return api

    @classmethod
    def registry(cls) -> FrozenSet:
        return frozenset(cls._registry)
