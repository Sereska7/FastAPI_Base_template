from typing import Annotated

from pydantic import SecretStr, constr

__all__ = ["NotEmptySecretStr", "NotEmptyStr"]

NotEmptyStr = Annotated[str, constr(min_length=1, strict=True)]
NotEmptySecretStr = Annotated[SecretStr, constr(min_length=1, strict=True)]
