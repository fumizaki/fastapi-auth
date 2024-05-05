from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from src.presentation.dependency.AuthorizationDependency import AuthorizationDependency
from src.application.usecase.AuthorizationUsecase import AuthorizationUsecase
from src.domain.v1.schema.AuthorizationSchema import (
    AuthorizeRequestSchema, AuthorizeResponseSchema, 
    TokenRequestSchema, TokenResponseSchema, TokenRefreshRequestSchema,
    TokenIntrospectRequestSchema, TokenIntrospectResponseSchema
)


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
async def v1_authorize(query: AuthorizeRequestSchema = Depends(), usecase: AuthorizationUsecase = Depends(AuthorizationDependency.depends)) -> ORJSONResponse:
    try:
        result: AuthorizeResponseSchema = usecase.v1_authorize_exec(AuthorizeRequestSchema(**query.__dict__))
        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post(
    path=V1_TOKEN,
    summary="アクセストークンの発行",
    status_code=status.HTTP_200_OK
)
async def v1_token(form: TokenRequestSchema, usecase: AuthorizationUsecase = Depends(AuthorizationDependency.depends)) -> ORJSONResponse:
    try:
        result: TokenResponseSchema = usecase.v1_token_exec(form)
        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post(
    path=V1_TOKEN_REFRESH,
    summary="アクセストークンのリフレッシュ",
    status_code=status.HTTP_200_OK
)
async def v1_token_refresh(form: TokenRefreshRequestSchema, usecase: AuthorizationUsecase = Depends(AuthorizationDependency.depends)) -> ORJSONResponse:
    try:
        result: TokenResponseSchema = usecase.v1_token_refresh_exec(form)
        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    path=V1_TOKEN_INTROSPECT,
    summary="アクセストークンの検証",
    status_code=status.HTTP_200_OK
)
async def v1_token_introspect(form: TokenIntrospectRequestSchema, usecase: AuthorizationUsecase = Depends(AuthorizationDependency.depends)) -> ORJSONResponse:
    try:
        result: TokenIntrospectResponseSchema = usecase.v1_token_introspect_exec(form)
        return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))