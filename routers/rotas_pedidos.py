from fastapi import APIRouter, status, HTTPException
from services import existe_usuario
from services import get_pedido_por_numero_pedido_filial, get_pedidos_bloqueados, get_pedidos_bloqueados_por_periodo, \
     get_filiais_com_pedidos_bloqueados, get_bloqueios_pedido, get_itens_pedido, liberar_bloqueio, \
     liberar_bloqueio_item, get_pedidos_bloqueados_por_filial
from schemas import SchemaLiberarPedido, SchemaLiberarItemPedido
from datetime import datetime
from typing import Dict, Union

router_pedidos = APIRouter()

@router_pedidos.get("/status-servidor/")
async def alive() -> Dict[str, datetime]:
    """ Retorna status e timestamp do servidor para conferir se o sistema está ativo """
    return { "status" : "OK",
             "timestamp": datetime.now()}


@router_pedidos.get("/pedidos-bloqueados/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados():
    result = get_pedidos_bloqueados()
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido bloqueado.",
        )


@router_pedidos.get("/pedidos-bloqueados-por-filial/{filial}/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados(filial:str):
    result = get_pedidos_bloqueados_por_filial(filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido bloqueado para a filial fornecida.",
        )


@router_pedidos.get("/get-filiais-com-pedidos-bloqueados/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados():
    result = get_filiais_com_pedidos_bloqueados()
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhuma filial com pedidos bloqueados.",
        )


@router_pedidos.get("/pedidos-bloqueados-por-periodo/", status_code=status.HTTP_200_OK)
async def pedidos_bloqueados_por_periodo(data_ini:str, data_fim:str):
    result = get_pedidos_bloqueados_por_periodo(data_ini, data_fim)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido bloqueado.",
        )


@router_pedidos.get("/pedidos/{id_pedido_filial}/", status_code=status.HTTP_200_OK)
async def um_pedido(id_pedido_filial: int) -> Dict[str, Union[float, int, str]]:
    result = get_pedido_por_numero_pedido_filial(id_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


@router_pedidos.post("/desbloquear-pedido/", status_code=status.HTTP_200_OK)
async def desbloquear_pedido(pedido: SchemaLiberarPedido):
    numero_pedido_filial = pedido.numero_pedido_filial
    codigo_usuario_liberador = pedido.codigo_usuario_liberador
    justificativa = pedido.justificativa
    liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa)


@router_pedidos.post("/desbloquear-item-pedido/", status_code=status.HTTP_200_OK)
async def desbloquear_item_pedido(item_pedido: SchemaLiberarItemPedido):
    numero_pedido_filial = item_pedido.numero_pedido_filial
    codigo_usuario_liberador = item_pedido.codigo_usuario_liberador
    justificativa = item_pedido.justificativa
    item_bloqueio = item_pedido.item_bloqueio
    liberar_bloqueio_item(numero_pedido_filial, item_bloqueio, codigo_usuario_liberador, justificativa)


@router_pedidos.get("/get-itens-pedido/{numero_pedido_filial}", status_code=status.HTTP_200_OK)
async def obter_itens_pedido(numero_pedido_filial: str):
    result = get_itens_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum pedido cadastrado com esse identificador.",
        )


@router_pedidos.get("/get-bloqueios-pedido/{numero_pedido_filial}", status_code=status.HTTP_200_OK)
async def obter_bloqueios_pedido(numero_pedido_filial: str):
    result = get_bloqueios_pedido(numero_pedido_filial)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado.",
        )


@router_pedidos.get("/existe-usuario/{login_usuario}", status_code=status.HTTP_200_OK)
async def verificar_existencia_usuario(login_usuario: str):
    result = existe_usuario(login_usuario)
    if result:
        return { "msg": "Usuário localizado com sucesso"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não há nenhum usuário cadastrado com esse login.",
        )
