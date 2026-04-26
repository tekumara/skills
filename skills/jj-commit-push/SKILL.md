---
name: jj-commit-push
description: Commits working-copy changes with Jujutsu and pushes the resulting bookmark in one shot. Use when the user asks to "jj commit and push", "commit and push with jj", or wants a single-step Jujutsu commit/bookmark-move/push workflow.
---

# JJ Commit and Push

Use the bundled script for the common Jujutsu flow:
1. commit the current working-copy changes
2. move the active bookmark to the new commit
3. push that bookmark to the remote

## Quick start

Run:

```bash
scripts/jj_commit_push.sh --message "<commit message>"
```

The script:
- requires a commit message
- defaults `--remote` to `origin`
- auto-detects the bookmark from `@-` when exactly one bookmark points there
- asks for `--bookmark` when none or multiple bookmarks are found

## Common cases

Commit and push using the bookmark on `@-`:

```bash
scripts/jj_commit_push.sh --message "update docs"
```

Commit and push a specific bookmark:

```bash
scripts/jj_commit_push.sh --message "update docs" --bookmark add-view-concept
```

Push to a different remote:

```bash
scripts/jj_commit_push.sh --message "update docs" --bookmark add-view-concept --remote upstream
```

## Notes

- Use this only when there are working-copy changes to commit.
- If the working-copy parent is not bookmarked, pass `--bookmark` explicitly.
- If multiple bookmarks point at `@-`, pass `--bookmark` explicitly.
- The script is intentionally conservative and fails instead of guessing the wrong bookmark.
