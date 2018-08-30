import json
import os


ENV_VAR_PREFIX = 'SHELLMAN_CONTEXT_'
DEFAULT_JSON_FILE = '.shellman.json'


def get_cli_context(args):
    context = {}
    if args:
        for context_arg in args:
            if context_arg[0] == "{":
                context.update(json.loads(context_arg))
            else:
                name, value = context_arg.split('=')
                context[name] = value
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
        except FileNotFoundError:
            pass

    context.update(get_env_context())
    context.update(get_cli_context(args.context))

    return context
