========
Shellman
========

.. start-badges


|travis|
|codacy|
|version|
|wheel|
|pyup|
|gitter|


.. |travis| image:: https://travis-ci.org/Pawamoy/shellman.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Pawamoy/shellman/

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/REPLACE_WITH_PROJECT_ID
    :target: https://www.codacy.com/app/Pawamoy/shellman/
    :alt: Codacy Code Quality Status

.. |pyup| image:: https://pyup.io/account/repos/github/pawamoy/shellman/shield.svg
    :target: https://pyup.io/account/repos/github/pawamoy/shellman/
    :alt: Updates

.. |gitter| image:: https://badges.gitter.im/Pawamoy/shellman.svg
    :alt: Join the chat at https://gitter.im/Pawamoy/shellman
    :target: https://gitter.im/Pawamoy/shellman?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |version| image:: https://img.shields.io/pypi/v/shellman.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/shellman/

.. |wheel| image:: https://img.shields.io/pypi/wheel/shellman.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/shellman/


.. end-badges

Write doc in your shell scripts.

Shellman is a Python package that read files, search for special comment lines
(documentation) and output formatted documentation as text, markdown or man page.

License
=======

Software licensed under `ISC`_ license.

.. _ISC: https://www.isc.org/downloads/software-support-policy/isc-license/

Installation
============

::

    [sudo -H] pip install shellman

Documentation
=============

http://shellman.readthedocs.io/en/latest/


Development
===========

To run all the tests: ``tox``

Usage
=====

To render the doc on standard output:

.. code:: bash

    shellman FILE
    # equivalent to...
    shellman --format=text FILE
    # other available formats:
    shellman --format=man FILE
    shellman --format=markdown FILE

You can pass the ``-o``, ``--output`` option to specify a file to write to,
instead of standard output.

To check if the documentation within a script is correct:

.. code:: bash

    shellman --check --warn FILE         # CI test
    shellman --check --failfast FILE     # quick CI test with no output
    shellman --check --warn --nice FILE  # always passing test with output

In a script, for automatic help text:

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
      -h, --help
        Print this help and exit.
