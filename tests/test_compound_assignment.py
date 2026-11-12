from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def fails(source: str) -> str:
    result = run_source(source)
    assert result.exit_code == 1
    return result.stderr.rstrip("\n")


def test_compound_assignment_adds_rhs_expression():
    source = """\
slop n = 2✨
n += 3 * 4✨
hallucinate(n)✨
"""
    assert run(source) == "14\n"


def test_compound_assignment_accumulates_across_statements():
    source = """\
slop n = 1✨
n += 2✨
n += 3✨
hallucinate(n)✨
"""
    assert run(source) == "6\n"


def test_compound_assignment_can_use_the_target_on_both_sides():
    source = """\
slop n = 3✨
n += n✨
hallucinate(n)✨
"""
    assert run(source) == "6\n"


def test_compound_assignment_concatenates_strings():
    source = """\
slop greeting = “hello”✨
greeting += “ world”✨
hallucinate(greeting)✨
"""
    assert run(source) == "hello world\n"


def test_compound_assignment_updates_the_nearest_enclosing_binding():
    source = """\
slop n = 1✨
{
    n += 2✨
}
hallucinate(n)✨
"""
    assert run(source) == "3\n"


def test_compound_assignment_to_a_constant_is_an_error():
    source = """\
loadbearing MAX = 3✨
MAX += 1✨
"""
    assert fails(source) == "SlopLang runtime error at line 2: cannot assign to loadbearing 'MAX'"


def test_compound_assignment_to_an_undefined_name_is_an_error():
    assert (
        fails("missing += 1✨") == "SlopLang runtime error at line 1: undefined variable 'missing'"
    )


def test_compound_assignment_to_a_clanker_is_an_error():
    source = """\
clanker f() {
}
f += 1✨
"""
    assert (
        fails(source) == "SlopLang runtime error at line 3: cannot assign to immutable binding 'f'"
    )


def test_compound_assignment_rejects_mismatched_types():
    source = """\
slop n = 1✨
n += “one”✨
"""
    assert fails(source) == (
        "SlopLang runtime error at line 2: operands of '+=' must both be numbers or both be "
        "strings, got number and string"
    )
