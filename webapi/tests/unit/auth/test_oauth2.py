import pytest
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client


@pytest.mark.parametrize(
    "expected, exp",
    [
        (True, 9999999999),
        (False, 0),
    ]
)
def test_is_effective(expected, exp):
    result = OAuth2Client.is_effective(exp)
    assert result == expected



@pytest.mark.parametrize(
    "expected, scopes, required_scopes",
    [
        (True, ["aaa", "bbb", "ccc"], ["aaa", "xxx", "yyy", "zzz"]),
        (True, ["aaa", "bbb", "ccc"], ["bbb", "xxx", "yyy", "zzz"]),
        (True, ["aaa", "bbb", "ccc"], ["ccc", "xxx", "yyy", "zzz"]),
        (False, ["aaa", "bbb", "ccc"], ["xxx", "yyy", "zzz"]),
    ]
)
def test_has_required_scope(expected, scopes, required_scopes):
    result = OAuth2Client.has_required_scope(scopes, required_scopes)
    assert result == expected