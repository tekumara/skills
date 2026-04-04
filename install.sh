#!/usr/bin/env bash

# every instruction is idempotent so this script can be rerun multiple times

set -euo pipefail

# install symlinks
stow -vv --ignore="install.sh|README.md" . -t ~/.codex/skills
