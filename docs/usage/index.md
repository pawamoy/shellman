# Usage on the Command-Line

```
Usage: shellman [-h] [-c CONTEXT [CONTEXT ...]]
                [--context-file CONTEXT_FILE]
                [-t TEMPLATE] [-m] [-o OUTPUT]
                [FILE [FILE ...]]
```

*Positional arguments:*

- `FILE`: path to the file(s) to read. Use - to read on standard input.

*Optional arguments:*

- `-h, --help`: show this help message and exit
- `-c, --context CONTEXT [CONTEXT ...]`:
  context to inject when rendering the template. You can
  pass JSON strings or key=value pairs. Example:
  `--context project=hello '{"version": [0, 3, 1]}'`.
- `--context-file CONTEXT_FILE`:
  JSON file to read context from. By default shellman
  will try to read the file '.shellman.json' in the
  current directory.
- `-t, --template TEMPLATE`:
  the Jinja2 template to use. Prefix with `path:` to
  specify the path to a custom template. Available
  templates: helptext, manpage, manpage.1, manpage.3,
  manpage.groff, manpage.markdown, manpage.md, wikipage,
  wikipage.markdown, wikipage.md
- `-m, --merge`:
  with multiple input files, merge their contents in the
  output instead of appending (default: False).
- `-o, --output OUTPUT`:
  file to write to (default: stdout). You can use the
  following variables in the output name: `{basename}`,
  `{ext}`, `{filename}` (equal to `{basename}.{ext}`),
  `{filepath}`, `{dirname}`, `{dirpath}`, and `{vcsroot}`
  (git and mercurial supported). They will be populated from
  each input file.


## Builtin templates

The available builtin templates are:

1. `helptext`: A basic help text typically printed by scripts' `--help` option.
2. `manpage`: A Groff (GNU Troff) formatted file, suitable for `man`.
3. `wikipage`: A Markdown formatted file to be used in a project's online wiki.

## Custom templates

Instead of using a builtin template, you can specify the path to a custom
template that you wrote:

```bash
shellman --template path:my/template
```

The given path can be absolute or relative.

