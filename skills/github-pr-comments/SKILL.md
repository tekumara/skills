---
name: github-pr-comments
description: Add, inspect, and verify GitHub PR comments, including inline comments in an existing pending (draft) review. Use when asked to comment on a GitHub pull request, add a GitHub review comment, or add a comment to a pending/draft GitHub review.
---

# GitHub PR comments

Use this skill for GitHub-hosted PR comments. It deliberately distinguishes GitHub review state from super.engineering's in-app review threads.

## Select the destination first

- **GitHub PR comment**, **GitHub review**, or **pending/draft GitHub review**: use `gh` and GitHub GraphQL.
- **In-app review**, **super.engineering review**, **worktree review**, or an explicit super.engineering `comment_id`: use `sc worktree review-*`.
- If the request could refer to either system, ask before writing a comment.
- Do not create a super.engineering review comment as a substitute for a requested GitHub review comment.

Read `better-github-skill` before GitHub operations. Keep work on the existing PR unless the user asks to create one.

## Safety rules

- A pending review is a draft. Do **not** submit it unless the user explicitly asks.
- Use the GitHub PR head and diff to establish an inline anchor. Do not anchor from an unpushed local change.
- Inspect the pending review's existing comments before adding one. Do not duplicate a comment already present.
- Do not post or submit a comment until its destination, PR, draft-review state, file, and changed-side line are verified.
- Use `--body-file` or a quoted heredoc for ordinary GitHub comment bodies. Never interpolate untrusted text into shell source.

## Adding an inline comment to an existing pending review

### 1. Identify the PR and its GitHub head

```sh
gh pr view --json number,url,headRefOid,headRefName
```

Use the reported PR number and head SHA. `gh api` only expands `{owner}` and `{repo}`; substitute the PR number yourself.

### 2. Find the current viewer's pending review

```sh
gh api graphql -f query='
query {
  viewer { login }
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      id
      reviews(first: 100) {
        nodes { id state author { login } }
      }
    }
  }
}'
```

Choose only the review where `state` is `PENDING` and `author.login` is the viewer. If there is no matching draft, stop and ask whether to create a draft review or post a submitted comment.

### 3. Verify the inline location against the PR diff

Fetch the PR's changed file from GitHub, not the local worktree. For example:

```sh
gh api 'repos/{owner}/{repo}/pulls/PR_NUMBER/files?per_page=100' --paginate \
  --jq '.[] | select(.filename == "PATH") | .patch' > "$TMPDIR/pr-file.patch"
```

Read the resulting patch and confirm that `LINE` is an added or context line on the requested `RIGHT` side. If it is not in the diff, ask for a PR-level comment or a different anchor.

### 4. Check the draft for a duplicate

Extend the GraphQL discovery query with the review's comments, or query the selected review directly. Compare the intended body, file, and line before writing.

### 5. Add the thread through GraphQL

GitHub's reliable route for appending an inline comment to an existing draft review is `addPullRequestReviewThread`:

```sh
gh api graphql \
  -f query='
mutation($review: ID!, $body: String!, $path: String!, $line: Int!, $side: DiffSide!) {
  addPullRequestReviewThread(input: {
    pullRequestReviewId: $review,
    body: $body,
    path: $path,
    line: $line,
    side: $side
  }) {
    thread {
      id
      comments(first: 1) {
        nodes {
          id
          body
          path
          line
          pullRequestReview { id state }
        }
      }
    }
  }
}' \
  -f review='PENDING_REVIEW_NODE_ID' \
  -f body='COMMENT_BODY' \
  -f path='PATH' \
  -F line=LINE \
  -f side=RIGHT
```

A successful response must show the expected path and line, and `pullRequestReview.state` must still be `PENDING`.

### 6. Report the result

State the PR URL, file and line, the created thread/comment ID, and that the review remains pending. Do not claim the comment is publicly submitted.

## Common traps

- `sc worktree review-add` writes a super.engineering comment, not a GitHub comment.
- `gh api '.../pulls/{pull_number}/reviews'` fails: replace `PR_NUMBER`; only `{owner}` and `{repo}` are placeholders.
- Do not rely on a REST `reviews/{review_id}/comments` route to append to an existing draft. Use the GraphQL mutation above.
- `PullRequestReviewComment` does not expose a `side` field in this GraphQL schema. Keep the mutation response selection to the fields shown above.
- `addPullRequestReviewComment` requires legacy diff `position`; prefer `addPullRequestReviewThread`, which accepts `line` and `side`.
- `docker compose up --wait` and similar suggestions should be reviewed against the PR's remote diff before adding the thread, even if a local edit already implements them.
