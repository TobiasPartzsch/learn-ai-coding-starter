# Sloperator

A tree-walking [SlopLang](docs/spec.md) interpreter written in Python.

## Quick Start

```bash
uv run sloperator.py path/to/program.slop          # run a program
uv run sloperator.py --check path/to/program.slop  # check syntax only
```

## Validation

```bash
uv run pytest               # tests
uv run ruff format --check  # formatting
uv run ruff check           # linting
uv run ty check             # type checking
```

## Playground

```bash
uv run playground/server.py
```

Open <http://localhost:8080>.

## Language

See [docs/spec.md](docs/spec.md) for the full specification: slop words, values,
scoping, and control flow. A taste:

```slop
— Comments start with an em dash. Statements end with sparkles.
clanker describe(count) {
    vibe count > 1 {
        ship “big slop”✨
    } nah {
        ship “small slop”✨
    }
}
```

## Layout

`sloperator.py` is the CLI entrypoint; `sloperator/` holds the lexer, parser,
evaluator, and `runner.py`. `docs/spec.md` is the spec; `examples/` and
`tests/` hold examples and tests; `playground/` is a small web editor.
