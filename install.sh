#!/usr/bin/env bash

# every instruction is idempotent so this script can be rerun multiple times

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

# install symlinks
stow -vv skills -t ~/.codex/skills
stow -vv skills -t ~/.pi/agent/skills
ln -sfn "$SCRIPT_DIR/prompts" ~/.pi/agent/prompts
