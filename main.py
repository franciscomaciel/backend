# -*- coding: UTF-8 -*-
import uvicorn
from fastapi import FastAPI
# from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.cors import CORSMiddleware

from auth import AuthHandler


# CORS
origins = [
    "http://10.10.10.236:3000",
]


coNNector = FastAPI()
auth_handler = AuthHandler()

# Autorizando a política de Cross-Origin Resource Sharing (CORS)
coNNector.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Rotas para a aplicação:
from routers import rotas_pedidos
coNNector.include_router(rotas_pedidos.router_pedidos)


if __name__ == '__main__':
    uvicorn.run(coNNector, host='0.0.0.0', port=8000)
