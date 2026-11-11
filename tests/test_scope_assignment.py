from sloperator.runner import run_source


def run(source: str) -> str:
    result = run_source(source)
    assert result.stderr == "", result.stderr
    return result.stdout


def test_nested_block_assignment_updates_enclosing_scope():
    source = """\
slop score = 1✨
{
    slop score = 2✨
    {
        score = 3✨
    }
    hallucinate(score)✨
}
hallucinate(score)✨
"""
    assert run(source) == "3\n1\n"


def test_assignment_targets_nearest_enclosing_declaration():
    source = """\
slop depth = 0✨
{
    slop depth = 1✨
    {
        slop depth = 2✨
        {
            depth = 3✨
        }
        hallucinate(depth)✨
    }
    hallucinate(depth)✨
}
hallucinate(depth)✨
"""
    assert run(source) == "3\n1\n0\n"


def test_nested_assignment_finds_enclosing_block_only_binding():
    source = """\
{
    slop flag = ✅✨
    {
        flag = ❌✨
    }
    hallucinate(flag)✨
}
"""
    assert run(source) == "❌\n"
