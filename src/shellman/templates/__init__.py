"""This module contains our definitions of templates."""

from __future__ import annotations

import os
import sys
from copy import deepcopy
from importlib.metadata import entry_points
from typing import Any

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from shellman.templates.filters import FILTERS

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points  # type: ignore[assignment]  # noqa: F811
else:
    from importlib.metadata import entry_points


def _get_builtin_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _get_env(path: str) -> Environment:
    return Environment(  # noqa: S701
        loader=FileSystemLoader(path),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        auto_reload=False,
    )


builtin_env = _get_env(_get_builtin_path())


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
        self.context = context or {}
        self.__template: Template = None  # type: ignore[assignment]

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
    directory, base_template = os.path.split(base_template_path)
    try:
        return Template(directory or ".", base_template)
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
                    templates[name] = template


def _names() -> list[str]:
    return sorted(templates.keys())


def _parser_choices() -> tuple[str]:
    class TemplateChoice(tuple):
        def __contains__(self, item: str) -> bool:  # type: ignore[override]
            return super().__contains__(item) or item.startswith("path:")

    return TemplateChoice(_names())  # type: ignore[return-value]


helptext = Template(
    builtin_env,
    "helptext",
    context={"indent": 2, "option_padding": 22},
)
manpage = Template(builtin_env, "manpage.groff", context={"indent": 4})
manpage_md = Template(builtin_env, "manpage.md")
wikipage = Template(builtin_env, "wikipage.md")
usagetext = Template(builtin_env, "usagetext")

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
