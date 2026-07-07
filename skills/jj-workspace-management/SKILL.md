---
name: jj-workspace-management
description: Manages Jujutsu workspaces for isolated task execution, GitHub PR checkout, rebases, conflict resolution, and cleanup. Use when the user asks to create or switch workspaces, check out a GitHub pull request in a JJ workspace, isolate dirty working copies, rebase onto main or another revision, resolve jj workspace conflicts, or clean up temporary workspaces.
---

# JJ Workspace Management

Use this skill for tasks involving `jj workspace add`, `jj new`, `jj rebase`, `jj workspace forget`, GitHub PR workspace checkout, and temporary-workspace cleanup.

## Quick checklist

Before acting, inspect:

```bash
jj status
jj workspace list
jj bookmark list
jj log -r 'main|@|@-' --no-graph
```

Report:
- current workspace
- whether the working copy is dirty
- current `@` and `@-`
- target revision/bookmark for the requested action

## Rules that prevent wrong turns

### 1) Do not guess what “main” means
If the user says “onto main”, verify whether they mean:
- the `main` bookmark
- the current active development head
- another repo-specific trunk ref

If those differ, do not substitute one for another silently. State what `main` resolves to before rebasing, or ask.

### 2) Prefer a sibling workspace when the current one is dirty
If the current workspace has unrelated changes and the user wants an isolated task, create a sibling workspace from a clean revision instead of reusing the dirty workspace.

Typical pattern:

```bash
jj workspace add ../<repo>-<task> -r @-
```

### 3) Rebase lifecycle is strict
Use this sequence:
1. inspect state
2. create/switch workspace if needed
3. make changes
4. commit
5. rebase if requested
6. resolve conflicts if any
7. validate
8. only then forget/remove the temporary workspace

### 4) Conflicts stop cleanup
If `jj rebase` produces conflicts:
- stop cleanup immediately
- keep the workspace alive
- resolve conflicts in that workspace
- validate the result
- squash the resolution into the conflicted change if appropriate
- only then remove the workspace

Never forget/remove a workspace that still contains the easiest path to conflict resolution.

### 5) Do not use `gh pr checkout` in the shared JJ checkout
In a colocated JJ repository, `jj workspace add` creates a JJ workspace, not a separate Git worktree. A new JJ workspace may not have a `.git` directory. Running `gh pr checkout` in the shared Git checkout can move Git `HEAD`, and then `jj status` can import that movement into the current JJ workspace.

When the user asks to check out a GitHub PR in a new JJ workspace, use `scripts/jj-pr-workspace` from this skill when possible.

```bash
scripts/jj-pr-workspace <pr-url-or-number> <new-workspace-path>
```

Run the script from the main colocated JJ workspace that has `.git`, not from a secondary JJ workspace without `.git`.

Script contract:
- Arguments: a GitHub PR URL or number, and a workspace path that must not already exist.
- Output: JSON with the PR head, predictable remote name `pr-<number>-<owner>`, tracked bookmark, new workspace path, new workspace head and parent, push hint, and original workspace verification.
- Behavior: fetches the PR branch with `jj git fetch`, runs `jj bookmark track`, creates a JJ workspace at the fetched remote PR bookmark, and verifies the original workspace did not move.
- Push after edits: move the tracked bookmark to the finished change, then push it. The script prints the exact `jj bookmark set ...` and `jj git push ...` commands in `push_hint`.
- Fallback: if the script is unavailable or fails before creating a workspace, fetch the PR branch without checking it out, run `jj bookmark track --remote <remote> <branch>`, then run `jj workspace add <path> -r <branch>@<remote>`. If it fails after creating a workspace, inspect `jj workspace list` and either continue from the created workspace or forget and delete it.

### 6) Fresh workspaces may need bootstrap
A new workspace directory may not have repo-local install artifacts. Before running tests, check whether bootstrap is needed.

Examples:
- Node: `test -d node_modules || npm ci`
- pnpm: `pnpm install --frozen-lockfile`
- Python/uv: `uv sync`

Use the repo’s normal bootstrap command.

## Common workflows

### Isolate work from a dirty workspace
1. inspect current state
2. create sibling workspace from a clean parent
3. do the task there
4. validate
5. remove temp workspace only after success

### Check out a GitHub PR into a new JJ workspace
1. inspect current state and record the current `@` full commit id
2. run `scripts/jj-pr-workspace <pr-url-or-number> <new-workspace-path>` from the main colocated JJ workspace
3. read the JSON output and verify `original_workspace_unchanged` is `true`
4. keep the `push_hint` for when the user asks to push back to the PR branch
5. `cd` into the new workspace
6. bootstrap if needed, then test or edit there

### Rebase a completed task onto main
1. resolve what `main` means
2. rebase onto the confirmed destination
3. if conflicts appear, resolve before cleanup
4. confirm final commit id and destination

### Recover after premature workspace removal
If a temp workspace was removed too early, recover from the surviving commit/change by creating another workspace on it:

```bash
jj workspace add ../<repo>-recover -r <commit-or-change>
```

Then resolve, validate, and clean up properly.

## Final report

After finishing, report:
- final commit id
- what it was based/rebased onto
- whether conflicts remain
- whether any temporary workspace was removed
