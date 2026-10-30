# Sources and Provenance

## Source inventory

| Source | Trust | Contribution | Constraints |
|---|---|---|---|
| [Upstream `skills/babysit-pr` at commit `1085050`](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/babysit-pr) | Primary, pinned upstream | Provenance for [`skills/babysit-pr/SKILL.md`](SKILL.md) and [`skills/babysit-pr/scripts/pr-wait`](scripts/pr-wait); the local skill adds auto-merge defaults | Upstream repository is MIT-licensed; see Rights and attribution |

## Provenance

- **Upstream repository:** [t3dotgg/tstack](https://github.com/t3dotgg/tstack)
- **Upstream path:** `skills/babysit-pr`
- **Pinned commit:** [`1085050f3baed1ac724caa4a8166145fb2ac88af`](https://github.com/t3dotgg/tstack/commit/1085050f3baed1ac724caa4a8166145fb2ac88af)
- **Requested source location:** [`skills/babysit-pr` at the pinned commit](https://github.com/t3dotgg/tstack/tree/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/babysit-pr)
- **Local paths:** `skills/babysit-pr/SKILL.md` and `skills/babysit-pr/scripts/pr-wait`
- **Content difference:** the local skill enables GitHub auto-merge by default
  without a base-branch prerequisite and permits an explicit user opt-out. If
  enabling auto-merge fails, it reports why and continues babysitting. Base-branch
  checks still apply to manual merges. The `pr-wait` script still matches its
  pinned upstream version.

## Rights and attribution

At the pinned commit, the upstream repository's [LICENSE](https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE) identifies the project as MIT-licensed and carries the notice: Copyright (c) 2026 Theo Browne.
