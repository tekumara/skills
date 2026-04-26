---
description: Rechunk into a narrative-quality change history
argument-hint: "[branch]"
---
Plan how to implement the changes in branch $ARGUMENTS as a new set of changes with a clean, narrative-quality change history suitable for reviewer comprehension.

### Steps

**Analyze the diff**

- Study all changes in the revision using `jj diff --git -r main..$ARGUMENTS`
- Form a clear understanding of the final intended state.

**Plan the change storyline**

- Break the implementation down into a sequence of self-contained steps.
- Each step should reflect a logical stage of development-as if writing a
  tutorial, and introduce a single coherent idea.

**Reimplement the work**

- Before making each change, start a new branch with `jj new main`. 
- Run `jj new -m TITLE` to create a new revision for each change. Replace TITLE with the change description

6. **Verify correctness**

- Confirm that the final state of your changes exactly matches the
  final state of the original revision.
