"""Optional field function for pydantic models."""

from typing import Any

from pydantic.fields import FieldInfo

__all__ = ["OptionalField"]


def OptionalField(field: FieldInfo, default: Any = None) -> FieldInfo:  # noqa
    """Takes an already created Field and makes it optional by adding a default
    value to it.

    Args:
        field (FieldInfo): Field to make optional.
        default (Any, optional): Default value. Defaults to None.

    Returns:
        FieldInfo: Optional field.
    """

    return field.merge_field_infos(field, default=default)
