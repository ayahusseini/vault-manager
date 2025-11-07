import pytest

from vault_manager.pattern_extractor import add, subtract, multiply, divide


def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2
    with pytest.raises(TypeError):
        add("1", 2)
    with pytest.raises(TypeError):
        add(1, "2")
    with pytest.raises(TypeError):
        add("1", "2")
