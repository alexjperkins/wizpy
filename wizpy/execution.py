import abc
import functools
import inspect
import sys
from typing import (
    Any, Callable, Dict, Generic,
    List, Optional, Tuple, TypeVar, Union,
    get_origin,
)

from . constants import (
    DESCRIPTION_ATTR_NAME,
)
from . display import prettyprint, red, green
from . messages import (
    CONTINUE_AFTER_EXECUTION_MSG,
    EXIT_WIZARD_MSG,
)


# Types
AnyFunc = Callable[[Any], Any]
T = TypeVar('T')  # NOQA


class IExecutionHandler(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def handle(cls, func: AnyFunc) -> None:
        pass


class ExecutionHandler(IExecutionHandler):
    type2str = {
        str: "String",
        int: "Int",
        bool: "Boolean [True|False]",
        List[int]: "List of Integers",
        List[str]: "List of Strings",
        List: "List of Strings",
    }

    def __init__(self, log: Callable[[Any], None]):
        self.log = log

    @classmethod
    def handle(cls, func: AnyFunc) -> None:
        kwargs: Dict = {}
        params = inspect.signature(func).parameters

        for key, param in params.items():
            cls._handle_description(func, key)
            cls._handle_type_annotation(param.annotation)

            if param.default is not inspect._empty:
                kwargs.update(
                    cls._handle_default_arg(key=key, param=param)
                )
            else:
                kwargs.update(cls._handle_arg(key=key, param=param))

        try:
            result = func(**kwargs)
        except Exception as error:
            prettyprint(red("\nERROR: "))
            prettyprint(error)
            prettyprint('\n')
        else:
            prettyprint(green("\nSUCCESS: "))
            prettyprint(result)
            prettyprint("\n")

        finally:
            to_continue = input(CONTINUE_AFTER_EXECUTION_MSG)
            if to_continue == 'n':
                prettyprint(red(EXIT_WIZARD_MSG))
                sys.exit(1)

    @classmethod
    def _handle_arg(cls, key: str, param: Any, default: bool = False) -> Dict:
        dmsg = f" (default={param.default})" if default else ""
        imsg = f"Input [{key.replace('_', ' ').title()}{dmsg}]: "

        value: str = input(imsg)

        if value is None and not default:
            prettyprint('Please provide a value, this argument is required')
            cls._handle_arg(key=key, param=param)

        parsed_value, ok = cls._parse_value(value, param.annotation)  # NOQA

        if not ok:
            prettyprint(
                f"ERROR: Invalid type. Please try again"
            )
            return cls._handle_arg(key, param, default)

        return {
            key: parsed_value or param.default
        }

    _handle_default_arg = functools.partialmethod(_handle_arg, default=True)

    @classmethod
    def _handle_type_annotation(cls, annotation: Any) -> None:
        if isinstance(annotation, str):
            if annotation.startswith('typing.'):
                prettyprint(f"Type: {annotation.replace('typing.', '')}")
            return None

        prettyprint(f"Type: {cls.type2str.get(annotation, '')}")
        return None

    @classmethod
    def _handle_description(cls, func: AnyFunc, key: str) -> None:
        if not hasattr(func, DESCRIPTION_ATTR_NAME):
            return None

        func_description = getattr(func, DESCRIPTION_ATTR_NAME)
        if key not in func_description:
            return None

        func_options = func_description[key]

        prettyprint(
            f"\nDescription: "
            f"{func_options.get('description', '')}"
        )

        foptions = func_options['options']
        if foptions is None:
            return None

        prettyprint('The following options are available:\n')
        if callable(foptions):
            prettyprint(foptions())
            return None

        prettyprint(foptions)
        return None

    @classmethod
    def _parse_value(
            cls, value: str, annotation: T
    ) -> Tuple[T, bool]:

        if annotation is int:
            return cls._parse_int(value)

        if annotation is bool:
            return cls._parse_bool(value)

        if get_origin(annotation) in {List, list}:
            return cls._parse_list(value, annotation)

        return value, True

    @classmethod
    def _parse_bool(cls, value: str) -> Tuple[bool, bool]:
        if value.lower() == "true":
            return True, True

        if value.lower() == "false":
            return False, True

        return False, False

    @classmethod
    def _parse_list(
            cls, value: str, annotation: List[T]
    ) -> Tuple[Optional[List[T]], bool]:

        if annotation == List[str] or annotation == List:
            return value.split(" "), True

        if annotation == List[int]:
            try:
                return [int(val) for val in value.split(" ")], True
            except ValueError:
                return None, False

        return None, False

    @classmethod
    def _parse_int(cls, value: str) -> Tuple[Optional[int], bool]:
        try:
            return int(value), True
        except ValueError:
            return None, False
