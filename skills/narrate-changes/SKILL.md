---
name: narrate-changes
description: Rechunk into a narrative-quality change history
---

Plan how to implement the changes in branch $ARGUMENTS as a new set of changes with a clean, narrative-quality change history suitable for reviewer comprehension.

Steps

1. Identify the scope

- If the user names a range, branch, commit, or files, use that scope.
- If no scope is given, inspect the current Git working tree, including staged, unstaged, and untracked files.
- If the intended base branch is ambiguous for a branch summary, infer from `origin/main` or `origin/master`; ask only when the base materially changes the answer.

2. Analyze the diff

- Study all changes in scope
- Form a clear understanding of the final intended state.

3. Plan the change storyline

- Break the implementation down into a sequence of self-contained steps.
- Each step should reflect a logical stage of development-as if writing a tutorial, and introduce a single coherent idea.

4. Reimplement the work

- Before making any changes, start a new branch.
- Create a new commit for each change.

5. Verify correctness
- Confirm that the final state of your changes exactly matches the final state of the original revision.
