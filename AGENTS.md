# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang (`.slop`). It targets
Python 3.13, is managed with `uv`, and has no runtime dependencies.

## Project layout

- `sloperator.py` — CLI entrypoint; `--check` parses without evaluating.
- `sloperator/runner.py` — `check_program`, `run_program`, and `run_source`
  (the in-memory result helper used by tests).
- `sloperator/lexer/`, `sloperator/parser/`, `sloperator/evaluator/` — tokenizer,
  AST parser, and tree-walking interpreter.
- `tests/` — pytest suite, including parser/AST and end-to-end tests.
- `examples/` — `.slop` programs; `tests/test_examples.py` requires each to exit 0,
  write nothing to stderr, and produce non-empty stdout.
- `playground/server.py` — optional HTTP playground that shells out to the CLI.

## Validation

Run all four from the repo root:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

## When to add regression tests

Add a regression test whenever you fix a bug or change observable language
behavior. Put it in `tests/` at the relevant layer, and for parser/evaluator
changes typically add both an AST-shape test (`parse(tokenize(...))`) and a
runtime test (`run_source(...)`). A bug fix should include a test that fails
before the fix.

## Language behavior

See [`docs/spec.md`](docs/spec.md) for SlopLang syntax, values, scoping,
operators, and errors.
