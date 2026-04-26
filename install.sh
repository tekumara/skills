#!/usr/bin/env bash

# every instruction is idempotent so this script can be rerun multiple times

set -euo pipefail

# install symlinks
stow -vv skills -t ~/.codex/skills
stow -vv skills -t ~/.pi/agent/skills
