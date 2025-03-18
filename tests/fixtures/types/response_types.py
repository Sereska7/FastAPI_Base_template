"""Classes for type checking in `router.responses` module."""

import typing

import httpx

from app.pkg.models.base import BaseAPIException, Model

__all__ = ["ErrorCheckerType", "ResponseEqual"]


class ErrorCheckerType(typing.Protocol):
    def __call__(
        self,
        response: httpx.Response,
        model: typing.Type[BaseAPIException],
        relative_occurrence: bool | None = False,
    ) -> bool:
        """Protocol of calling function in
        `router.responses:response_without_error`"""


class ResponseEqual(typing.Protocol):
    def __call__(
        self,
        response: httpx.Response,
        model: Model,
        expected_status_code: int,
        exclude_from_model: typing.List[str] | None = None,
    ):
        """Protocol of calling function in `router.responses:response_equal`"""