See [How to write a template plugin](plugins.md) on this wiki,
and [Jinja2's documentation](https://jinja.palletsprojects.com/en/3.1.x/) for more
information about how to write templates.

You can also take a look at the source code for the builtin templates [on GitHub][github].

[github]: https://github.com/pawamoy/shellman/tree/master/src/shellman/templates/data

## Examples

### Basic usage

Simply pass the path to your script to shellman:

```bash
shellman my_script
```

The default template is `helptext`, so the previous example is equivalent to:

```bash
shellman --template helptext my_script
```

Instead of using the shell's redirection (`>`, `>>`),
you can pass the output path to the `-o, --output` option:

```bash
shellman -t wikipage lib/base.sh -o ./wiki/base.sh.md
```

### Previewing a man page

Here is a simple trick to see how the man page would look using man:

```bash
man <(shellman -t manpage my_script)
```

### Multiple input files

You can of course use shellman in a loop:

```bash
for file in lib/*; do
  shellman $f
done
```

...but this would be inefficient because of the process' starting time being
repeated for each file.

The most efficient way is to pass the list of files directly as argument
to shellman.

```bash
shellman lib/*
```

#### Using variable output name

This is especially useful when passing multiple files as input.
The available variables are `{basename}`,
`{ext}`, `{filename}` (equal to `{basename}.{ext}`),
`{filepath}`, `{dirname}`, `{dirpath}` and `{vcsroot}`.

```bash
shellman -t wikipage lib/* -o ./wiki/{filename}.md
```

#### Merging contents of multiple files

By default, each input file is rendered separately,
but you can ask shellman to merge the contents of multiple files
before rendering. It is done with the `-m, --merge` option:

```bash
shellman -m lib/* -o ./wiki/all_libs.md
```

It can be useful if you want to generate a single documentation
page from code that is split across multiple files.

Without the `-m` option, rendered contents for each input file
is appended in the output file:

```
brief, desc, usage, ... for script 1
brief, desc, usage, ... for script 2
...
brief, desc, usage, ... for script n
```

#### Using shellman with find

Let say you have a directory containing multiple git repositories.
Each one of these repositories has a `lib` folder with shell libraries inside.
You want to generate the man pages for each library file and output them in
the respective man directories.

```bash
shellman $(find my_dir -regex '.*/lib/.*\.sh') \
  --template manpage \
  --output {vcsroot}/man/{filename}.3
```

#### Using shellman with find and xargs

If you have thousands of file to treat,
the previous command could be too long for the interpreter.
A solution is to split the command with xargs,
treating 50 files at a time.

```bash
find big_project -iname "*.sh" | xargs -n 50 \
  shellman -twikipage -o big_project/wiki/{filename}.md
```

### Using shellman in a Makefile

If you are using a Makefile for your project,
it could be interesting to add rules to (re)generate
the documentation files when scripts or libraries
have been updated. Here is an example of Makefile
using shellman to update man pages and wiki pages:

```make
# Declare project structure
BINDIR := bin
LIBDIR := lib
MANDIR := man
WIKIDIR := wiki

# List scripts and libraries
SCRIPTS := $(sort $(shell cd $(BINDIR) && ls))
LIBRARIES := $(sort $(shell cd $(LIBDIR) && ls))

# Declare related man pages and wikipages
MANPAGES := $(addprefix $(MANDIR)/,$(addsuffix .1,$(SCRIPTS)) $(addsuffix .3,$(LIBRARIES)))
WIKIPAGES := $(addprefix $(WIKIDIR)/,$(addsuffix .md,$(SCRIPTS)) $(addsuffix .md,$(LIBRARIES)))

# Each man(1) page depends on its respective script
$(MANDIR)/%.1: $(BINDIR)/%
	shellman -tmanpage $< -o $@

# Each man(3) page depends on its respective library
$(MANDIR)/%.sh.3: $(LIBDIR)/%.sh
	shellman -tmanpage $< -o $@

# Each script wiki page depends on its respective script
$(WIKIDIR)/%.md: $(BINDIR)/%
	shellman -twikipage $< -o $@

# Each library wiki page depends on its respective library
$(WIKIDIR)/%.sh.md: $(LIBDIR)/%.sh
	shellman -twikipage $< -o $@

man: $(MANPAGES)

wiki: $(WIKIPAGES)

doc: man wiki
```

### Playing with context

When you render a template, you can change the values of the variables
by injecting "context".
What we call context here is simply a nested key-value list.
There are three ways to inject extra context in a template:

1. with command-line arguments
2. with environment variables
3. with a JSON file

The order of precedence is the same:
CLI arguments have priority over environment variables,
which have priority over JSON file context.

#### Passing context with command-line arguments

The option to pass context is `-c` or `--context`.
It accepts one or more positional arguments.
These positional arguments can have two forms:
a JSON-formatted string or a KEY=VALUE string.
The KEY part can be dot-separated to declare a nested item.
The VALUE part will always be a string.

Here are a few examples:

```bash
# These two examples are equivalent
shellman my_script --context '{"filename": "My Script"}'
shellman my_script --context filename="My Script"
```

```bash
# These two examples are NOT equivalent
shellman my_script --context '{"number": 0}'  # number is integer
shellman my_script --context number=0  # number is string
```

```bash
# These two examples are equivalent
shellman my_script -c '{"some": {"nested": {"item": "value"}}}'
shellman my_script -c some.nested.item=value
```

The context is recursively updated with each argument,
so you can add values to dictionaries without erasing them.

```bash
shellman my_script -c some.nested.item=value '{"some": {"other": {"item": 1}}}' some.hello=world
```

```json
{
  "some": {
    "nested": {
      "item": "value"
    },
    "other": {
      "item": 1
    },
    "hello": "world"
  }
}
```

But of course, if you redefine the dictionary itself,
all previous contents are lost:

```bash
shellman my_script -c some.nested.item=value some=hello
```

```json
{
  "some": "hello"
}
```

#### Passing context with environment variables

Environment variables prefixed with `SHELLMAN_CONTEXT_`
will be used to update the context.

```bash
SHELLMAN_CONTEXT_HELLO=world shellman my_script
```

```json
{
  "hello": "world"
}
```

As explained above, CLI arguments override environment variables.

```bash
SHELLMAN_CONTEXT_HELLO=world shellman my_script -c hello=universe
```

```json
{
  "hello": "universe"
}
```

There is currently no way to pass nested items with environment variables:

```bash
SHELLMAN_CONTEXT_SOME_NESTED_ITEM=value shellman my_script
```

```json
{
  "some_nested_item": "value"
}
```

#### Passing context with a JSON file

By default, `shellman` will try to read context from a file
in the current directory called `.shellman.json`.
You can specify another file with the `--context-file` option.

```bash
shellman my_script --context-file ./context/special.json
```
