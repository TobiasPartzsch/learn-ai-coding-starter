---
description: Review the diff, stage and commit changes, then rebase onto origin/main
---

Review the current project changes, commit them, and rebase onto `origin/main`.

1. Inspect the working tree with `git status --short`, `git diff`, and `git diff --staged`. Read untracked files that would be committed. Stop and report instead of committing if you find secrets, credentials, debug leftovers, or generated artifacts that should not be tracked.
2. Stage the reviewed project changes with `git add -A`. Do not stage anything excluded by `.gitignore`.
3. Commit using this message exactly as provided:

$ARGUMENTS

   Pass the message verbatim as a single commit message; quote it safely if it contains shell metacharacters. If the message is empty, stop and ask for one instead of inventing a message.
4. After the commit succeeds, run `git pull --rebase origin main`.
5. If the rebase reports conflicts, stop immediately. Do not resolve or abort the rebase without asking; report the conflicting files and the current rebase state.

Report the commit hash, the files committed, and the result of the rebase.
