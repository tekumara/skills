---
name: jj-commit
description: Commit Jujutsu working-copy changes, push an existing Jujutsu bookmark, or commit and push when explicitly requested. Use when the user asks to "jj commit", "commit with jj", "jj push", "push with jj", "jj commit and push", or wants a fast Jujutsu commit/push workflow.
---

# JJ Commit

Use this skill for commit-only, push-only, and commit+push flows.

## Decision rule

- If the user asks to **commit**, do a commit only.
- If the user asks to **push** or says **jj push**, push an existing committed change/bookmark only; do not create a commit unless they also ask to commit.
- If the user explicitly asks to **commit and push**, use the commit+push flow.
- Never infer push from words like "commit", "jj commit", or "save this".
- Never infer commit from words like "push" or "jj push"; if there are uncommitted working-copy changes, stop and ask whether to commit them first.

## Fast path

Use this short flow unless something looks unusual:

1. Run `jj status`.
2. For commit flows, run `jj diff --stat` to size the working-copy change.
3. For push flows, inspect bookmarks on the commit to push with `jj bookmark list -r @- -T 'name ++ "\n"'` when the working copy is empty.
4. Open full `jj diff` only when the scope is unclear, the diff is surprisingly large, or you need help writing the message.
5. Skip `jj help commit` / `jj help git push` unless you need uncommon flags or a command fails.
6. Before committing, run the rationale gate in Message tips; fast path reduces inspection, not commit-message quality.

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

## Push only (`jj push` requests)

Use this when the user asks to push an already-created jj change.

1. Confirm there are no uncommitted working-copy changes:

```bash
jj status
```

If `jj status` reports working-copy changes, do not push them implicitly. Ask whether to commit first.

2. Identify the commit to push and its bookmark. In the common post-`jj commit` state, `@` is an empty working-copy commit and `@-` is the commit to push:

```bash
jj log -r '(@|@-)' --no-graph --template 'change_id.short() ++ " " ++ commit_id.short() ++ " " ++ description.first_line() ++ " bookmarks=" ++ bookmarks ++ "\n"'
jj bookmark list -r @- -T 'name ++ "\n"'
```

3. If exactly one local bookmark is already on `@-`, push it:

```bash
jj git push --bookmark <bookmark> --remote origin
```

4. If `@-` has no bookmark but the branch bookmark is clearly on the parent/base commit (common immediately after `jj commit`), move the intended bookmark to `@-`, then push:

```bash
jj bookmark set <bookmark> -r @-
jj git push --bookmark <bookmark> --remote origin
```

Use `jj bookmark list` and the recent `jj log` output to choose the bookmark. If none or multiple bookmarks are plausible, ask the user instead of guessing.

5. If push fails with a non-tracking remote bookmark error, track the remote bookmark and retry:

```bash
jj bookmark track <bookmark> --remote=origin
jj git push --bookmark <bookmark> --remote origin
```

6. Optional verification when useful:

```bash
git ls-remote origin "refs/heads/<bookmark>"
```

## Commit and push

Do not assume a repo-local helper exists. Use the portable native flow by default:

1. Commit the working-copy change:

```bash
jj commit -m "<commit message>"
```

2. Identify the bookmark to push. In the common post-commit state, `@` is an empty working-copy commit and `@-` is the commit to push:

```bash
jj log -r '(@|@-)' --no-graph --template 'change_id.short() ++ " " ++ commit_id.short() ++ " " ++ description.first_line() ++ " bookmarks=" ++ bookmarks ++ "\n"'
jj bookmark list -r @- -T 'name ++ "\n"'
```

3. Push using the push-only flow above. If no bookmark is already on `@-`, move or create a bookmark only when the intended branch is clear; otherwise ask the user instead of guessing.

Optional repo helper:

- Only use `scripts/jj_commit_push.sh` after verifying it exists and is executable.
- If the check fails, do not call the script; continue with the native flow.

```bash
test -x scripts/jj_commit_push.sh && scripts/jj_commit_push.sh --message "<commit message>"
```

Use push-only commands instead of any commit+push helper for a plain `jj push` request; helpers that commit require an explicit commit request and message.

## Message tips

- Reuse the repo's existing commit style when obvious.
- Prefer a concrete message over a generic one.
- If the recent work makes the message obvious, choose it and proceed.
- Ask the user only when the intent is genuinely ambiguous.

### Rationale gate

Before every commit, decide whether a future reader can infer **why** from the subject and diff alone.

Add a commit body when any condition is true:

- The change fixes misleading behavior, flaky tests, timeouts, performance, reliability, data loss, or evaluation/metric artifacts.
- The diff is mechanically small but the cause/effect chain is non-obvious.
- The change chooses a tradeoff, workaround, limit, timeout, concurrency setting, dependency override, migration path, or compatibility constraint.
- The user supplied rationale or asked “why” during the task.

Subject-only commits are acceptable only for self-explanatory changes such as typo fixes, pure renames, generated lockfile updates, or trivial config bumps.

### Body Guidelines

- Include motivation and rationale for the change.
- State previous behavior and new behavior when relevant.
- Explain the causal chain for non-obvious fixes, not just the files changed.
- Use imperative mood and present tense.

## Notes

- For commit-only and commit+push flows, require working-copy changes to commit.
- For push-only flows, require a committed change and a clear bookmark to push.
- For commit+push, after committing, require a clear bookmark before pushing.
- If no bookmark points at `@-`, move or create one only when the intended branch is clear; otherwise ask.
- Never call repo-local helper scripts unless their existence/executability was checked first.
