---
name: jj-workspace-management
description: Manages Jujutsu workspaces for isolated task execution, rebases, conflict resolution, and cleanup. Use when the user asks to create or switch workspaces, isolate dirty working copies, rebase onto main or another revision, resolve jj workspace conflicts, or clean up temporary workspaces.
---

# JJ Workspace Management

Use this skill for tasks involving `jj workspace add`, `jj new`, `jj rebase`, `jj workspace forget`, and temporary-workspace cleanup.

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

### 5) Fresh workspaces may need bootstrap
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
