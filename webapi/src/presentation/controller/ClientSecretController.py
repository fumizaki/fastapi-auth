from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from src.presentation.dependency.ClientSecretDependency import ClientSecretDependency
from src.application.usecase.ClientSecretUsecase import ClientSecretUsecase
from src.domain.v1.type.ClientValueType import ApplicationId
from src.domain.v1.schema.ClientSecretSchema import CreateClientSecretSchema
from src.domain.v1.entity.ClientSecretEntity import ClientSecretEntity

V1_LIST_CLIENT_SECRET_LINKED_TO_APPLICATION = "/v1/list/client/{application_id}/secret"
V1_CREATE_CLIENT_SECRET = "/v1/create/client/secret"


router = APIRouter(tags=["ClientSecret"], default_response_class=ORJSONResponse)


@router.get(
    path=V1_LIST_CLIENT_SECRET_LINKED_TO_APPLICATION,
    summary="クライアントシークレットの取得",
    status_code=status.HTTP_200_OK
)
async def v1_list_client_secret_linked_to_application(application_id: ApplicationId, usecase: ClientSecretUsecase = Depends(ClientSecretDependency.depends)):
    results: list[Optional[ClientSecretEntity]] = usecase.v1_list_client_secret_linked_to_application_exec(application_id)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=([result.model_dump() for result in results] if len(results) > 0 else [])
        )
    
@router.post(
    path=V1_CREATE_CLIENT_SECRET,
    summary="クライアントシークレットの新規作成",
    status_code=status.HTTP_200_OK
)
async def v1_create_client_secret(form: CreateClientSecretSchema, usecase: ClientSecretUsecase = Depends(ClientSecretDependency.depends)):
    result: ClientSecretEntity = usecase.v1_create_client_secret_exec(form)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )