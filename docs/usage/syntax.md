# Documentation syntax

To write your documentation, you must follow a few simple rules.


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

That's it! You may want to take a look at the [available tags](tags.md) now.
