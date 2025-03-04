"""
Helper methods for validating that an arbitrary blob matches a given model.
"""

import functools
import typing

from pydantic import ConfigDict, TypeAdapter


T = typing.TypeVar("T")


@functools.cache
def _get_validator(model: type[T]) -> TypeAdapter[T]:
    """
    Get the validator for a given type.  This is a moderately expensive
    process, so we cache the result -- we only need to create the
    validator once for each type.
    """
    try:
        model.__pydantic_config__ = ConfigDict(extra="forbid")  # type: ignore
    except (AttributeError, TypeError):
        pass

    return TypeAdapter(model)


def validate_type(t: typing.Any, *, model: type[T]) -> T:
    """
    Check that some data matches a given type.

    We use this to e.g. check that the structured data we receive from
    Wikimedia matches our definitions, so we can use the data in our
    type-checked Python.

    See https://stackoverflow.com/a/77386216/1558022
    """
    # This is to fix an issue from the type checker:
    #
    #     Argument 1 to "__call__" of "_lru_cache_wrapper"
    #     has incompatible type "type[T]"; expected "Hashable"
    #
    assert isinstance(model, typing.Hashable)

    validator = _get_validator(model)

    return validator.validate_python(t, strict=True)
