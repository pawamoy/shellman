# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2020, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# This module contains our definitions of templates.

from __future__ import annotations

from copy import deepcopy
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from shellman._internal.templates.filters import FILTERS


def _get_builtin_path() -> str:
    return str(Path(__file__).resolve().parent / "data")


def _get_env(path: str) -> Environment:
    return Environment(  # noqa: S701
        loader=FileSystemLoader(path),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        auto_reload=False,
    )


builtin_env = _get_env(_get_builtin_path())
"""The built-in Jinja environment."""


class Template:
    """Shellman templates."""

    def __init__(
        self,
        env_or_directory: str | Environment,
        base_template: str,
        context: dict[str, Any] | None = None,
        filters: dict[str, Any] | None = None,
    ):
        """Initialize the template.

        Parameters:
            env_or_directory: Jinja environment or directory to load environment from.
            base_template: The template file to use.
            context: Base context to render with.
            filters: Base filters to add to the environment.
        """
        self.env: Environment
        """The Jinja environment."""

        if isinstance(env_or_directory, Environment):
            self.env = env_or_directory
        elif isinstance(env_or_directory, str):
            self.env = _get_env(env_or_directory)
        else:
            raise TypeError(env_or_directory)

        if filters is None:
            filters = {}

        self.env.filters.update(FILTERS)
        self.env.filters.update(filters)

        self.base_template = base_template
        """The base template file."""
        self.context = context or {}
        """The base context."""
        self.__template: Template = None  # ty:ignore[invalid-assignment]

    @property
    def template(self) -> Template:
        """The corresponding Jinja template."""
        if self.__template is None:
            self.__template = self.env.get_template(self.base_template)
        return self.__template

    def render(self, **kwargs: Any) -> str:
        """Render the template.

        Parameters:
            **kwargs: Keyword arguments passed to Jinja's render method.


        Returns:
            The rendered text.
        """
        context = deepcopy(self.context)
        context.update(kwargs)
        return self.template.render(**context).rstrip("\n")


def _get_custom_template(base_template_path: str) -> Template:
    path = Path(base_template_path)
    try:
        return Template(str(path.parent), path.name)
    except TemplateNotFound as error:
        raise FileNotFoundError(base_template_path) from error


def _load_plugin_templates() -> None:
    for entry_point in entry_points(group="shellman"):  # type: ignore[call-arg]
        obj = entry_point.load()  # type: ignore[attr-defined]
        if isinstance(obj, Template):
            templates[entry_point.name] = obj  # type: ignore[attr-defined]
        elif isinstance(obj, dict):
            for name, template in obj.items():
                if isinstance(template, Template):
                    templates[name] = template  # noqa: PERF403


def _names() -> list[str]:
    return sorted(templates.keys())


def _parser_choices() -> tuple[str]:
    class TemplateChoice(tuple):  # noqa: SLOT001
        def __contains__(self, item: str) -> bool:  # ty:ignore[invalid-method-override]
            return super().__contains__(item) or item.startswith("path:")

    return TemplateChoice(_names())  # type: ignore[return-value]


helptext = Template(
    builtin_env,
    "helptext",
    context={"indent": 2, "option_padding": 22},
)
"""Template for help text."""
manpage = Template(builtin_env, "manpage.groff", context={"indent": 4})
"""Template for manpages."""
manpage_md = Template(builtin_env, "manpage.md")
"""Template for manpages in Markdown format."""
wikipage = Template(builtin_env, "wikipage.md")
"""Template for wiki pages."""
usagetext = Template(builtin_env, "usagetext")
"""Template for usage text."""

templates = {
    "usagetext": usagetext,
    "helptext": helptext,
    "manpage": manpage,
    "manpage.groff": manpage,
    "manpage.1": manpage,
    "manpage.3": manpage,
    "manpage.md": manpage_md,
    "manpage.markdown": manpage_md,
    "wikipage": wikipage,
    "wikipage.md": wikipage,
    "wikipage.markdown": wikipage,
}
"""The available templates."""
