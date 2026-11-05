"""Regression test: unary minus accepts only numbers, never booleans.

Python's ``bool`` is a subclass of ``int``, so a naive ``isinstance`` check
would let ``-✅`` through as ``-1``. This pins the runtime error instead.
"""

import pytest

from sloperator.runner import run_source


@pytest.mark.parametrize("boolean", ["✅", "❌"])
def test_unary_minus_rejects_boolean_operands(boolean: str):
    result = run_source(f"hallucinate(-{boolean})✨")

    assert result.exit_code == 1
    assert result.stderr == (
        "SlopLang runtime error at line 1: operand of unary '-' must be a number, got boolean\n"
    )
