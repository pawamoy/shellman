import os

from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound

from .filters import FILTERS


def get_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_env(path):
    env = Environment(loader=FileSystemLoader(path))
    env.filters.update(FILTERS)
    return env


def get_custom_template(path, ext=None):
    template = 'index'
    if ext:
        template += '.' + ext
    try:
        return get_env(os.path.abspath(path)).get_template(template)
    except TemplateNotFound:
        raise FileNotFoundError


def get_template(name, ext=None):
    template = 'index'
    if ext:
        template += '.' + ext
    return get_env(os.path.join(get_path(), name)).get_template(template)
