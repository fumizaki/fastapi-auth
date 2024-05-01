import pytest
from src.infrastructure.core.auth.util.OAuth2Client import OAuth2Client
from src.infrastructure.core.auth.model.OAuth2Model import AuthorizationToken, AuthorizationCode, Credential


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



def test_authorization_token():
    param = AuthorizationToken(
        sub="",
        iss=OAuth2Client.iss(),
        aud=OAuth2Client.aud(),
        exp=OAuth2Client.exp(),
        iat=OAuth2Client.iat()
    )
    token = OAuth2Client.create_authorization_token(param)
    assert isinstance(token, str)

    result = OAuth2Client.decode_authorization_token(token)
    assert isinstance(result, AuthorizationToken)


def test_authorization_code():
    param = AuthorizationCode(
        code="",
        client_id="",
        state=""
    )
    code = OAuth2Client.create_authorization_code(param)
    assert isinstance(code, str)

    result = OAuth2Client.decode_authorization_code(code)
    assert isinstance(result, AuthorizationCode)


@pytest.mark.parametrize(
    "sub, iss, aud, exp, iat, scope, jti, nonce, required_scopes",
    [
        ("", "fastapi-auth-server.com", "fastapi-auth", 5555555555, 1714574366, None, None, None, []),
        ("", "fastapi-auth-server.com", "fastapi-auth", 5555555555, 1714574366, "aaa", None, None, ["aaa", "bbb", "ccc"]),
    ]
)
def test_verify(sub, iss, aud, exp, iat, scope, jti, nonce, required_scopes):
    param = AuthorizationToken(
        sub=sub,
        iss=iss,
        aud=aud,
        exp=exp,
        iat=iat,
        scope=scope,
        jti=jti,
        nonce=nonce
    )
    token = OAuth2Client.create_authorization_token(param)
    credential = OAuth2Client.verify(required_scopes, token)
    assert isinstance(credential, Credential)


@pytest.mark.parametrize(
    "exception, sub, iss, aud, exp, iat, scope, jti, nonce, required_scopes",
    [
        (ValueError, "", "", "fastapi-auth", 5555555555, 1714574366, None, None, None, []),
        (ValueError, "", "fastapi-auth-server.com", "", 5555555555, 1714574366, "aaa", None, None, ["aaa", "bbb", "ccc"]),
        (ValueError, "", "fastapi-auth-server.com", "fastapi-auth", 5555555555, 1714574366, "xxx", None, None, ["aaa", "bbb", "ccc"]),
    ]
)
def test_verify_failed(exception, sub, iss, aud, exp, iat, scope, jti, nonce, required_scopes):
    param = AuthorizationToken(
        sub=sub,
        iss=iss,
        aud=aud,
        exp=exp,
        iat=iat,
        scope=scope,
        jti=jti,
        nonce=nonce
    )
    token = OAuth2Client.create_authorization_token(param)
    with pytest.raises(exception):
        OAuth2Client.verify(required_scopes, token)





