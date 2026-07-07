# JJ Workspace Management Specification

## Intent

This skill helps agents use Jujutsu workspaces safely for isolated work. It prevents accidental movement of the original workspace, especially when Git commands and JJ workspaces share one repository.

## Scope

In scope:
- creating and switching JJ workspaces
- isolating work from a dirty workspace
- checking out GitHub pull requests into new JJ workspaces with tracked bookmarks for pushing back
- rebasing completed work
- resolving workspace conflicts before cleanup
- forgetting and deleting temporary workspaces after validation

Out of scope:
- teaching JJ from first principles
- replacing project-specific release or test workflows
- managing non-JJ Git worktrees except as a fallback for PR inspection

## Users and trigger context

Primary users:
- coding agents working in repositories that use JJ

Common user requests:
- create a new JJ workspace
- check out a GitHub PR in a JJ workspace
- keep the original workspace unchanged
- rebase or clean up a temporary workspace

Should not trigger for:
- ordinary Git checkout requests in repositories that do not use JJ
- code review or testing tasks that do not mention workspace isolation or JJ operations

## Runtime contract

Required first actions:
- inspect `jj status`, `jj workspace list`, `jj bookmark list`, and the current `@` and `@-`
- record the current full commit id before risky workspace or Git operations

Required outputs:
- workspace path and current revision
- base revision or PR head used
- validation run
- cleanup status
- remaining conflicts or risks

Non-negotiable constraints:
- do not run `gh pr checkout` in the shared JJ checkout for isolated PR work
- run `jj bookmark track` when checking out a PR branch so `jj git push` can update the PR branch later
- do not remove a workspace that is still the easiest path to resolving conflicts
- do not silently guess what `main` means

Expected bundled files loaded at runtime:
- `scripts/jj-pr-workspace` when checking out a GitHub PR into a JJ workspace
- `jj bookmark track` through the installed JJ CLI for PR checkouts that need push-back support

## Source and evidence model

Authoritative sources:
- JJ command behavior from the installed `jj` CLI
- GitHub PR metadata from `gh pr view`
- repository-specific instructions such as `CLAUDE.md`

Useful improvement sources:
- failed workspace checkout transcripts
- cleanup mistakes and recovery transcripts
- validation results from script tests

Data that must not be stored:
- secrets
- private repository URLs beyond what is needed to reproduce a workspace command
- customer data

## Reference architecture

- `SKILL.md` contains runtime rules and common workflows.
- `scripts/` contains deterministic helpers for fragile workspace operations.
- `references/` is not used unless a future workflow needs optional depth.
- `assets/` is not used.

## Validation

Lightweight validation:
- run the skill validator on the skill directory
- run `python3 -m py_compile scripts/jj-pr-workspace`
- test the script against a disposable workspace and verify the original workspace is unchanged
- verify that the script runs `jj bookmark track`, creates a tracked PR bookmark, and prints a push hint

Deeper validation:
- test PR checkout from a fork
- test the failure path from a secondary JJ workspace without `.git`

Acceptance gates:
- the script is non-interactive
- the script prints structured JSON on success
- the script fetches and tracks the PR branch before creating the workspace
- the script uses a predictable remote name in the form `pr-<number>-<owner>`
- the original workspace commit is unchanged after a successful script run
- cleanup of test workspaces is verified with `jj workspace list`

## Known limitations

- `scripts/jj-pr-workspace` must be run from a colocated JJ workspace that has a Git checkout.
- The script fetches the PR head by repository and branch name, so it can fail if the PR branch was deleted.
- The script may fail in a blobless partial clone if JJ cannot check out missing Git objects into the new workspace.

## Maintenance notes

Update `SKILL.md` when a runtime rule changes. Update this `SPEC.md` when scope, safety rules, or validation gates change. Add evidence under `references/evidence/` only if repeated failures need preserved examples.
