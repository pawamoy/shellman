# List of supported tags

You will find here the list of supported tags and examples of how to use them.

### Author

The author tag is used to declare authors, usually one per tag.

**Syntax:**

```
## \author TEXT...
```

**Example:**

```
## \author Timothée Mazzucotelli / @pawamoy / <pawamoy@pm.me>
## \author Another random author
```

**In templates:**

- Reference: `{% for author in shellman.doc.author %}`
- `{{ author.text }}`: the text written after the tag.

### Bug

The bug tag is used to tell about bugs, usually one per tag, on several lines.

**Syntax:**

```
## \bug TEXT...
```

**Example:**

```
## \bug Describe a bug.
## This is typically a well-known bug that won't be fixed.
```

**In templates:**

- Reference: `{% for bug in shellman.doc.bug %}`
- `{{ bug.text }}`: the text written after the tag.

### Brief

The brief tag is used to briefly tell what the script does.

**Syntax:**

```
## \brief TEXT...
```

**Example:**

```
## \brief A brief description of the script or library.
## You can use multiple lines, but usually one is better.
```

**In templates:**

- Reference: `{% for brief in shellman.doc.brief %}`
- `{{ brief.text }}`: the text written after the tag.

### Caveat

The caveat tag is used to tell about limitations,
usually one per tag, on several lines.

**Syntax:**

```
## \caveat TEXT...
```

**Example:**

```
## \caveat A limitation in your code.
## Use as many lines as you want.
```

**In templates:**

- Reference: `{% for caveat in shellman.doc.caveat %}`
- `{{ caveat.text }}`: the text written after the tag.

### Copyright

The copyright tag is used to declare some copyright on the file.

**Syntax:**

```
## \copyright TEXT...
```

**Example:**

```
## \copyright Copyright 2018 Timothée Mazzucotelli.
## You could also include the text of the license.
```

**In templates:**

- Reference: `{% for copyright in shellman.doc.copyright %}`
- `{{ copyright.text }}`: the text written after the tag.

### Date

The date tag is used to declare the date of the last update/version.

**Syntax:**

```
## \date TEXT...
```

**Example:**

```
## \date 2018-08-31. Or 31 Août 2018.
## It's just text, it will not be parsed as a date object. Prefer one line.
```

**In templates:**

- Reference: `{% for date in shellman.doc.date %}`
- `{{ date.text }}`: the text written after the tag.

### Description

The description tag is used to write the description of the script.

**Syntax:**

```
## \desc TEXT...
```

**Example:**

```
## \desc The big description.
## Usually takes many lines.
```
**In templates:**

- Reference: `{% for desc in shellman.doc.desc %}`
- `{{ desc.text }}`: the text written after the tag.

### Environment variable

The environment variable tag is used to declare the environment variables
used in the script.

**Syntax:**

```
## \env NAME DESCRIPTION...
```

**Example:**

```
## \env MY_VARIABLE And a short description. Or...

## \env MY_VARIABLE
## A longer
## description.

## \env MY_VARIABLE Actually you can mix both styles,
## as each new line of documentation will be appended to the description
## of the given environment variable.
## The first word will be the variable name (everything before the first space).
```

**In templates:**

- Reference: `{% for env in shellman.doc.env %}`
- `{{ env.name }}`: the name of the environment variable (`MY_VARIABLE`).
- `{{ env.description }}`: the description of the environment variable.

### Error

The error tag is used to write about typical errors when using the script.

**Syntax:**

```
## \error TEXT...
```

**Example:**

```
## \error Just like bugs, notes, caveats...
## An error is something the user should not do,
## something that is considered wrong or bad practice when using your script.

## If you want to document the standard error messages, or the exit status,
## see \stderr and \exit.
```

**In templates:**

- Reference: `{% for error in shellman.doc.error %}`
- `{{ error.text }}`: the text written after the tag.

### Example

The example tag is used to add examples of usage.

**Syntax:**

