#!/bin/sh
set -e

command -v pipx &>/dev/null || python3 -m pip install --user pipx
command -v pdm &>/dev/null || pipx install pdm

pdm self list 2>/dev/null | grep -q pdm-multirun || pdm install --plugins

[ -n "${PDM_MULTIRUN_VERSIONS}" ] && pdm multirun -v pdm install -G:all && exit 0

pdm install -G:all
