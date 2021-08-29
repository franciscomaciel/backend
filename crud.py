import json
import decimal, datetime
import databases
from schemas.schemas import Usuario
from infra.providers import hash_provider

def get_pedidos_bloqueados():
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio," \
                   "P.nu_pedido_filial PedidoFilial  " \
                   " FROM CTL.PEDIDOS P, CTL.CLIENTES C, CTL.TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND V.COD_VEND=P.COD_VEND1 " \
                   "      AND P.FL_DOLAR='N' " \
                   "      AND P.Fl_Bloqueio='S' " \
                   "      AND P.Situacao='N' " \
                   "      AND P.FL_ANALISE_CRITICA='N' " \
                   "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                   " ORDER BY  P.data_emissao DESC, P.filial, P.nu_pedido"
    try:
        registros = databases.engine.execute(str_consulta)
        result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    except Exception as instancia:
        result = {"erro" : instancia}
    return result


def get_pedidos_bloqueados_por_periodo(data_ini, data_fim):
    if (not data_ini) or (not data_fim):
        raise Exception("Devem ser fornecidas as datas iniciais e finais.")
    else:
        str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                       "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                       "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio," \
                       "P.nu_pedido_filial PedidoFilial  " \
                       " FROM CTL.PEDIDOS P, CTL.CLIENTES C, CTL.TABVENDEDOR V " \
                       " WHERE C.cgc_cpf=P.cgc_cpf " \
                       "      AND V.COD_VEND=P.COD_VEND1 " \
                       "      AND P.FL_DOLAR='N' " \
                       "      AND P.Fl_Bloqueio='S' " \
                       "      AND P.Situacao='N' " \
                       "      AND P.FL_ANALISE_CRITICA='N' " \
                       "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                       "      AND (P.DATA_ENTRADA >= TO_DATE('" + data_ini + "', 'DD/MM/YYYY'))" \
                       "      AND (P.DATA_ENTRADA <= TO_DATE('" + data_fim+ "', 'DD/MM/YYYY'))" \
                       " ORDER BY  P.data_emissao, P.filial, P.nu_pedido"
        registros = databases.engine.execute(str_consulta)
        result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
        return result


# Exemplo do formato em que as datas devem ser fornecidas.: p_data_inicio = '01-DEC-20', p_data_fim='31-DEC-20'
def listar_pedidos(p_data_inicio, p_data_fim):
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio " \
                   "P.nu_pedido_filial PedidoFilial " \
                   " FROM CTL.PEDIDOS P, CTL.CLIENTES C, CTL.TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND V.COD_VEND=P.COD_VEND1 " \
                   "      AND P.FL_DOLAR='N' " \
                   "      AND P.data_emissao BETWEEN :p_data_inicio " \
                   "      AND :p_data_fim " \
                   "      AND P.Fl_Bloqueio='S' " \
                   "      AND P.Situacao='N' " \
                   "      AND P.FL_ANALISE_CRITICA='N' " \
                   "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                   " ORDER BY  P.data_emissao, P.filial, P.nu_pedido"
    registros = databases.engine.execute(str_consulta,
                                         {'p_data_inicio': f'"{p_data_inicio}"' , 'p_data_fim': f'"{p_data_fim}"' })
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result


def get_pedido_por_numero(numero_pedido):
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio, " \
                   "P.nu_pedido_filial PedidoFilial " \
                   " FROM CTL.PEDIDOS P, CTL.CLIENTES C, CTL.TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND P.NU_PEDIDO=:p_numero_pedido " \
                   "      AND V.COD_VEND=P.COD_VEND1 "
    registros = databases.engine.execute(str_consulta, {'p_numero_pedido': f'{numero_pedido}'})
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result

def get_bloqueios_pedido(numero_pedido_filial):
    str_consulta = "SELECT DS_MOTIVO, DT_INCLUSAO, SUBSTR(ds_motivo,1,1) ITEM_MOTIVO " \
                   " FROM CTL.BLOQUEIO_PEDIDO " \
                   " WHERE NU_PEDIDO_FILIAL =:p_numero_pedido_filial AND DS_MOTIVO!='DESBLOQUEADO'"
    registros = databases.engine.execute(str_consulta, {'p_numero_pedido_filial': f'{numero_pedido_filial}'})
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result


def get_itens_pedido(numero_pedido_filial):
    str_consulta = "SELECT I.NU_PED_FIL_ITEM NU_PEDIDO_FILIAL, I.NU_ITEM NU_ITEM, " \
                   "       I.COD_PROD CODIGO_PRODUTO, " \
                   "       I.DESCR_PROD DESCRICAO_PRODUTO, " \
                   "       I.QUANTIDADE QUANTIDADE," \
                   "       I.PRECO_UNIT PRECO_UNITARIO, " \
                   "       (I.QUANTIDADE / PP.QT_EMB) VOLUMES, " \
                   "       (I.QUANTIDADE * I.PRECO_UNIT) VALOR, " \
                   "       I.CUSTO_MEDIO CUSTO_MEDIO, " \
                   "       ((100 * I.VL_MB) / (I.PRECO_UNIT + (I.PRECO_UNIT*I.PERC_IPI/100))) PERC_MB " \
                   " FROM CTL.ITENS I, CTL.PRODUTO_PIRAMIDE PP " \
                   " WHERE NU_PED_FIL_ITEM like '" + numero_pedido_filial + "%' " \
                   "       AND PP.CD_ESTOQUE = I.COD_PROD " \
                   " ORDER BY I.NU_ITEM"
    registros = databases.engine.execute(str_consulta)
    # registros = databases.engine.execute(str_consulta, {'p_npf': f'{numero_pedido_filial}' })
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result

def liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa):
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    conn = databases.engine.connect()
    trans = conn.begin()
    str_consulta1 = "UPDATE CTL.BLOQUEIO_PEDIDO SET dt_liberado=systimestamp, " \
                    "                           hr_liberado=SUBSTR(TO_CHAR(systimestamp, 'HH24MIssFF'),1,8), " \
                    "                           cd_usuario=\'" + codigo_usuario_liberador + "\', " \
                    "                           ds_Justificativa='" + justificativa + "', " \
                    "                           ds_motivo = 'DESBLOQUEADO' " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'" # AND SUBSTR(ds_motivo,1,1)=\'3\'"
    databases.engine.execute(str_consulta1)
    # Depois, a tabela PEDIDOS:
    str_consulta2 = "UPDATE CTL.PEDIDOS SET fl_bloqueio='N', dt_liberado=systimestamp, " \
                    "       hr_liberado=SUBSTR(TO_CHAR(systimestamp, \'HH24MIssFF\'),1,8), " \
                    "       cd_usuario=\'" + codigo_usuario_liberador + "\', ds_motivo='DESBLOQUEADO', " \
                    "       ds_Justificativa='" + justificativa + "', " \
                    "       dt_impressao_of=NULL, hr_impressao_of=NULL " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
    databases.engine.execute(str_consulta2)
    trans.commit()


def liberar_bloqueio_item(numero_pedido_filial, item_bloqueio, codigo_usuario_liberador, justificativa):
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    conn = databases.engine.connect()
    trans = conn.begin()
    str_consulta1 = "UPDATE CTL.BLOQUEIO_PEDIDO SET dt_liberado=systimestamp, " \
                    "                           hr_liberado=SUBSTR(TO_CHAR(systimestamp, 'HH24MIssFF'),1,8), " \
                    "                           cd_usuario=\'" + codigo_usuario_liberador + "\', " \
                    "                           ds_Justificativa='" + justificativa + "', " \
                    "                           ds_motivo = 'DESBLOQUEADO' " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\' AND SUBSTR(ds_motivo,1,1)=\'" + item_bloqueio + "\'"
    databases.engine.execute(str_consulta1)
    # Depois, a tabela PEDIDOS:
    str_consulta2 = "UPDATE CTL.PEDIDOS SET fl_bloqueio='N', dt_liberado=systimestamp, " \
                    "       hr_liberado=SUBSTR(TO_CHAR(systimestamp, \'HH24MIssFF\'),1,8), " \
                    "       cd_usuario=\'" + codigo_usuario_liberador + "\', ds_motivo='DESBLOQUEADO', " \
                    "       ds_Justificativa='" + justificativa + "', " \
                    "       dt_impressao_of=NULL, hr_impressao_of=NULL " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\' AND SUBSTR(ds_motivo,1,1)=\'" + item_bloqueio + "\'"
    databases.engine.execute(str_consulta2)
    trans.commit()


"""
def liberar_bloqueio(pedido: ModeloLiberarPedido):
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    numero_pedido_filial = pedido.numero_pedido_filial
    codigo_usuario_liberador = pedido.codigo_usuario_liberador
    justificativa = pedido.justificativa
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    conn = databases.engine.connect()
    trans = conn.begin()
    str_consulta1 = "UPDATE CTL.BLOQUEIO_PEDIDO SET dt_liberado=systimestamp, " \
                    "                           hr_liberado=SUBSTR(TO_CHAR(systimestamp, 'HH24MIssFF'),1,8), " \
                    "                           cd_usuario=\'" + codigo_usuario_liberador + "\', " \
                    "                           ds_Justificativa='" + justificativa + "', " \
                    "                           ds_motivo = 'DESBLOQUEADO' " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'" # AND SUBSTR(ds_motivo,1,1)=\'3\'"
    databases.engine.execute(str_consulta1)
    # Depois, a tabela PEDIDOS:
    str_consulta2 = "UPDATE CTL.PEDIDOS SET fl_bloqueio='N', dt_liberado=systimestamp, " \
                    "       hr_liberado=SUBSTR(TO_CHAR(systimestamp, \'HH24MIssFF\'),1,8), " \
                    "       cd_usuario=\'" + codigo_usuario_liberador + "\', ds_motivo='DESBLOQUEADO', " \
                    "       ds_Justificativa='" + justificativa + "', " \
                    "       dt_impressao_of=NULL, hr_impressao_of=NULL " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
    databases.engine.execute(str_consulta2)
    trans.commit()
"""


def existe_usuario(login_ad: str):
    str_consulta = "SELECT * " \
                   " FROM CTL.WCONNECTOR_CREDENCIAL " \
                   " WHERE CD_LOGIN_AD = \'" + login_ad +  "\' "
    registros = databases.engine.execute(str_consulta)
    rows_amount = 0
    for row in registros:
        rows_amount += 1
    result = (rows_amount > 0)
    return result


""" Função JSON encoder para as classes do SQLAlchemy."""
def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
