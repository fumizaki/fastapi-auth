from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from src.presentation.dependency.AuthenticationDependency import AuthenticationDependency
from src.application.usecase.AuthenticationUsecase import AuthenticationUsecase
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.schema.AuthenticationSchema import SignUpSchema, SignInSchema
from src.domain.v1.entity.AccountEntity import AccountEntity

V1_SIGNUP = "/v1/oauth/signup"
V1_SIGNIN = "/v1/oauth/signin"
V1_EMAIL_VERIFICATION = "/v1/oauth/verify/email/{id}"


router = APIRouter(tags=["Authentication"], default_response_class=ORJSONResponse)

@router.post(
    path=V1_SIGNUP,
    summary="アカウントの新規登録",
    status_code=status.HTTP_200_OK
)
async def v1_signup(form: SignUpSchema, usecase: AuthenticationUsecase = Depends(AuthenticationDependency.depends)) -> ORJSONResponse:
    result: AccountEntity = usecase.v1_signup_exec(form)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
    
@router.post(
    path=V1_SIGNIN,
    summary="サインイン",
    status_code=status.HTTP_200_OK
)
async def v1_signin(form: SignInSchema, usecase: AuthenticationUsecase = Depends(AuthenticationDependency.depends)) -> ORJSONResponse:
    result: AccountEntity = usecase.v1_signin_exec(form)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )


@router.get(
    path=V1_EMAIL_VERIFICATION,
    summary="Email確認",
    status_code=status.HTTP_200_OK
)
async def v1_verify_email(id: RecordId, usecase: AuthenticationUsecase = Depends(AuthenticationDependency.depends)) -> ORJSONResponse:
    pass
