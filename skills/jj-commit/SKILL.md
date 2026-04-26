---
name: jj-commit
description: Commit Jujutsu working-copy changes, or commit and push when the user explicitly asks to push. Use when the user asks to "jj commit", "commit with jj", "jj commit and push", or wants a fast Jujutsu commit workflow.
---

# JJ Commit

Use this skill for both commit-only and commit+push flows.

## Decision rule

- If the user asks to **commit**, do a commit only.
- If the user explicitly asks to **push**, use the commit+push flow.
- Never infer push from words like "commit", "jj commit", or "save this".

## Fast path

Use this short flow unless something looks unusual:
1. Run `jj status` to confirm there are working-copy changes.
2. Run `jj diff --stat` to size the change.
3. If the requested action is just a commit, commit immediately with a specific message.
4. Open full `jj diff` only when the scope is unclear, the diff is surprisingly large, or you need help writing the message.
5. Skip `jj help commit` unless you need uncommon flags or the command fails.

This avoids spending time on a full patch review for small, already-understood changes.

## Commit only

Run native Jujutsu directly:

```bash
jj commit -m "<commit message>"
```

Example:

```bash
jj commit -m "feat: add --tsv output for transactions list"
```

Prefer the native command for commit-only work. It is simpler and avoids unnecessary wrapper logic.

## Commit and push

Run:

```bash
scripts/jj_commit_push.sh --message "<commit message>"
```

The script:
- requires a commit message
- defaults `--remote` to `origin`
- auto-detects the bookmark from `@-` when exactly one bookmark points there
- asks for `--bookmark` when none or multiple bookmarks are found

Common cases:

```bash
scripts/jj_commit_push.sh --message "update docs"
scripts/jj_commit_push.sh --message "update docs" --bookmark add-view-concept
scripts/jj_commit_push.sh --message "update docs" --bookmark add-view-concept --remote upstream
```

## Message tips

- Reuse the repo's existing commit style when obvious.
- Prefer a concrete message over a generic one.
- If the recent work makes the message obvious, choose it and proceed.
- Ask the user only when the intent is genuinely ambiguous.

## Notes

- Use this skill only when there are working-copy changes to commit.
- For commit+push, if the working-copy parent is not bookmarked, pass `--bookmark` explicitly.
- For commit+push, if multiple bookmarks point at `@-`, pass `--bookmark` explicitly.
- The push script is intentionally conservative and fails instead of guessing the wrong bookmark.
