import collections
import json
import os

ENV_VAR_PREFIX = "SHELLMAN_CONTEXT_"
DEFAULT_JSON_FILE = ".shellman.json"


def get_cli_context(args):
    context = {}
    if args:
        for context_arg in args:
            if not context_arg:
                continue
            if context_arg[0] == "{":
                context.update(json.loads(context_arg))
            elif "=" in context_arg:
                name, value = context_arg.split("=", 1)
                if '.' in name:
                    name_dict = d = {}
                    parts = name.split('.')
                    for name_part in parts[1:-1]:
                        d[name_part] = d = {}
                    d[parts[-1]] = value
                    context[parts[0]] = name_dict
                else:
                    context[name] = value
            # else invalid arg
    return context


def get_env_context():
    context = {}
    for env_name, env_value in os.environ.items():
        if env_name.startswith(ENV_VAR_PREFIX):
            context_var_name = env_name[len(ENV_VAR_PREFIX):].lower()
            context[context_var_name] = env_value
    return context


def get_file_context(file):
    with open(file) as stream:
        return json.load(stream)


def get_context(args):
    context = {}

    if args.context_file:
        context.update(get_file_context(args.context_file))
    else:
        try:
            context.update(get_file_context(DEFAULT_JSON_FILE))
        except IOError:  # compatible python 2-3
            pass

    update(context, get_env_context())
    update(context, get_cli_context(args.context))

    return context


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
