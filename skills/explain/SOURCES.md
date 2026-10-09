# Sources And Provenance

## Source inventory

| Source | Trust | Contribution | Constraints |
|---|---|---|---|
| [`skills/explain/SKILL.md` at `b771ea1`](https://github.com/hugobowne/show-us-your-agent-skills/blob/b771ea1b33d75fa19f4b02dbe10b0f1bf2fb49ef/skills/explain/SKILL.md) | Primary, author-supplied | Entire `SKILL.md`, copied verbatim except one frontmatter field | MIT; keep the copyright notice and license link below |

## Provenance

- **Upstream repository:** [hugobowne/show-us-your-agent-skills](https://github.com/hugobowne/show-us-your-agent-skills)
- **Upstream path:** `skills/explain/SKILL.md`
- **Pinned commit:** [`b771ea1`](https://github.com/hugobowne/show-us-your-agent-skills/commit/b771ea1b33d75fa19f4b02dbe10b0f1bf2fb49ef), merged as [PR #6](https://github.com/hugobowne/show-us-your-agent-skills/pull/6) on 2026-05-26. It is the latest commit that touches the file.
- **Original author:** Jeremiah Lowin, credited as the commit author and in the upstream skill README.
- **Blob SHA:** `bc87bf7bf73484c60655008669bd0f50f00611de`
- **Retrieved:** 2026-10-09
- **Local changes:** adds `disable-model-invocation: true` to the frontmatter, so the skill runs only when invoked explicitly as `/skill:explain`.

To verify the copy, run `sed '/^disable-model-invocation: true$/d' skills/explain/SKILL.md | git hash-object --stdin`. It should print the blob SHA above.

## Version choice

Upstream has two earlier versions of this file, at `ee53434` and `db577c2`. The upstream skill README says `b771ea1` replaces an earlier OCR transcription of the live recording and makes it the authoritative version. This copy uses `b771ea1`.

## Rights and attribution

The upstream repository is MIT licensed, Copyright (c) 2026 Hugo Bowne-Anderson. The full license text is in the [LICENSE file at `b771ea1`](https://github.com/hugobowne/show-us-your-agent-skills/blob/b771ea1b33d75fa19f4b02dbe10b0f1bf2fb49ef/LICENSE).
