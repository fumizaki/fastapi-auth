from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from src.presentation.dependency.AuthenticationDependency import AuthenticationDependency
from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema
from src.domain.v1.entity.AccountEntity import AccountEntity

V1_SIGNUP = "/v1/oauth/signup"


router = APIRouter(tags=["Authentication"], default_response_class=ORJSONResponse)

@router.post(
    path=V1_SIGNUP,
    summary="アカウントの新規登録",
    status_code=status.HTTP_200_OK
)
async def signup(form: SignUpSchema, usecase: AuthenticationUsecase = Depends(AuthenticationDependency.depends)):
    result: AccountEntity = await usecase.v1_signup_exec(form)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )