<p align="center">
  <img src="logo.png">
</p>

<h1 align="center">Shell Script Documentation</h1>

<p align="center">Write documentation in comments and render it with templates.</p>

<!-- start-badges -->
<p align="center">
  <a href="https://travis-ci.org/pawamoy/shellman/">
    <img src="https://travis-ci.org/pawamoy/shellman.svg?branch=master">
  </a>
  <a href="https://www.codacy.com/app/Pawamoy/shellman/dashboard">
    <img src="https://api.codacy.com/project/badge/Grade/85e410da099c46d0bcf3700c563bbc2a">
  </a>
  <a href="https://www.codacy.com/app/pawamoy/shellman/dashboard">
    <img src="https://api.codacy.com/project/badge/Coverage/85e410da099c46d0bcf3700c563bbc2a">
  </a>
  <a href="https://pypi.python.org/pypi/shellman/">
    <img src="https://img.shields.io/pypi/v/shellman.svg?style=flat">
  </a>
  <a href="https://pypi.python.org/pypi/shellman/">
    <img src="https://img.shields.io/pypi/wheel/shellman.svg?style=flat">
  </a>
  <a href="https://gitter.im/pawamoy/shellman">
    <img src="https://badges.gitter.im/pawamoy/shellman.svg">
  </a>
</p>
<!-- end-badges -->

`shellman` can generate man pages, wiki pages and help text
using documentation written in shell scripts comments.

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

You can see more examples and all the documentation in the wiki!

- [GitLab wiki](https://gitlab.com/pawamoy/shellman/wikis)
- [GitHub wiki](https://github.com/pawamoy/shellman/wiki)

<h2 align="center">Demo</h2>
<p align="center"><img src="demo.svg"></p>

In the demo above we saw the three builtin templates:
helptext, manpage and wikipage.

You can use your own templates
by specifying them with the ``--template path:my/template`` syntax.

You can also write a plugin: see [the wiki page on GitLab] or [on GitHub].

[the wiki page on GitLab]: https://gitlab.com/pawamoy/shellman/wikis/plugins
[on GitHub]: https://github.com/pawamoy/shellman/wiki/plugins

## Installation
`shellman` is written in Python, so you must install it with `pip`:

    pip install shellman

## Some projects using shellman

- [shellm](https://github.com/shellm-org) —
  A collection of scripts and libraries
  built on its [core inclusion-system](https://github.com/shellm-org/core),
  all installable with [basher](https://github.com/basherpm/basher).

## License
Software licensed under [ISC] license.

[ISC]: https://www.isc.org/downloads/software-support-policy/isc-license/
