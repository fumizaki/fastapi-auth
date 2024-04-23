import pytest
from fastapi.testclient import TestClient
from main import app
from src.presentation.controller.AuthenticationController import V1_SIGNUP

client = TestClient(app)


@pytest.mark.parametrize(
    "expected, email, password",
    [
        (200, "test@test.com", "testtesttest"),
        (422, "test", "testtesttest"),
        (422, "test@test.com", "test"),
    ]
)
def test_v1_signup(expected, email, password):
    res = client.post(
        V1_SIGNUP,
        json = {
            "email": email,
            "password": password
        }
        )
    assert res.status_code == expected