```
## \example BRIEF...
[## \example-code [LANG]
 ##   CODE...
]
[## \example-description DESCRIPTION...]
```

**Example:**

```
## \example The first line is the brief description.
## Can span multiple lines.
## \example-code bash
##   # Note the "bash" keyword on the previous line.
##   # It will be used, for example, in Markdown templates, for code syntax highlighting.
##   if this_condition; then
##     cd this_dir && do_that_thing
##   fi
## \example-description Now we describe the example more seriously.
## But you can simply skip the description if it easy enough to understand.
```

**In templates:**

- Reference: `{% for example in shellman.doc.example %}`
- `{{ example.brief }}`: the brief explanation / title of the example.
- `{{ example.code }}`: the code of the example.
- `{{ example.code_lang }}`: the language specified after \example-code if any.
- `{{ example.description }}`: the description of what the example does.

### Exit status

The exit status tag is used to declare what exit codes are returned, and when/why.

**Syntax:**

```
## \exit CODE DESCRIPTION...
```

**Example:**

```
## \exit 0 Everything went fine.

## \exit 1 Something went wrong.
## I don't know why, really.

## \exit 73
## I had never encounter this exit code before!

## \exit NO_INTERNET
## The code can also be a string.
```

**In templates:**

- Reference: `{% for exit in shellman.doc.exit %}`
- `{{ exit.code }}`: the exit code.
- `{{ exit.description }}`: the description of the event
  (when the script exits with this code).

### File

The file tag is used to tell about the files used by the script.

**Syntax:**

```
## \file NAME DESCRIPTION...
```

**Example:**

```
## \file /etc/super_script/default_conf.rc The default configuration file for my super script.

## \file /dev/null
## I think you got it.
```

**In templates:**

- Reference: `{% for file in shellman.doc.file %}`
- `{{ file.name }}`: the name of the file, usually its absolute path.
- `{{ file.description }}`: the description of how the file is used.

### Function

The function tag is used to document a function.

**Syntax:**

```
## \function PROTOTYPE
[## DESCRIPTION...]
[## \function-brief BRIEF]
[## \function-argument NAME DESCRIPTION]...
[## \function-precondition DESCRIPTION]...
[## \function-return CODE DESCRIPTION]...
[## \function-seealso TEXT]...
[## \function-stdin TEXT]...
[## \function-stderr TEXT]...
[## \function-stdout TEXT]...
```

For now, shellman does not support too much verbosity for the attributes:
only one line can be used for each.

Each line without a tag will be appended to the description.

**Example:**

```
## \function say_hello(person, hello='bonjour')
## \function-brief Say hello (in French by default) to the given person.
## \function-precondition The person you say hello to must be a human or a dog.
## \function-argument hello How to say hello. Default is "bonjour".
## \function-return 0 The person was not authorized to answer back.
## \function-return 1 The person was human.
## \function-return 17 The person was a good boy.
## \function-stdout The person's answer will be printed on standard output.
```

**In templates:**

- Reference: `{% for function in shellman.doc.function %}`
- `{{ function.prototype }}`: the function prototype.
- `{{ function.brief }}`: a brief explanation.
- `{{ function.description }}`: a longer explanation.
- `{{ function.arguments }}`: the list of arguments.
- `{{ function.preconditions }}`: the list of preconditions.
- `{{ function.return_codes }}`: the list of return codes.
- `{{ function.seealso }}`: the list of "see also".
- `{{ function.stderr }}`: the list of standard error messages.
- `{{ function.stdin }}`: the list of standard input messages.
- `{{ function.stdout }}`: the list of standard output messages.

### History

The history tag is used to write about the history of the project.
Interesing dates, change of maintainer, etc.

**Syntax:**

```
## \history TEXT...
```

**Example:**

```
## \history 2018-08-31: this example was written.

## \history Far future:
## 2K stars on GitHub!
```

**In templates:**

- Reference: `{% for history in shellman.doc.history %}`
- `{{ history.text }}`: the text written after the tag.

