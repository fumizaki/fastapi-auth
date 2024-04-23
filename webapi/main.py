from fastapi import FastAPI
from src.presentation.controller import AuthenticationController


app = FastAPI()
app.include_router(AuthenticationController.router)
