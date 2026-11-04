"""Regression tests pinning lexer diagnostics.

These cover behavior that was previously wrong, so a failure here means a
diagnostic regression rather than a change to the language.
"""

import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


def test_lexical_error_after_an_em_dash_comment_reports_the_correct_line():
    """A comment must advance the scanner's line counter.

    The comment branch consumes its trailing newline with ``match("\\n")``;
    if that does not also increment ``line``, every error after a comment is
    attributed to the comment's line instead of the real one.
    """
    with pytest.raises(LexicalError) as info:
        tokenize("— comment on line one\n\"straight quotes on line two\"")

    assert info.value.message == "straight quotes are not supported, use “ and ” for strings"
    assert info.value.line == 2
    assert str(info.value) == (
        "SlopLang lexical error at line 2: "
        "straight quotes are not supported, use “ and ” for strings"
    )
