from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse




V1_AUTHORIZE = "/v1/oauth/authorize"
V1_TOKEN = "/v1/oauth/token"
V1_TOKEN_REFRESH = "/v1/oauth/token/refresh"
V1_TOKEN_INTROSPECT = "/v1/oauth/token/introspect"


router = APIRouter(tags=["Authorization"], default_response_class=ORJSONResponse)


@router.get(
    path=V1_AUTHORIZE,
    summary="認可コードの発行",
    status_code=status.HTTP_200_OK
)
async def v1_authorize():
    pass



@router.post(
    path=V1_TOKEN,
    summary="アクセストークンの発行",
    status_code=status.HTTP_200_OK
)
async def v1_token():
    pass



@router.post(
    path=V1_TOKEN_REFRESH,
    summary="アクセストークンのリフレッシュ",
    status_code=status.HTTP_200_OK
)
async def v1_token_refresh():
    pass


@router.post(
    path=V1_TOKEN_INTROSPECT,
    summary="アクセストークンの検証",
    status_code=status.HTTP_200_OK
)
async def v1_token_introspect():
    pass