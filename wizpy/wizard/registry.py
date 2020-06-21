import logging
logger = logging.getLogger(__file__)


class GlobalWizardRegistry():

    _registry = set()

    @classmethod
    def register(cls, api):

        if not hasattr(api, '_wizard'):
            logger.warn(
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
    def registry(cls):
        return frozenset(cls._registry)
