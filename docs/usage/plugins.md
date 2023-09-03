# Write a template plugin

To show how to write a template plugin,
we will create a new, minimal Python package.

Its structure will be like the following:

```
.
├── setup.py
└── src
    └── package_name
        ├── __init__.py
        └── data
            └── my_template
```

In `src/package_name/__init__.py`,
we are simply going to import the `Template` class
from `shellman`, and define an instance of it:

```python
# __init__.py

import os
from shellman import Template

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

my_template = Template(data_path, "my_template")
```

In `setup.py`, we then add a `shellman` entrypoint pointing to that template:

```python
# setup.py

from setuptools import setup

setup(
    ...,
    entrypoints={
        "shellman": [
            "my_template_name = package_name:my_template"
        ]
    }
)
```

Instead of pointing to an instance of Template, you can also point to
a dictionary of templates. This is useful if you want to set aliases for
the same template (like `my_template`, `my_template.md`, `my_template.markdown`).

```python
# __init__.py

import os
from shellman import Template

data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

my_template = Template(data_path, "my_template")

template_dict = {
    "my_template": my_template,
    "my_template.md": my_template,
    "my_template.markdown": my_template,
}
```

```python
# setup.py

from setuptools import setup

setup(
    ...,
    entrypoints={
        "shellman": [
            "unused_dict_name = package_name:template_dict"
        ]
    }
)
```

Similarly, you could do it with entrypoints only:

```python
# setup.py

from setuptools import setup

setup(
    ...,
    entrypoints={
        "shellman": [
            "my_template = package_name:my_template",
            "my_template.md = package_name:my_template",
            "my_template.markdown = package_name:my_template"
        ]
    }
)
```

## The template itself

Please read [Jinja2's documentation](http://jinja.pocoo.org/docs/2.10/)
for more information about how to write templates.

You can also take a look at the source code for the builtin templates [on GitHub][github].

[github]: https://github.com/pawamoy/shellman/tree/master/src/shellman/templates/data

## Adding context and Jinja filters

You can specify a default context and default filters
to use within your template:

```python
def do_url(obj):
  return "https://{}/{}/{}".format(obj.domain, obj.namespace, obj.name)


my_template = Template(
    data_path,
    "my_template",
    context={
        "indent": 4
    },
    filters={
        "url": do_url
    })
```

In your template, you will then have access to the `{{ my_object|url }}` filter,
as well as the `{{ indent }}` variable, which could be used like
`{{ indent * " " }}`.
