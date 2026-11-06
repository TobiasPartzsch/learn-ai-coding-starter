---
name: create-test-program
description: Turn a SlopLang language feature into a runnable program in examples/ plus a regression test in tests/test_example_outputs.py that pins its exact output, using docs/spec.md as the contract
---

# Create Test Program

Given a SlopLang language feature, add one small example program and an exact-output test for it.

## 1. Read the contract

Read `docs/spec.md` and find the section that defines the feature: syntax, precedence, output formatting, and error behavior.

- Do not invent semantics. If the spec does not describe the feature, stop and report the gap instead of guessing.
- Note anything the example must avoid (unsupported operators, coercion rules, evaluation order).

## 2. Write the example

Create `examples/<feature>.slop`, named after the feature in lowercase, joining words with underscores (for example `examples/short_circuit.slop`).

Conventions, taken from the existing examples:

- Start with a `—` (em dash) comment naming the feature.
- Use smart quotes `“ ”` for strings; straight quotes are a lexical error.
- End every statement with `✨`.
- Print at least one line: `tests/test_examples.py` requires non-empty stdout.
- Keep it minimal and deterministic, demonstrating only the feature in question.

Run it before writing the test:

```bash
uv run sloperator.py examples/<feature>.slop
```

## 3. Pin the exact output

Add a case to `tests/test_example_outputs.py`. Create the file if it does not exist; otherwise leave the harness alone and add one entry.

The file maps an example's file stem to its complete expected stdout:

```python
from pathlib import Path

import pytest

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"

OUTPUTS = {
    "short_circuit": "left\nright\n",
}


@pytest.mark.parametrize(("name", "expected"), sorted(OUTPUTS.items()))
def test_example_output(name: str, expected: str):
    source = (EXAMPLES / f"{name}.slop").read_text(encoding="utf-8")
    result = run_source(source)

    assert (result.stdout, result.stderr, result.exit_code) == (expected, "", 0)
```

Rules:

- Assert the whole stdout string, including the trailing newline. Never use `in` or substring checks.
- Keep the expected value next to the example name so a reader can compare them.
- Use a triple-quoted string if the output spans lines and a plain quoted string otherwise.

## 4. Validate

```bash
uv run pytest tests/test_example_outputs.py -q
uv run pytest -q
uv run ruff format
uv run ruff format --check
uv run ruff check
uv run ty check
```

Report the example path, the exact expected output, and which checks passed. Report failures before proposing fixes.
