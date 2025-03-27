# Jinja-context related utilities.

from __future__ import annotations

import contextlib
import json
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import argparse
    from collections.abc import Sequence

ENV_VAR_PREFIX = "SHELLMAN_CONTEXT_"
"""The prefix for environment variables that will be used as context."""
DEFAULT_JSON_FILE = ".shellman.json"
"""The default JSON file to read context from."""


def _get_cli_context(args: Sequence[str]) -> dict:
    context: dict[str, Any] = {}
    if args:
        for context_arg in args:
            if not context_arg:
                continue
            if context_arg[0] == "{":
                context.update(json.loads(context_arg))
            elif "=" in context_arg:
                name, value = context_arg.split("=", 1)
                if "." in name:
                    name_dict: dict[str, Any] = {}
                    d = name_dict
                    parts = name.split(".")
                    for name_part in parts[1:-1]:
                        d[name_part] = d = {}
                    d[parts[-1]] = value
                    context[parts[0]] = name_dict
                else:
                    context[name] = value
            # else invalid arg
    return context


def _get_env_context() -> dict:
    context = {}
    for env_name, env_value in os.environ.items():
        if env_name.startswith(ENV_VAR_PREFIX):
            context_var_name = env_name[len(ENV_VAR_PREFIX) :].lower()
            context[context_var_name] = env_value
    return context


def _get_file_context(file: str) -> dict:
    with open(file) as stream:
        return json.load(stream)


def _get_context(args: argparse.Namespace) -> dict:
    context = {}

    if args.context_file:
        context.update(_get_file_context(args.context_file))
    else:
        with contextlib.suppress(OSError):
            context.update(_get_file_context(DEFAULT_JSON_FILE))

    _update(context, _get_env_context())
    _update(context, _get_cli_context(args.context))

    return context


def _update(base: dict, added: dict) -> dict:
    for key, value in added.items():
        if isinstance(value, dict):
            base[key] = _update(base.get(key, {}), value)
        else:
            base[key] = value
    return base
