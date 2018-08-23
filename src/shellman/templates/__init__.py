import os

import pkg_resources
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from .filters import FILTERS


class Template:
    def __init__(self, name, directory='', base_template='', default_format=''):
        self.name = name
        self.directory = directory or get_builtin_path(name)
        self.base_template = base_template or name
        self.default_format = default_format
        self.env = Environment(
            loader=FileSystemLoader(self.directory),
            trim_blocks=True,
            lstrip_blocks=True)
        self.env.filters.update(FILTERS)

    def get(self, format=None):
        file_name = self.base_template + (format or self.default_format)
        return self.env.get_template(file_name)


def get_plugin_templates():
    plugins = []
    for entry_point in pkg_resources.iter_entry_points(group='shellman'):
        obj = entry_point.load()
        if issubclass(obj, Template):
            plugins.append(obj)
    return plugins


def get_builtin_path(subdirectory=''):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), subdirectory)


def get_custom_template(base_template_path):
    directory, base_template = os.path.split(base_template_path)
    try:
        return Template('', directory, base_template).get()
    except TemplateNotFound:
        raise FileNotFoundError


def names():
    return sorted(templates.keys())


def parser_choices():
    class TemplateChoice(tuple):
        def __contains__(self, item):
            return super(TemplateChoice, self).__contains__(item) or item.startswith('path:')
    return TemplateChoice(names())


builtin_templates = [
    Template(name='helptext', default_format='.txt'),
    Template(name='manpage', default_format='.groff'),
    Template(name='wikipage', default_format='.md'),
]
plugin_templates = get_plugin_templates()
templates = {t.name: t for t in builtin_templates + plugin_templates}
