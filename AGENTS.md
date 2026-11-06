# Sloperator

## Layout

- `sloperator/lexer/`: tokenization
- `sloperator/parser/`: syntax trees and grammar
- `sloperator/evaluator/`: runtime behavior
- `tests/`: regression tests
- `examples/`: runnable programs

## Validation

- `uv run pytest`
- `uv run ruff format --check`
- `uv run ruff check`
- `uv run ty check`
- For comparison precedence changes, run `uv run pytest tests/test_comparisons.py -q`.

Add a regression test when fixing a bug or adding language behavior. Test observable results and errors rather than private implementation details.

See [docs/spec.md](docs/spec.md) for the language contract.