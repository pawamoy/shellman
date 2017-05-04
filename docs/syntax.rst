Syntax
======

Rules
-----

- Documentation lines always begin with ``##``.

  .. code:: bash

      ## This is a doc line.
      # This is not a doc line.

- Documentation lines can't be placed at the end of instructions.

  .. code:: bash

      ## This will be recognized.
          ## Even with spaces before.
      echo "This will NOT be recognized" ## Ignored

  If we also wanted to get documentation comments at the end of instructions,
  it would require to write a **real** parser. Indeed, think about a few cases:

  .. code:: bash

      echo "## doc line or not?"
      echo ${docline##ornot?}

- Documentation **tags** are available to precise the type of documentation.
  Tags are always preceded with either ``@`` or ``\`` (at or backslash).
  Example:

  .. code:: bash

      ## @brief This file is the README.
      ## \desc I personally prefer backslash,
      ## I find it more readable.
      ## \brief Ignored: brief already written.

- The previous example leads us to tags' **occurrences** and **number of possible lines**.
  Currently the script only handles **one** or **many** for both (and not
  specific numbers like 2, 17, or 94873407).

  .. code:: bash

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

  .. code:: bash

      ## \desc Ook. Ook?

      ## This line will be ignored, because the blank line above "ended" the current tag.

      ## \usage An instruction between doc lines
      echo "Ook! Ook!"
      ## will also "end" the current tag documentation (this line is ignored).

- shellman also handles documentation for functions. Start documentation for
  a function with the ``fn`` tag.

  .. code:: bash

      ## \fn some prototype or else
      ## \brief one-line description
      ## \param P some parameter
      some_function() { echo "Hello"; }

      ## \fn and again...

- Some tags have a special behavior for display. If their content have multiple
  lines, then the first line is considered a header. If they have just one line,
  then the first word is considered the header. It helps to create a better
  display (with indentation).

  .. code:: bash

      ## \option -o Optimize computation.
      ## \option -s, --slow
      ## Slower computation.


      Options:
        -o Optimize computation.
        -s, --slow
          Slower computation.


Script tags
-----------

============== ===================== =========== ======================= ===============================================
Tag            Multiple occurrences? Many lines? First word/line header? Description
============== ===================== =========== ======================= ===============================================
``author``     ✓                                                         The author of the script.
``bug``        ✓                     ✓                                   A bug in the script.
``brief``                                                                The one-line description for the script.
``caveat``     ✓                     ✓                                   A caveat.
``copyright``                        ✓                                   The copyright.
``date``                                                                 The date of the first release of the script.
``desc``                             ✓                                   The multi-line description of the script.
``env``        ✓                     ✓           ✓                       An environment variable used by the script.
``error``      ✓                     ✓           ✓                       An explained error, like in Diagnostics section.
``example``    ✓                     ✓           ✓                       An example of usage.
``exit``       ✓                     ✓           ✓                       Information about the exit status code.
``file``       ✓                     ✓           ✓                       A file used by the script.
``history``                          ✓                                   Kind of a changelog.
``license``                          ✓                                   The license under which the script is released.
``note``       ✓                     ✓                                   A note to the documentation readers.
``option``     ✓                     ✓           ✓                       A script option.
``seealso``    ✓                                                         A reference to another function or script.
``stderr``     ✓                     ✓                                   Something written on standard error.
``stdin``      ✓                     ✓                                   Something taken from standard input.
``stdout``     ✓                     ✓                                   Something written on standard output.
``usage``      ✓                     ✓                                   The synopsis or usage of the script.
``version``                                                              The version of the script.
============== ===================== =========== ======================= ===============================================

Function tags
-------------

=========== ===================== =========== ======================= ===========================================
Tag         Multiple occurrences? Many lines? First word/line header? Description
=========== ===================== =========== ======================= ===========================================
``fn``                                                                A function prototype.
``brief``                                                             The one-line description for the function.
``desc``                          ✓                                   The multi-line description of the function.
``param``   ✓                     ✓           ✓                       A function parameter.
``pre``     ✓                     ✓                                   A function precondition.
``return``  ✓                     ✓           ✓                       A function return code and explanation.
``seealso`` ✓                                                         A reference to another function or script.
``stderr``  ✓                     ✓                                   Something written on standard error.
``stdin``   ✓                     ✓                                   Something taken from standard input.
``stdout``  ✓                     ✓                                   Something written on standard output.
=========== ===================== =========== ======================= ===========================================
