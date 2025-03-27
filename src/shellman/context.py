"""Deprecated. Import directly from `shellman` instead."""

# YORE: Bump 2: Remove file.

import warnings
from typing import Any

from shellman._internal import context


def __getattr__(name: str) -> Any:
    warnings.warn(
        "Importing from 'shellman.context' is deprecated. Import directly from 'shellman' instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return getattr(context, name)
