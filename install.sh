#!/usr/bin/env bash

# every instruction is idempotent so this script can be rerun multiple times

set -euo pipefail

# install symlinks
mkdir -p ~/.agents/skills ~/.pi/agent/prompts
stow -vv skills -t ~/.agents/skills
stow -vv prompts -t ~/.pi/agent/prompts
