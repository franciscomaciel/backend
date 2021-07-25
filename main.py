# -*- coding: UTF-8 -*-
import uvicorn

from datetime import datetime
from typing import Dict, Union
from fastapi import FastAPI, HTTPException, status
from crud import get_pedido_por_numero, get_pedidos, get_pedidos_bloqueados, liberar_bloqueio, \
                 get_pedidos_bloqueados_por_periodo, get_bloqueios_pedido, get_itens_pedido, \
                 liberar_bloqueio_item

# from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware # from starlette.middleware.cors import CORSMiddleware
from models import ModeloLiberarPedido, ModeloLiberarItemPedido


origins = [
    "http://10.10.10.236:3000",
]


coNNector = FastAPI()


# Autorizando a política de Cross-Origin Resource Sharing (CORS)
coNNector.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@coNNector.get("/status-servidor/")
async def alive() -> Dict[str, datetime]:
    """ Retorna status e timestamp do servidor para conferir se o sistema está ativo """
    return { "status" : "OK",
             "timestamp": datetime.now()}


@coNNector.get("/pedidos/", status_code=status.HTTP_200_OK)
async def todos_pedidos():
    """ Retorna todos os pedidos cadastrados """
    result = get_pedidos()
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado.",
        )


@coNNector.get("/pedidos-bloqueados/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados():
    result = get_pedidos_bloqueados()
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido bloqueado.",
        )


@coNNector.get("/pedidos-bloqueados-por-periodo/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados_por_periodo(data_ini:str, data_fim:str):
    result = get_pedidos_bloqueados_por_periodo(data_ini, data_fim)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido bloqueado.",
        )


@coNNector.get("/pedidos/{id_pedido}/")
async def um_pedido(id_pedido: int) -> Dict[str, Union[float, int, str]]:
    result = get_pedido_por_numero(id_pedido)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


"""
@coNNector.get("/desbloquear-pedido/")
async def desbloquear_pedido(numero_pedido_filial: str, codigo_usuario_liberador: str, justificativa: str):
    liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa)
"""


@coNNector.post("/desbloquear-pedido/")
async def desbloquear_pedido(pedido: ModeloLiberarPedido):
    numero_pedido_filial = pedido.numero_pedido_filial
    codigo_usuario_liberador = pedido.codigo_usuario_liberador
    justificativa = pedido.justificativa
    liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa)


@coNNector.post("/desbloquear-item-pedido/")
async def desbloquear_item_pedido(item_pedido: ModeloLiberarItemPedido):
    numero_pedido_filial = item_pedido.numero_pedido_filial
    codigo_usuario_liberador = item_pedido.codigo_usuario_liberador
    justificativa = item_pedido.justificativa
    item_bloqueio = item_pedido.item_bloqueio
    liberar_bloqueio_item(numero_pedido_filial, item_bloqueio, codigo_usuario_liberador, justificativa)


@coNNector.get("/get-itens-pedido/{numero_pedido_filial}")
async def obter_itens_pedido(numero_pedido_filial: str):
    result = get_itens_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


@coNNector.get("/get-bloqueios-pedido/{numero_pedido_filial}")
async def obter_bloqueios_pedido(numero_pedido_filial: str):
    result = get_bloqueios_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )


@coNNector.post("/login")
def login():
    pass


@coNNector.get("/")
def inicio():
    """ Redireciona o usuário para o endpoint /status-servidor/ , se nenhum outro endpoint for fornecido """
    alive()


if __name__ == '__main__':
    uvicorn.run(coNNector, host='0.0.0.0', port=8000)
