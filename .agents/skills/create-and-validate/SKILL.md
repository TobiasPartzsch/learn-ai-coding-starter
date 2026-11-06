---
name: create-and-validate
description: Add a runnable example and exact-output test for a SlopLang feature by loading create-test-program, then run the validate checks to confirm the project is still green
---

# Create and Validate

Add a test program for a language feature, then prove the project still passes.

## 1. Load the example workflow

Call the `skill` tool with `create-test-program` and follow its instructions for the requested feature.

- If the request does not name a feature, ask which one before starting.
- `create-test-program` has an `ask` permission. Wait for approval; do not bypass it or recreate its steps from memory.
- If `docs/spec.md` does not describe the feature, stop and report the gap instead of inventing semantics.

## 2. Format before checking

Once the example and test are written, run:

```bash
uv run ruff format
```

## 3. Validate

Call the `skill` tool with `validate` and follow it: run the tests, formatting check, linter, and type checker.

## 4. Report

State the example path, the exact expected output, and the result of each check. Report failures before proposing fixes.
