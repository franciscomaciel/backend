# -*- coding: UTF-8 -*-
import uvicorn
import fastapi as _fastapi
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from routers import rotas_pedidos, rotas_auth


# CORS
origins = [
    "http://10.10.10.236",
    "http://0.0.0.0:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


# coNNector = _fastapi.FastAPI()


# Autorizando a política de Cross-Origin Resource Sharing (CORS)
"""
coNNector.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
"""
middleware = [
    Middleware(CORSMiddleware, allow_origins=origins)
]

coNNector = _fastapi.FastAPI(middleware=middleware)

# Rotas de negócio:
coNNector.include_router(rotas_pedidos.router_pedidos)
# Rotas de segurança:
coNNector.include_router(rotas_auth.router_autorizacao)


if __name__ == '__main__':
    uvicorn.run("main:coNNector", host='0.0.0.0', port=8000, reload=True)
