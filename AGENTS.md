# AGENTS.md

Sloperator is a tree-walking interpreter for SlopLang (`.slop`). Python 3.13,
managed with `uv`, no runtime dependencies. `docs/spec.md` describes the
language; when it disagrees with the code, see "Known divergences" below.

## Commands (run from repo root)

```bash
uv run pytest                               # all tests
uv run pytest tests/test_nested_calls.py -q # one file
uv run pytest tests/test_nested_calls.py::test_call_as_argument_to_another_call -q
uv run ruff format --check                  # formatting (line length 100)
uv run ruff check                           # lint (E, F, I, UP, B)
uv run ty check                             # typecheck
uv run sloperator.py examples/hello.slop    # run a program
uv run sloperator.py --check path.slop      # parse only; does not catch runtime errors
```

The custom `run_slop` tool runs one `.slop` file and returns stdout, stderr, and
exitCode. Do not try to read `.env`; `opencode.jsonc` denies `*.env` reads.

## Pipeline and layout

- `sloperator.py`: CLI entrypoint. `--check` only lexes/parses and never evaluates.
- `sloperator/runner.py`: `check_program`, `run_program`, and `run_source`
  (in-memory `RunResult` used by most tests).
- `sloperator/lexer/`: `scanner.py` produces tokens; token types/keywords live in `tokens.py`.
- `sloperator/parser/`: `parse(tokens) -> list[Stmt]`; frozen dataclass AST in `ast.py`.
- `sloperator/evaluator/`: tree-walking `Interpreter`, scope `Environment`/binding kinds,
  and runtime `Value` helpers in `values.py`.
- `playground/server.py`: standalone HTTP playground; shells out to the CLI per request
  (5-second timeout) and appends JSON to `logs/runs.log` (gitignored).

## Language and implementation gotchas

- Source is Unicode-significant: `✨` ends statements, `“ ”` quote strings, `—` starts
  comments, `✅`/`❌` are booleans. Preserve these exactly in tests and examples; never
  replace them with ASCII. Straight quotes, `;`, `//`, and en dash `–` are intentional
  lexical errors with corrective messages. A U+FE0F variation selector after an emoji
  is accepted.
- Always use the `TokenType` enum in `tokens.py`; never compare raw strings or numeric values for token kinds.
- AST nodes are frozen dataclasses in `ast.py`. Maintain strict type annotations (`typing` primitives / `Self`) and immutability when introducing or modifying nodes.
- Avoid bare `Any`. Type all new function signatures and public evaluator methods strictly.
- `hallucinate` is the only built-in. `ship` is only valid inside a `clanker`, and
  clankers are top-level only. No floats, arrays, or nested functions.
- Python `bool` is an `int` subclass. Use `is_number()`/`type_name()`/explicit `bool`
  checks when editing evaluator code; do not use bare `isinstance(x, int)` for numbers.
- Arithmetic on mixed types is a runtime error (no coercion). Division truncates toward
  zero (`-7 / 2` is `-3`). Runtime errors never leak tracebacks; `RecursionError`
  becomes a runtime "stack overflow" (call-depth cap 500).

## Known divergences from `docs/spec.md` (verified)

Trust the interpreter behavior here; update tests/spec deliberately if fixing:

- `ralph` executes its body once before testing the condition, so `ralph ❌ { ... }`
  runs one iteration.
- A bare `{ ... }` block statement inside a `clanker` is parented to `globals`, so it
  cannot see the function's parameters/locals (unlike `vibe`/`ralph` bodies).
- `comparison()` calls `equality()`, so equality binds tighter than comparison — the
  opposite of the spec; mixing `<` and `==` misparses. Use parentheses in tests.
- Identifier scanning stops at digits (`is_identifier_char` only accepts letters/`_`),
  so `x1` becomes two tokens despite the spec's `[A-Za-z_][A-Za-z0-9_]*`.

## Testing conventions

- Behavior/end-to-end: call `run_source` and assert the `RunResult` tuple
  (see `tests/test_evaluator.py`).
- Parser/AST boundary: `parse(tokenize(source))` and assert node types/fields
  (see `tests/test_parser.py`, `tests/test_nested_calls.py`).
- CLI: subprocess with `sys.executable` running `sloperator.py`, not the `uv` wrapper
  (see `tests/test_cli.py`).
- Every `.slop` in `examples/` is executed by `tests/test_examples.py`; each must exit 0,
  write nothing to stderr, and produce non-empty stdout.
- Add both AST-shape and runtime tests for new expression/statement behavior.
