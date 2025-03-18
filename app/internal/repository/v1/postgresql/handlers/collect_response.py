"""Collect response module."""

from functools import wraps
from types import NoneType, UnionType
from typing import (
    Any,
    Callable,
    List,
    Optional,
    ParamSpec,
    Type,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from psycopg2.extras import RealDictRow  # type: ignore
from pydantic import TypeAdapter

from app.internal.repository.v1.postgresql.handlers.handle_exception import (
    handle_exception,
)
from app.pkg.models.base import Model
from app.pkg.models.v1.exceptions.repository import EmptyResult

__all__ = ["collect_response"]


def collect_response(fn) -> Callable:
    """Collect response from the database and convert it to the model.

    Args:
        fn: Target function that contains a query in postgresql.

    Returns:
        The model that is specified in type hints of `fn`.

    Raises:
        EmptyResult: when query of fn is not Optional or None, and it's result is Falsy.
    """

    @wraps(fn)
    @handle_exception
    async def inner(
        *args: object,
        **kwargs: object,
    ) -> Union[List[Type[Model]], Type[Model], None]:
        """Inner function that wraps the target function.
        Args:
            *args: Arbitrary arguments.
            **kwargs: Arbitrary keyword arguments.

        Returns: List[`Model`] if List is specified in the type annotations,
                or a single `Model` if `Model` is specified in the type annotations,
                or `None` if `Optional` or `None` is specified in the type annotations.
        """
        response = await fn(*args, **kwargs)
        return await process_response(fn, response)

    return inner


async def process_response(
    fn: Callable[..., Union[Type[Model], List[Type[Model]], None]],
    response: Any,
) -> Union[List[Type[Model]], Type[Model], None]:
    """Process the response and convert it to the appropriate model.

    Args:
        fn: The target function.
        response: The response from the database.

    Returns:
        The processed response in the form of the model.
    """
    return_annotation = get_type_hints(fn)["return"]
    if return_annotation is None or return_annotation is NoneType:
        return None

    origin = get_origin(return_annotation)
    is_optional = __is_optional_type(origin)

    if is_optional and response:
        return_annotation = __get_optional_type(return_annotation)
    elif is_optional and not response:
        return None

    if origin is list and not response:
        return []

    if not response:
        raise EmptyResult

    adapter = TypeAdapter(return_annotation)

    return adapter.validate_python(
        await __convert_response(
            response=response,
            annotations=str(return_annotation),
        ),
    )


async def __convert_response(
    response: RealDictRow,
    annotations: str,
) -> list[RealDictRow] | RealDictRow:
    """
    Converts the response of the request to a List of models or to a single model.
    Args:
        response: Response of aiopg query.
        annotations: Annotations of `fn`.

    Returns: List[`Model`] if List is specified in the type annotations,
            or a single `Model` if `Model` is specified in the type annotations.
    """
    r = response.copy()

    annotations = annotations.replace("typing.", "").replace("List", "list")

    if annotations.startswith("list"):
        return [await __convert_memory_viewer(item) for item in r]

    return await __convert_memory_viewer(r)


async def __convert_memory_viewer(r: RealDictRow) -> RealDictRow:
    """Convert memory viewer in bytes.

    Notes: aiopg returns memory viewer in query response,
        when in database type of cell `bytes`.
    """
    for key, value in r.items():
        if isinstance(value, memoryview):
            r[key] = value.tobytes()
    return r


def __is_optional_type(origin: ParamSpec | Type[UnionType] | type | None) -> bool:
    """Check if the type is Optional or Union.
    Args:
        origin: Type origin.

    Returns: True if the type is Optional or Union, False otherwise.
    """
    return origin in (
        Optional,
        Union,
    )


def __get_optional_type(return_annotation: Type[Model]) -> Type[Model]:
    """Get the type of Optional or Union.
    Args:
        return_annotation: Type annotation.

    Returns: Type of the Optional or Union.
    """
    origin = get_origin(return_annotation)
    if origin not in (Optional, Union):
        return return_annotation
    args = get_args(return_annotation)
    for arg in args:
        if arg is type(None):
            continue
        return arg
