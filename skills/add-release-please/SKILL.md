---
name: add-release-please
description: Add release-please automation to a repository that uses GitHub Actions for releases or package publishing. Use when Codex needs to inspect an existing repo, install a release-please workflow, add the required manifest/config files, preserve any existing publish workflow, add a Release flow section to CONTRIBUTING.md explaining how releases work, and then tell the user which GitHub secrets and settings to add manually after the code changes are complete.
---

# Add Release Please

Inspect the repository before changing anything. Reuse existing release or publish workflows where possible instead of replacing them.

## Workflow

1. Inspect the current release flow.
   - Read `.github/workflows/*`.
   - Read the dominant package metadata such as `package.json`, `pyproject.toml`, `Cargo.toml`, or equivalent.
   - Check whether tags, GitHub Releases, or package publishing already exist.
   - Check both local tags and remote tags on `origin` before deciding the repository is untagged.
   - Check `git status --short` and avoid overwriting unrelated local edits.

2. Choose the release-please shape.
   - Add `.github/workflows/release-please.yml` using the example shape below as-is unless the repository has a specific branch-name requirement.
   - Trigger it on pushes to the main release branch and `workflow_dispatch`.
   - Prefer a GitHub App token via `actions/create-github-app-token@v2` so release PRs and GitHub Releases can trigger downstream workflows.
   - Grant workflow permissions for `contents`, `pull-requests`, and `issues` write unless the repo has a narrower proven configuration.

3. Add repository config.
   - Create a manifest file at `.release-please-manifest.json`.
   - Create `release-please-config.json` using the example shape below as-is, except update `packages["."].release-type` to match the repository ecosystem.
   - Set the package path to `"."` for single-package repositories.
   - Use the release type that matches the repository ecosystem. If the correct release type is unclear, verify it against the official `release-please` docs before editing.
   - Seed the manifest version from the current package version when present; otherwise use the repo's current unreleased baseline.

4. Bootstrap the initial release tag when needed.
   - If there are no existing local tags and no remote tags on `origin`, create an annotated `v0.0.0` tag on the repository's first commit.
   - Push that bootstrap tag to `origin` so `release-please` has a baseline release point.
   - Do not add the bootstrap tag if the repository already has any tag history, existing GitHub Releases, or an established non-`v` tagging convention that should be preserved.

5. Integrate with the existing publish flow.
   - Keep publish workflows that already run on `release.published`.
   - If publishing currently depends on tags or manual version bumps, adapt it to consume GitHub Releases created by `release-please`.
   - Do not duplicate version ownership. After installation, `release-please` should own changelog and version bumps.

6. Update contributor documentation.
   - Add a `Release flow` section to `CONTRIBUTING.md`.
   - If `CONTRIBUTING.md` does not exist, create it.
   - Explain the operational flow only: conventional commits, the release PR, the merge creating the tag and GitHub Release, and any downstream publish workflow.
   - Use this default section text unless the repository needs a small wording adjustment:

```md
### Release flow

- Push conventional commits to `main` such as `feat: ...` and `fix: ...`.
- `.github/workflows/release-please.yml` opens or updates the release PR.
- Merging that PR creates the tag and GitHub Release.
- The existing publish workflow then publishes the package to npm from the `release.published` event.
```

   - Do not add secret values or GitHub App setup steps to `CONTRIBUTING.md` unless the user explicitly asks for that documentation.

7. Hand off the remaining manual setup.
   - In the final response, tell the user which repository secrets to add: `APP_ID` and `APP_PRIVATE_KEY`.
   - Tell the user which GitHub App permissions or repo settings still need manual configuration when relevant: install the app on the repo, grant `Contents`, `Pull requests`, and `Issues` write access, and enable GitHub Actions pull request creation if the repo blocks workflow-created PRs.

8. Validate.
   - Validate YAML and JSON syntax locally.
   - Validate any Markdown edits for clarity and placement.
   - Summarize any remaining manual setup, especially secrets and repo settings, in the final handoff.

## Default Files To Add

- `.github/workflows/release-please.yml`
- `.release-please-manifest.json`
- `release-please-config.json`
- `CONTRIBUTING.md`

## Example File Shapes

Use these as default shapes. Keep `.github/workflows/release-please.yml` and `release-please-config.json` as written, except for the `release-type` value in `release-please-config.json`.

### `.github/workflows/release-please.yml`

```yaml
name: release-please

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - name: Generate app token for release-please
        id: app-token
        uses: actions/create-github-app-token@v3
        with:
          # https://github.com/apps/potatobot-prime
          client-id: ${{ secrets.APP_ID }}
          private-key: ${{ secrets.APP_PRIVATE_KEY }}
      - uses: googleapis/release-please-action@v4
        with:
          # use app token so that PRs and releases created by release-please trigger
          # additional workflows. They'll also be authored by the app.
          # see https://github.com/googleapis/release-please-action#github-credentials
          token: ${{ steps.app-token.outputs.token }}
```

### `release-please-config.json`

```json
{
  "prerelease": true,
  "bump-minor-pre-major": true,
  "bump-patch-for-minor-pre-major": true,
  "include-component-in-tag": false,
  "changelog-sections": [
    { "type": "feat", "section": "Features" },
    { "type": "fix", "section": "Bug Fixes" },
    { "type": "chore", "section": "Chores" },
    { "type": "refactor", "section": "Code Refactoring", "hidden": true },
    { "type": "style", "section": "Styles"},
    { "type": "test", "section": "Tests"},
    { "type": "ci", "section": "Builds" },
    { "type": "perf", "section": "Performance Improvements" }
  ],
  "packages": {
    ".": {
      "release-type": "rust"
    }
  },
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/schemas/config.json"
}
```

Change only `"release-type"` as appropriate for the target repository.

### `.release-please-manifest.json`

```json
{
  ".": "0.0.0"
}
```
