<p align="center">
  <img src="https://rawgit.com/pawamoy/shellman/master/logo.png">
</p>

<h1 align="center">Shell Script Documentation</h1>

<p align="center">Write documentation in comments and render it with templates.</p>

<p align="center">
  <a href="https://github.com/pawamoy/shellman/actions?query=workflow%3Aci">
    <img alt="ci" src="https://github.com/pawamoy/shellman/workflows/ci/badge.svg" />
  </a>
  <a href="https://pawamoy.github.io/shellman/">
    <img alt="documentation" src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" />
  </a>
  <a href="https://pypi.org/project/shellman/">
    <img alt="pypi" src="https://img.shields.io/pypi/v/shellman.svg" />
  </a>
  <a href="https://gitpod.io/#https://github.com/pawamoy/shellman">
    <img alt="gitpod" src="https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat" />
  </a>
  <a href="https://gitter.im/shellman/community">
    <img alt="gitter" src="https://badges.gitter.im/join%20chat.svg" />
  </a>
</p>

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
<p align="center"><img src="https://rawgit.com/pawamoy/shellman/master/demo.svg"></p>

In the demo above we saw the three builtin templates:
helptext, manpage and wikipage.

You can use your own templates
by specifying them with the ``--template path:my/template`` syntax.

You can also write a plugin: see [the wiki page on GitLab] or [on GitHub].

[the wiki page on GitLab]: https://gitlab.com/pawamoy/shellman/wikis/plugins
[on GitHub]: https://github.com/pawamoy/shellman/wiki/plugins

## Installation

With `pip`:
```bash
pip install shellman
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.8 -m pip install --user pipx
pipx install shellman
```

## Some projects using shellman

- [shellm](https://github.com/shellm-org) —
  A collection of scripts and libraries
  built on a [core inclusion-system](https://github.com/shellm-org/core),
  all installable with [basher](https://github.com/basherpm/basher).
  Here are a few examples:
  - [daemon](https://github.com/shellm-org/daemon) —
    A library that facilitates the writing of daemonized scripts that consume
    files in a watched directory.
  - [debug](https://github.com/shellm-org/debug) —
    A simple script that sets the verbose/dry-run/debug
    Bash flags before running another script.
  - [format](https://github.com/shellm-org/format) —
    Format your output with style and color.
  - [home](https://github.com/shellm-org/home) —
    A home for your shell scripts! 
  - [loop](https://github.com/shellm-org/loop) —
    Control the flow of your loops (pause/resume/etc.).
