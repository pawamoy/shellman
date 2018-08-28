import os
from copy import deepcopy
from datetime import date

import pkg_resources
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from .filters import FILTERS


class Template:
    def __init__(
        self, name, directory="", base_template="", formats=None, context=None
    ):
        self.name = name
        self.directory = directory or get_builtin_path(name)
        self.base_template = base_template or name
        self.formats = formats or []
        self.context = context or {}

        # FIXME: might need to get this out for performance when multiple file inputs/outputs
        self.env = Environment(
            loader=FileSystemLoader(self.directory),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
            auto_reload=False,
        )
        self.env.filters.update(FILTERS)

    def get(self, format=""):
        if format or self.formats:
            format = "." + (format or self.formats[0])
        file_name = self.base_template + format
        return self.env.get_template(file_name)

    def get_context(self, format=""):
        # Initialize with generic context
        format_context = deepcopy(self.context)
        for f in self.formats:
            if f in format_context:
                del format_context[f]
        # Update with specific context
        if format in self.context:
            format_context.update(self.context[format])
        return format_context

    def render(self, format="", **kwargs):
        return (
            self.get(format)
            .render(context=self.get_context(format), now=date.today(), **kwargs)
            .rstrip("\n")
        )


def get_plugin_templates():
    plugins = []
    for entry_point in pkg_resources.iter_entry_points(group="shellman"):
        obj = entry_point.load()
        if isinstance(obj, Template):
            plugins.append(obj)
    return plugins


def get_builtin_path(subdirectory=""):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), subdirectory)


def get_custom_template(base_template_path):
    directory, base_template = os.path.split(base_template_path)
    try:
        return Template("", directory, base_template).get()
    except TemplateNotFound:
        raise FileNotFoundError


def names():
    return sorted(templates.keys())


def parser_choices():
    class TemplateChoice(tuple):
        def __contains__(self, item):
            return super(TemplateChoice, self).__contains__(item) or item.startswith(
                "path:"
            )

    return TemplateChoice(names())


builtin_templates = [
    Template(
        name="helptext",
        formats=["txt"],
        context={"indent": 2, "indent_str": "  ", "option_padding": 22},
    ),
    Template(
        name="manpage",
        formats=["groff", "1", "3", "md"],
        context={"indent": 4, "indent_str": "    "},
    ),
    Template(name="wikipage", formats=["md"]),
]

plugin_templates = get_plugin_templates()
templates = {t.name: t for t in builtin_templates}

# Update with plugin templates (they are allowed to override builtin ones)
templates.update({t.name: t for t in plugin_templates})
