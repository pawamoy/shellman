import os
from copy import deepcopy

import pkg_resources
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from .filters import FILTERS


def get_builtin_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def get_env(path):  # nosec
    return Environment(
        loader=FileSystemLoader(path),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
        auto_reload=False,
    )


builtin_env = get_env(get_builtin_path())


class Template:
    def __init__(self, env_or_directory, base_template, context=None, filters=None):
        if isinstance(env_or_directory, Environment):
            self.env = env_or_directory
        elif isinstance(env_or_directory, str):
            self.env = get_env(env_or_directory)
        else:
            raise ValueError(env_or_directory)

        if filters is None:
            filters = {}

        self.env.filters.update(FILTERS)
        self.env.filters.update(filters)
        self.base_template = base_template
        self.context = context or {}
        self.__template = None

    @property
    def template(self):
        if self.__template is None:
            self.__template = self.env.get_template(self.base_template)
        return self.__template

    def render(self, **kwargs):
        context = deepcopy(self.context)
        context.update(kwargs)
        return self.template.render(**context).rstrip("\n")


def get_custom_template(base_template_path):
    directory, base_template = os.path.split(base_template_path)
    try:
        return Template(directory or ".", base_template)
    except TemplateNotFound:
        raise FileNotFoundError


def load_plugin_templates():
    for entry_point in pkg_resources.iter_entry_points(group="shellman"):
        obj = entry_point.load()
        if isinstance(obj, Template):
            templates[entry_point.name] = obj
        elif isinstance(obj, dict):
            for name, template in obj.items():
                if isinstance(template, Template):
                    templates[name] = template


def names():
    return sorted(templates.keys())


def parser_choices():
    class TemplateChoice(tuple):
        def __contains__(self, item):
            return super(TemplateChoice, self).__contains__(item) or item.startswith(
                "path:"
            )

    return TemplateChoice(names())


helptext = Template(
    builtin_env,
    "helptext",
    context={"indent": 2, "option_padding": 22},
)
manpage = Template(
    builtin_env, "manpage.groff", context={"indent": 4}
)
manpage_md = Template(builtin_env, "manpage.md")
wikipage = Template(builtin_env, "wikipage.md")

templates = {
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
