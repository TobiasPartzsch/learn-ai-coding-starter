from sloperator.runner import run_source


def test_ralph_with_false_condition_never_runs_the_body():
    result = run_source("ralph ❌ {\n    hallucinate(“never”)✨\n}\n")

    assert (result.stdout, result.stderr, result.exit_code) == ("", "", 0)
