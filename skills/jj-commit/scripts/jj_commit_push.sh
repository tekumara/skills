#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  jj_commit_push.sh --message "<commit message>" [--bookmark <name>] [--remote <name>] [--dry-run]

Commits the current Jujutsu working-copy changes, moves a bookmark to the new commit,
and pushes that bookmark to the selected remote.

Options:
  -m, --message   Commit message (required)
  -b, --bookmark  Bookmark to move and push (optional if exactly one bookmark points at @-)
  -r, --remote    Remote to push to (default: origin)
      --dry-run   Print commands without executing them
  -h, --help      Show this help
EOF
}

message=""
bookmark=""
remote="origin"
dry_run=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -m|--message)
      [[ $# -ge 2 ]] || { echo "error: --message requires a value" >&2; exit 2; }
      message="$2"
      shift 2
      ;;
    -b|--bookmark)
      [[ $# -ge 2 ]] || { echo "error: --bookmark requires a value" >&2; exit 2; }
      bookmark="$2"
      shift 2
      ;;
    -r|--remote)
      [[ $# -ge 2 ]] || { echo "error: --remote requires a value" >&2; exit 2; }
      remote="$2"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$message" ]]; then
  echo "error: --message is required" >&2
  usage >&2
  exit 2
fi

command -v jj >/dev/null 2>&1 || {
  echo "error: jj is not installed or not on PATH" >&2
  exit 1
}

run() {
  echo "+ $*"
  if [[ "$dry_run" -eq 0 ]]; then
    "$@"
  fi
}

if [[ -z "$(jj diff --summary)" ]]; then
  echo "error: no working-copy changes to commit" >&2
  exit 1
fi

if [[ -z "$bookmark" ]]; then
  mapfile -t bookmarks < <(jj bookmark list -r @- -T 'name ++ "\n"' | sed '/^$/d')

  if [[ ${#bookmarks[@]} -eq 0 ]]; then
    echo "error: no bookmark found on @-. Pass --bookmark <name> explicitly." >&2
    exit 1
  elif [[ ${#bookmarks[@]} -gt 1 ]]; then
    echo "error: multiple bookmarks found on @-. Pass --bookmark explicitly." >&2
    printf 'bookmarks on @-:\n' >&2
    printf '  %s\n' "${bookmarks[@]}" >&2
    exit 1
  fi

  bookmark="${bookmarks[0]}"
fi

if [[ -z "$(jj bookmark list "$bookmark")" ]]; then
  echo "error: bookmark not found: $bookmark" >&2
  exit 1
fi

run jj commit -m "$message"
run jj bookmark move "$bookmark" --to @-
run jj git push --remote "$remote" --bookmark "$bookmark"
