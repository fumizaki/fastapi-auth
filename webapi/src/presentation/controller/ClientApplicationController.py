from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import ORJSONResponse
from src.presentation.dependency.ClientApplicationDependency import ClientApplicationDependency
from src.application.usecase.ClientApplicationUsecase import ClientApplicationUsecase
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.schema.ClientApplicationSchema import CreateClientApplicationSchema
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity

V1_LIST_CLIENT_APPLICATION = "/v1/list/client/application"
V1_GET_CLIENT_APPLICATION = "/v1/get/client/application/{id}"
V1_CREATE_CLIENT_APPLICATION = "/v1/create/client/application"


router = APIRouter(tags=["ClientApplication"], default_response_class=ORJSONResponse)


@router.get(
    path=V1_LIST_CLIENT_APPLICATION,
    summary="クライアントアプリケーションの一覧取得",
    status_code=status.HTTP_200_OK
)
async def v1_list_client_application(usecase: ClientApplicationUsecase = Depends(ClientApplicationDependency.depends)):
    results: list[Optional[ClientApplicationEntity]] = usecase.v1_list_client_application_exec()
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=([result.model_dump() for result in results] if len(results) > 0 else [])
        )


@router.get(
    path=V1_GET_CLIENT_APPLICATION,
    summary="クライアントアプリケーションの取得",
    status_code=status.HTTP_200_OK
)
async def v1_get_client_application(id: RecordId, usecase: ClientApplicationUsecase = Depends(ClientApplicationDependency.depends)):
    result: ClientApplicationEntity = usecase.v1_get_client_application_exec(id)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )


@router.post(
    path=V1_CREATE_CLIENT_APPLICATION,
    summary="クライアントアプリケーションの新規作成",
    status_code=status.HTTP_200_OK
)
async def v1_create_client_application(form: CreateClientApplicationSchema, usecase: ClientApplicationUsecase = Depends(ClientApplicationDependency.depends)):
    result: ClientApplicationEntity = usecase.v1_create_client_application_exec(form)
    return ORJSONResponse(
            status_code=status.HTTP_200_OK,
            content=(result.model_dump())
        )
