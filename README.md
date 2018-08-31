# ## \shellman

<!-- start-badges -->

[![Travis-CI Build Status](https://travis-ci.org/pawamoy/shellman.svg?branch=master)](https://travis-ci.org/pawamoy/shellman/)
[![Codacy Code Quality Status](https://api.codacy.com/project/badge/Grade/85e410da099c46d0bcf3700c563bbc2a)](https://www.codacy.com/app/Pawamoy/shellman/dashboard)
[![Codacy Code Coverage](https://api.codacy.com/project/badge/Coverage/85e410da099c46d0bcf3700c563bbc2a)](https://www.codacy.com/app/pawamoy/shellman/dashboard)
[![Updates](https://pyup.io/repos/github/pawamoy/shellman/shield.svg)](https://pyup.io/repos/github/pawamoy/shellman/)
[![PyPI Package latest release](https://img.shields.io/pypi/v/shellman.svg?style=flat)](https://pypi.python.org/pypi/shellman/)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/shellman.svg?style=flat)](https://pypi.python.org/pypi/shellman/)
[![Join the chat at https://gitter.im/pawamoy/shellman](https://badges.gitter.im/pawamoy/shellman.svg)](https://gitter.im/pawamoy/shellman)

<!-- end-badges -->

Read documentation from comments and render it with templates.

`shellman` can generate man pages, wiki pages and help text using documentation written
in shell scripts comments.

For example:

```bash
#!/bin/bash

## \brief Just a demo
## \desc This script actually does nothing.

main() {
  case "$1" in
    ## \option -h, --help
    ## Print this help and exit.
    -h|--help) shellman "$0"; exit 0 ;;
  esac
}

## \usage demo [-h]
main "$@"
```

Output when calling ``./demo -h``:

```
Usage: demo [-h]

This script actually does nothing.

Options:
  -h, --help            Print this help and exit.
```

![demo svg](demo.svg)

You can use your own templates
by specifying them with the ``--template path:my/template`` syntax.
You can also create a Python package with a "shellman" entrypoint
pointing at ``shellman.Template`` instances (or dictionaries of such).
They will then be directly available to shellman, and selectable
with the ``--template template_name`` syntax.

See http://jinja.pocoo.org/docs/2.10/templates/ for more information
on how to write Jinja2 templates.


## Installation

    [sudo -H] pip install shellman


## Documentation syntax

- Documentation lines always begin with `##` and a space.
  ```
  ## This is a doc line.
  # This is not a doc line.
  ##This is not valid because there is no space after ##.
  ```

- Documentation lines cannot be placed at the end of instructions.
  ```
  ## This will be recognized.
      ## Even with spaces or tabs before.
  echo "This will NOT be recognized" ## Ignored
  ```
  
- Documentation **tags** are available to precise the type of documentation.
  Tags are always preceded with either ``@`` or ``\`` (at or backslash).
  Example:
  ```
  ## @brief This file is the README.
  ## \desc I personally prefer backslash, I find it more readable.
  ```
  
- A documentation tag can have multiple lines of contents.
  ```
  ## \bug First line.
  ## Second line.
  ##
  ## Fourth line.
  ```

- You can leave the first line blank though.
  ```
  ## \bug
  ## First line.
  ##
  ## Third line.
  ```

- There is no restriction in the number of occurrences or number of lines per tag.
  ```
  ## \brief Although only the first brief will be used in builtin templates...
  ## \brief ...you still can write more than one.
  ```

- Documentation lines without tags are always attached to the previous tag.
  ```
  ## \note This is the first note.
  
  ## This is still the first note.
  ## \note This is another note.
  ```

- Tags can have sub-tags. The best example is the ``\function`` tag:
  ```
  ## \function some prototype or else
  ## \function-brief one-line description
  ## \function-argument arg1 some argument
  some_function() { echo "Hello"; }
  ```
- When rendering a tag's contents as text, shellman will indent and wrap it. To prevent joining
  lines that should not be joined, simply indent them with one more space or tab. Also blank
  documentation lines are kept as blank lines.
  ```
  ## \desc Starting a description.
  ## Showing a list of steps:
  ##
  ##   - do this
  ##   - and do that
  ```

## List of supported tags

You will find here the list of supported tags and examples of how to use them.

- [Author](#author)
- [Bug](#bug)
- [Brief](#brief)
- [Caveat](#caveat)
- [Copyright](#copyright)
- [Date](#date)
- [Description](#description)
- [Environment variable](#environment-variable)
- [Error](#error)
- [Example](#example)
- [Exit status](#exit-status)
- [File](#file)
- [Function](#function)
- [History](#history)
- [License](#license)
- [Note](#note)
- [Option](#option)
- [See also](#see-also)
- [Standard error](#standard-error)
- [Standard input](#standard-input)
- [Standard output](#standard-output)
- [Usage](#usage)
- [Version](#version)


### Author

    ## \author Timothée Mazzucotelli / @pawamoy / <pawamoy@pm.me>

### Bug

    ## \bug Describe a bug.
    ## This is typically a well-known bug that won't be fixed.

### Brief

    ## \brief A brief description of the script or library.
    ## You can use multiple lines, but usually one is better.

### Caveat

    ## \caveat A limitation in your code.
    ## Use as many lines as you want.

### Copyright

    ## \copyright Copyright 2018 Timothée Mazzucotelli.
    ## You could also include the text of the license.

### Date

    ## \date 2018-08-31. Or 31 Août 2018.
    ## It's just text, it will not be parsed as a date object. Prefer one line.

### Description

    ## \desc The big description.
    ## Usually takes many lines.

### Environment variable

It has a ``name`` and a ``description``.

    ## \env MY_VARIABLE And a short description. Or...
    ## \env MY_VARIABLE
    ## A longer
    ## description.

    ## \env MY_VARIABLE Actually you can mix both styles,
    ## as each new line of documentation will be appended to the description
    ## of the given environment variable.
    ## The first word will be the variable name (everything before the first space).

### Error

    ## \error Just like bugs, notes, caveats...
    ## An error is something the user should not do,
    ## something that is considered wrong or bad practice when using your script.

    ## If you want to document the standard error messages, or the exit status,
    ## see \stderr and \exit.

### Example

It has ``brief``, ``code``, ``code_lang`` and ``description`` attributes.

    ## \example The first line is the brief description.
    ## Can span multiple lines.
    ## \example-code bash
    ##   # Note the "bash" keyword on the previous line.
    ##   # It will be used in, for example, Markdown templates, for code syntax highlighting.
    ##   if this_condition; then
    ##     cd this_dir && do_that_thing
    ##   fi
    ## \example-description Now we describe the example more seriously.
    ## But you can simply skip the description if it easy enough to understand.

### Exit status

It has a ``code`` and a ``description``.

    ## \exit 0 Everything went fine.

    ## \exit 1 Something went wrong.
    ## I don't know why, really.

    ## \exit 73
    ## I had never encounter this exit code before!

    ## \exit NO_INTERNET
    ## The code can also be a string.

### File

It has a ``name`` and a ``description``.

    ## \file /etc/super_script/default_conf.rc The default configuration file for my super script.

    ## \file /dev/null
    ## I think you got it.

### Function

A function has the following attributes:
``prototype``, ``brief``, ``description``,
``arguments``, ``preconditions``, ``return_codes``,
``seealso``, ``stderr``, ``stdin`` and ``stdout``.

For now, shellman does not support too much verbosity for the attributes:
only one line can be used for each.

Each line without a tag will be appended to the description.

    ## \function say_hello(person, hello='bonjour')
    ## \function-brief Say hello (in French by default) to the given person.
    ## \function-argument hello How to say hello. Default is "bonjour".
    ## \function-precondition The person you say hello to must be a human or a dog.
    ## \function-return 0 The person was not authorized to answer back.
    ## \function-return 1 The person was human.
    ## \function-return 17 The person was a good boy.
    ## \function-stdout The person's answer will be printed on standard output.

### History

    ## \history 2018-08-31: this example was written.

    ## \history Far future:
    ## 2K stars on GitHub!


### License

    ## \license ISC License
    ##
    ## Copyright (c) 2018, Timothée Mazzucotelli
    ##
    ## Permission to use, copy, modify, and/or distribute this software for any
    ## purpose with or without fee is hereby granted, provided that the above
    ## copyright notice and this permission notice appear in all copies.
    ##
    ## THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
    ## WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
    ## MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
    ## ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
    ## WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
    ## ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
    ## OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

### Note

    ## \note If shellman does not work as expected, please file a bug on GitLab.
    ## Here is the URL: https://gitlab.com/pawamoy/shellman.

### Option

    ## \option

### See also

    ## \seealso A note about something else to look at.

### Standard Error

    ## \stderr

### Standard Input

    ## \stdin

### Standard Output

    ## \stdout

### Usage

    ## \usage

### Version

    ## \version


License
=======

Software licensed under [ISC] license.

[ISC]: https://www.isc.org/downloads/software-support-policy/isc-license/
