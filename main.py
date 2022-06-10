# -*- coding: UTF-8 -*-
import uvicorn
import logging
import fastapi as _fastapi
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from routers import rotas_pedidos, rotas_auth
from config.general_config import Config


# CORS
origins = [
    "http://10.10.10.236",          # Apenas para execução local; remover em produção.
    "http://10.10.10.236:3000",     # Apenas para execução local; remover em produção.
    "http://localhost:3000",        # Apenas para execução local; remover em produção.
    "http://0.0.0.0:8000",
    f'{Config.PRODUCTION_SERVER_IP}:3000',
]


# coNNector = _fastapi.FastAPI()


middleware = [
    Middleware(CORSMiddleware, allow_origins=origins)
]

coNNector = _fastapi.FastAPI(middleware=middleware)
logging.basicConfig(filename='connector_web.log', encoding='utf-8', level=logging.DEBUG)


# Autorizando a política de Cross-Origin Resource Sharing (CORS)
coNNector.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas de negócio:
coNNector.include_router(rotas_pedidos.router_pedidos)
# Rotas de segurança:
coNNector.include_router(rotas_auth.router_autorizacao)


if __name__ == '__main__':
    uvicorn.run("main:coNNector", host='0.0.0.0', port=8000, reload=True)
