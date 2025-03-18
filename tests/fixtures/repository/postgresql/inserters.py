"""Inserters for PostgreSQL repository.

This module contains fixtures for inserting models to database using JSF
generators.
"""

from typing import Type

from pydantic import PositiveInt

from app.internal.repository.repository import Repository
from app.pkg.models.base import Model


async def __inserter(
    repository: Repository,
    cmd_model: Type[Model],
    func_name: str = "create",
    batch_insert_count: PositiveInt | None = 1,
    **kwargs,
) -> tuple[Model, Model] | list[tuple[Model, Model]]:
    """Insert generic model to database.

    Args:
        repository (Repository): Repository instance.
        cmd_model (Type[Model]): Command model.
        func_name (str): Name of the repository function to invoke. Defaults to 'create'.
        **kwargs: Model fields.

    Returns:
        tuple[Model, Model]: Tuple with result of insert and command.
    """
    if batch_insert_count > 1:
        result = []
        for _ in range(batch_insert_count):
            cmd = cmd_model.factory().build(**kwargs)
            func = getattr(repository, func_name)
            result.append((await func(cmd=cmd), cmd))
        return result
    cmd = cmd_model.factory().build(**kwargs)
    func = getattr(repository, func_name)
    return await func(cmd=cmd), cmd
