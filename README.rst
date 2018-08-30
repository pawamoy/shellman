========
Shellman
========

.. start-badges


|travis|
|codacygrade|
|codacycoverage|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Pawamoy/shellman.svg?branch=master
    :target: https://travis-ci.org/Pawamoy/shellman/
    :alt: Travis-CI Build Status

.. |codacygrade| image:: https://api.codacy.com/project/badge/Grade/85e410da099c46d0bcf3700c563bbc2a
    :target: https://www.codacy.com/app/Pawamoy/shellman/dashboard
    :alt: Codacy Code Quality Status

.. |codacycoverage| image:: https://api.codacy.com/project/badge/Coverage/85e410da099c46d0bcf3700c563bbc2a
    :target: https://www.codacy.com/app/Pawamoy/shellman/dashboard
    :alt: Codacy Code Coverage

.. |pyup| image:: https://pyup.io/repos/github/Pawamoy/shellman/shield.svg
    :target: https://pyup.io/repos/github/Pawamoy/shellman/
    :alt: Updates

.. |version| image:: https://img.shields.io/pypi/v/shellman.svg?style=flat
    :target: https://pypi.python.org/pypi/shellman/
    :alt: PyPI Package latest release

.. |wheel| image:: https://img.shields.io/pypi/wheel/shellman.svg?style=flat
    :target: https://pypi.python.org/pypi/shellman/
    :alt: PyPI Wheel

.. |gitter| image:: https://badges.gitter.im/Pawamoy/shellman.svg
    :target: https://gitter.im/Pawamoy/shellman
    :alt: Join the chat at https://gitter.im/Pawamoy/shellman



.. end-badges

Read documentation from comments and render it with templates.

``shellman`` can generate man pages, wiki pages and help text using documentation written
in a shell script's comments.

For example:

.. code:: bash

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


Output when calling ``./demo -h``:

.. code::

    Usage: demo [-h]

    This script actually does nothing.

    Options:
      -h, --help            Print this help and exit.


.. image:: demo.svg
    :alt: Demo

You can use your own templates
by specifying them with the ``--template path:my/template`` syntax.
You can also create a Python package with a "shellman" entrypoint
pointing at ``shellman.Template`` instances (or dictionaries of such).
They will then be directly available to shellman, and selectable
with the ``--template template_name`` syntax.

See http://jinja.pocoo.org/docs/2.10/templates/ for more information
on how to write Jinja2 templates.

Documentation syntax
====================

- Documentation lines always begin with `##`.

    ## This is a doc line.
    # This is not a doc line.

- Documentation lines can't be placed at the end of instructions.

    ## This will be recognized.
        ## Even with spaces before.
    echo "This will NOT be recognized" ## Ignored

- Documentation **tags** are available to precise the type of documentation.
  Tags are always preceded with either ``@`` or ``\`` (at or backslash).
  Example:

    ## @brief This file is the README.
    ## \desc I personally prefer backslash,
    ## I find it more readable.

# CONTINUE HERE
- The previous example leads us to tags' **occurrences** and **number of possible lines**.
  Currently the script only handles **one** or **many** for both (and not
  specific numbers like 2, 17, or 94873407).

    ## \brief Accepted only once, next ones will be ignored.
    ## \brief The first one is kept. Only one line here.
    ## So this line is ignored because it has no tags.

    ## \desc Accepted only once.
    ## Can have many lines below.
    ## You want a empty line? Here:
    ##
    ## End.

    ## \usage Some tags can be used several times
    ## and also have many lines
    ## \usage like this one (usage).
    ## See below how such tags' content will be displayed.

- If a tag supports many lines, it will end at first non-documentation line or
  first documentation line with a tag.

    ## \desc Ook. Ook?

    ## This line will be ignored, because the blank line above "ended" the current tag.

    ## \usage An instruction between doc lines
    echo "Ook! Ook!"
    ## will also "end" the current tag documentation (this line is ignored).

- shellman also handles documentation for functions. Start documentation for
  a function with the `fn` tag.

    ## \fn some prototype or else
    ## \brief one-line description
    ## \param P some parameter
    some_function() { echo "Hello"; }

    ## \fn and again...

- Some tags have a special behaviour for display. If their content have multiple
  lines, then the first line is considered a header. If they have just one line,
  then the first word is considered the header. It helps to create a better
  display (with indentation).

    ## \option -o Optimize computation.
    ## \option -s, --slow
    ## Slower computation.

    Options:
      -o Optimize computation.
      -s, --slow
        Slower computation.




Author
------

.. code::

    ## \author
Bug
Brief
Caveat
Copyright
Date
Desc
Env
Error
Example
Exit
File
Function
History
License
Note
Option
Seealso
Stderr
Stdin
Stdout
Usage
Version


License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    [sudo -H] pip install shellman

Development
===========

To run all the tests: ``tox``

Usage
=====

