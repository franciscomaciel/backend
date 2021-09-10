# -*- coding: UTF-8 -*-
from datetime import datetime
from typing import Dict, Union

import uvicorn
from fastapi import FastAPI, HTTPException, status
# from starlette.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware  # from starlette.middleware.cors import CORSMiddleware

from auth import AuthHandler
from crud import existe_usuario
from crud import get_pedido_por_numero_pedido_filial, get_pedidos_bloqueados, get_pedidos_bloqueados_por_periodo, \
    get_bloqueios_pedido, get_itens_pedido, liberar_bloqueio, liberar_bloqueio_item
from schemas.schemas import SchemaLiberarPedido, SchemaLiberarItemPedido

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
"""
from routers import rotas_auth
coNNector.include_router(rotas_auth)
"""

@coNNector.get("/status-servidor/")
async def alive() -> Dict[str, datetime]:
    """ Retorna status e timestamp do servidor para conferir se o sistema está ativo """
    return { "status" : "OK",
             "timestamp": datetime.now()}


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


@coNNector.get("/pedidos/{id_pedido_filial}/", status_code=status.HTTP_200_OK)
async def um_pedido(id_pedido_filial: int) -> Dict[str, Union[float, int, str]]:
    result = get_pedido_por_numero_pedido_filial(id_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


@coNNector.post("/desbloquear-pedido/", status_code=status.HTTP_200_OK)
async def desbloquear_pedido(pedido: SchemaLiberarPedido):
    numero_pedido_filial = pedido.numero_pedido_filial
    codigo_usuario_liberador = pedido.codigo_usuario_liberador
    justificativa = pedido.justificativa
    liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa)


@coNNector.post("/desbloquear-item-pedido/", status_code=status.HTTP_200_OK)
async def desbloquear_item_pedido(item_pedido: SchemaLiberarItemPedido):
    numero_pedido_filial = item_pedido.numero_pedido_filial
    codigo_usuario_liberador = item_pedido.codigo_usuario_liberador
    justificativa = item_pedido.justificativa
    item_bloqueio = item_pedido.item_bloqueio
    liberar_bloqueio_item(numero_pedido_filial, item_bloqueio, codigo_usuario_liberador, justificativa)


@coNNector.get("/get-itens-pedido/{numero_pedido_filial}", status_code=status.HTTP_200_OK)
async def obter_itens_pedido(numero_pedido_filial: str):
    result = get_itens_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


@coNNector.get("/get-bloqueios-pedido/{numero_pedido_filial}", status_code=status.HTTP_200_OK)
async def obter_bloqueios_pedido(numero_pedido_filial: str):
    result = get_bloqueios_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )

"""
*!* VERIFICAR ESTE MÉTODO:
@coNNector.post("/login")
def login(auth_details: AuthDetails):
    user = None
    #  TODO: *!* Implementar localização do usuário com o SQLAlchemy
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Login ou senha inválido.')
    token = auth_handler.encode_token(user['auth_details'])
    return { 'token': token }
"""


@coNNector.get("/existe-usuario/{login_usuario}", status_code=status.HTTP_200_OK)
async def verificar_existencia_usuario(login_usuario: str):
    result = existe_usuario(login_usuario)
    if result:
        return { "msg": "Usuário localizado com sucesso"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum usuário cadastrado com esse login.",
        )


@coNNector.get("/", status_code=status.HTTP_200_OK)
async def inicio():
    """ Redireciona o usuário para o endpoint /status-servidor/ , se nenhum outro endpoint for fornecido """
    await alive()


if __name__ == '__main__':
    uvicorn.run(coNNector, host='0.0.0.0', port=8000)
