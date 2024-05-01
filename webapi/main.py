from fastapi import FastAPI
from src.presentation.controller import (
    AuthenticationController,
    ClientApplicationController,
    ClientSecretController
)


app = FastAPI()
app.include_router(AuthenticationController.router)
app.include_router(ClientApplicationController.router)
app.include_router(ClientSecretController.router)
