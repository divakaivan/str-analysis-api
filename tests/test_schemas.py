import pytest

from pydantic import ValidationError

from src.schemas import StrInput


def test_strinput_validation_empty():
    with pytest.raises(ValidationError):
        StrInput(str_input="")


def test_strinput_accepts_valid_string():
    v = "a valid string"
    si = StrInput(str_input=v)
    assert si.str_input == v


def test_strinput_too_long_raises():
    long_s = "x" * 100001
    with pytest.raises(ValidationError):
        StrInput(str_input=long_s)
