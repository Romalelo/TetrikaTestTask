import pytest
from solution import strict


@strict
def add(x: int, y: int) -> int:
    return x + y


@strict
def shout(text: str, excited: bool) -> str:
    return text.upper() + ("!" if excited else ".")


def test_add_correct():
    assert add(3, 4) == 7


def test_add_wrong_type():
    with pytest.raises(TypeError):
        add(3, "4")


def test_shout_correct():
    assert shout("hello", True) == "HELLO!"


def test_shout_wrong_type():
    with pytest.raises(TypeError):
        shout("hello", "yes")