### License

The license tag is used to write licensing information.

**Syntax:**

```
## \license TEXT...
```

**Example:**

```
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
```

**In templates:**

- Reference: `{% for license in shellman.doc.license %}`
- `{{ license.text }}`: the text written after the tag.

### Note

The note tag is used to write a note about something.

**Syntax:**

```
## \note TEXT...
```

**Example:**

```
## \note If shellman does not work as expected, please file a bug on GitHub.
## Here is the URL: https://github.com/pawamoy/shellman.
```

**In templates:**

- Reference: `{% for note in shellman.doc.note %}`
- `{{ note.text }}`: the text written after the tag.

### Option

The option tag is used to document one of your script options.

**Syntax:**

```
## \option SIGNATURE
## DESCRIPTION...
[## \option-default DEFAULT]
[## \option-group GROUP]
```

`SIGNATURE` being `[short option, ][long option ][positional arguments]`.

**Example:**

```
## \option -h, --help
## Print this help and exit.
## \option-group General options

## \option -c, --context CONTEXT...
## Inject specified context into the template.
## Context can be a KEY=VALUE string or a JSON string.

## \option --easter-egg
## \option-default False
## \option-group Experimental options
## Activate the easter-egg.
```

**In templates:**

- Reference: `{% for option in shellman.doc.option %}`
- `{{ option.short }}`: the short option if any.
- `{{ option.long }}`: the long option if any.
- `{{ option.positional }}`: the option's positional arguments if any.
- `{{ option.default }}`: the default value of the option.
- `{{ option.group }}`: the option's group.
- `{{ option.description }}`: the option's description.
- `{{ option.signature }}`: the option's signature.

### See also

The see also tag is used to mention other related things
(websites, tools, etc.).

**Syntax:**

```
## \seealso TEXT...
```

**Example:**

```
## \seealso A note about something else to look at.
```

**In templates:**

- Reference: `{% for seealso in shellman.doc.seealso %}`
- `{{ seealso.text }}`: the text written after the tag.

### Standard Error

The standard error tag is used to tell what is written on the standard error,
and when/why.

**Syntax:**

```
## \stderr TEXT...
```

**Example:**

```
## \stderr The download progression is printed on standard error.
```

**In templates:**

- Reference: `{% for stderr in shellman.doc.stderr %}`
- `{{ stderr.text }}`: the text written after the tag.

### Standard Input

The standard input tag is used to tell what is expected on the standard input,
and when/why.

**Syntax:**

```
## \stdin TEXT...
```

**Example:**

```
## \stdin Standard input expects JSON formatted text.
```

**In templates:**

- Reference: `{% for stdin in shellman.doc.stdin %}`
- `{{ stdin.text }}`: the text written after the tag.

### Standard Output

The standard output tag is used to tell what is written on the standard output,
and when/why.

**Syntax:**

```
## \stdout TEXT...
```

**Example:**

```
## \stdout This script prints your geolocation on standard output.
```

**In templates:**

- Reference: `{% for stdout in shellman.doc.stdout %}`
- `{{ stdout.text }}`: the text written after the tag.

### Usage

The usage tag is used to show how to use the script.

**Syntax:**

```
## \usage PROGRAM [COMMAND...]
```

**Example:**

```
## \usage shellman [-h] [-c CONTEXT...] [--context-file FILE] [-t TEMPLATE] [-m] [-o OUTPUT] [FILE [FILE ...]]

## \usage my_script on
## \usage my_script off
```

**In templates:**

- Reference: `{% for usage in shellman.doc.usage %}`
- `{{ usage.program }}`: the program name (name of the executable).
- `{{ usage.command }}`: the command string.

### Version

The version tag is used to denotate the current version of the script.

**Syntax:**

```
## \version TEXT...
```

**Example:**

```
## \version 1.3.0
```

**In templates:**

- Reference: `{% for version in shellman.doc.version %}`
- `{{ version.text }}`: the text written after the tag.
