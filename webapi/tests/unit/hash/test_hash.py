import pytest
from src.infrastructure.core.hash.util.HashClient import HashClient



def test_generate_salt():
    salt = HashClient.salt()
    assert isinstance(salt, str)
    assert len(salt) == 32


def test_generate_stretching():
    stretching = HashClient.stretching()
    assert isinstance(stretching, int)


@pytest.mark.parametrize(
    "password, salt, stretching",
    [
        ("ABCDE", HashClient.salt(), HashClient.stretching()),
        ("12345", HashClient.salt(), HashClient.stretching()),
        ("ABCDE@12345", HashClient.salt(), HashClient.stretching())
    ]
)
def test_hash(password, salt, stretching):
    hashed = HashClient.hash(password, salt, stretching)
    assert isinstance(hashed, str)
    assert len(hashed) == 64


def test_hash_failed():
    with pytest.raises(ValueError):
        HashClient.hash("", "", 0)


@pytest.mark.parametrize(
    "expected, password, salt, stretching",
    [
        (True, "ABCDE", HashClient.salt(), HashClient.stretching()),
        (True, "12345", HashClient.salt(), HashClient.stretching()),
        (True, "ABCDE@12345", HashClient.salt(), HashClient.stretching())
    ]
)
def test_verify(expected, password, salt, stretching):
    hashed = HashClient.hash(password, salt, stretching)
    is_valid = HashClient.verify(password, salt, stretching, hashed)
    assert is_valid == expected


def test_verify_failed():
    is_valid = HashClient.verify("aaa", "bbb", 10, "ccc")
    assert is_valid == False