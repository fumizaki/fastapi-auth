from fastapi import FastAPI
from src.presentation.controller import (
    AuthenticationController,
    AuthorizationController,
    ClientApplicationController,
    ClientSecretController
)


app = FastAPI()
app.include_router(AuthenticationController.router)
app.include_router(AuthorizationController.router)
app.include_router(ClientApplicationController.router)
app.include_router(ClientSecretController.router)
