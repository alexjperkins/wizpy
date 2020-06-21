import abc

from aws.factories import AWSClientFactory


class MissingServiceClassAttributeError(Exception):
    pass


class AWSClientMeta(type):
    def __repr__(cls):
        return f'AWS Client: {cls._service}'


class AbstractAWSClient(metaclass=AWSClientMeta):

    _service = None

    def __init_subclass__(cls):
        if cls._service is None:
            raise MissingServiceClassAttributeError(
                f'All classes extending {cls.__name__} '
                f'must define ``_service``'
            )

        setattr(cls, 'client', AWSClientFactory.build(cls._service))
