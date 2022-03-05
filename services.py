import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import json
import decimal, datetime
import database
from fastapi import Depends, HTTPException, status
import providers.hash_provider as _hash
import providers.token_provider as _token
import schemas, models
from config import config
from providers import token_provider
from jose import JWTError

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/token")

""" Função JSON encoder para as classes do SQLAlchemy."""
def alchemyencoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


def get_db():
    print('**!** Chamou get_db()')
    db = database.SessionLocal()
    print('**!** Instanciou SessionLocal.')
    try:
        print('**!** Retornou uma sessão do BD.')
        yield db
    finally:
        db.close()


async def existe_usuario(login_ad: str):
    str_consulta = "SELECT * " \
                   " FROM WCONNECTOR_CREDENCIAL " \
                   " WHERE LOGIN_AD = UPPER(\'" + login_ad + "\') "
    registros = database.engine.execute(str_consulta)
    rows_amount = 0
    for row in registros:
        rows_amount += 1
    result = (rows_amount > 0)
    return result


async def criar_usuario(usuario: schemas.UserCreate, session: _orm.Session):
    usuario_bd = models.Usuario(login_ad=usuario.login_ad, hash_senha=_hash.gerar_hash(usuario.senha),
                                temp_passwd='', flag_admin='N')
    session.add(usuario_bd)
    session.commit()
    session.refresh(usuario_bd)
    return usuario_bd
"""
    conn = database.engine.connect()
    trans = conn.begin()
    try:
        str_consulta = 'INSERT INTO WCONNECTOR_CREDENCIAL (login_ad, hash_senha, flag_admin) ' \
                        'VALUES     (\'{login_ad}\', \'{senha}\',\'N\')'.format(login_ad=usuario.login_ad, senha=_hash.bcrypt.hash(usuario.senha))
        database.engine.execute(str_consulta)
    except:
        trans.rollback()
        raise
    else:
        trans.commit()
"""


async def get_usuario_by_login_ad(login_ad: str, session: _orm.Session):
    result = session.query(models.Usuario).filter(models.Usuario.login_ad == login_ad).first()
    return result


async def autenticar_usuario(login_ad: str, senha: str, session: _orm.Session):
    usuario = await get_usuario_by_login_ad(login_ad=login_ad, session=session)
    if not usuario:
        return False
    if not usuario.verificar_senha(senha):
        return False
    return usuario

async def criar_token(usuario: models.Usuario):
    return _token.criar_access_token({'sub': usuario.login_ad})

    # return dict(access_token={
    #             "sub": usuario.login_ad,
    #             "token_type": "bearer"})

async def get_usuario_atual(session: _orm.Session = _fastapi.Depends(get_db), token: str = _fastapi.Depends(oauth2schema)):
    try:
        payload = token_provider.verificar_access_token(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        usuario = session.query(models.Usuario).get(payload["login_ad"])
    except:
        raise _fastapi.HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Login do AD ou senha inválida.")
    return schemas.User.from_orm(usuario)

def get_pedidos_bloqueados():
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio," \
                   "P.nu_pedido_filial PedidoFilial  " \
                   " FROM PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND V.COD_VEND=P.COD_VEND1 " \
                   "      AND P.FL_DOLAR='N' " \
                   "      AND P.Fl_Bloqueio='S' " \
                   "      AND P.Situacao='N' " \
                   "      AND P.FL_ANALISE_CRITICA='N' " \
                   "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                   " ORDER BY  P.data_emissao DESC, P.filial, P.nu_pedido"
    try:
        registros = database.engine.execute(str_consulta)
        result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    except Exception as instancia:
        result = {"erro": instancia}
    return result


def get_pedidos_bloqueados_por_filial(filial):
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio," \
                   "P.nu_pedido_filial PedidoFilial  " \
                   " FROM PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND V.COD_VEND=P.COD_VEND1 " \
                   "      AND P.FILIAL='" + filial + "' " \
                                                     "      AND P.FL_DOLAR='N' " \
                                                     "      AND P.Fl_Bloqueio='S' " \
                                                     "      AND P.Situacao='N' " \
                                                     "      AND P.FL_ANALISE_CRITICA='N' " \
                                                     "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                                                     " ORDER BY  P.data_emissao DESC, P.filial, P.nu_pedido"
    try:
        registros = database.engine.execute(str_consulta)
        result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    except Exception as instancia:
        result = {"erro": instancia}
    return result


def get_pedidos_bloqueados_por_periodo(data_ini, data_fim):
    if (not data_ini) or (not data_fim):
        raise Exception("Devem ser fornecidas as datas iniciais e finais.")
    else:
        str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                       "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                       "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio," \
                       "P.nu_pedido_filial PedidoFilial  " \
                       " FROM PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
                       " WHERE C.cgc_cpf=P.cgc_cpf " \
                       "      AND V.COD_VEND=P.COD_VEND1 " \
                       "      AND P.FL_DOLAR='N' " \
                       "      AND P.Fl_Bloqueio='S' " \
                       "      AND P.Situacao='N' " \
                       "      AND P.FL_ANALISE_CRITICA='N' " \
                       "      AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S')  " \
                       "      AND (P.DATA_ENTRADA >= TO_DATE('" + data_ini + "', 'DD/MM/YYYY'))" \
                       "      AND (P.DATA_ENTRADA <= TO_DATE('" + data_fim + "', 'DD/MM/YYYY'))" \
                       " ORDER BY  P.data_emissao, P.filial, P.nu_pedido"

        registros = database.engine.execute(str_consulta)
        result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
        return result


# Exemplo do formato em que as datas devem ser fornecidas.: p_data_inicio = '01-DEC-20', p_data_fim='31-DEC-20'
def listar_pedidos(p_data_inicio, p_data_fim):
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio " \
                   "P.nu_pedido_filial PedidoFilial " \
                   " FROM PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
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
    registros = database.engine.execute(str_consulta,
                                        {'p_data_inicio': f'"{p_data_inicio}"', 'p_data_fim': f'"{p_data_fim}"'})
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result


def get_pedido_por_numero_pedido_filial(numero_pedido_filial):
    str_consulta = "SELECT V.NOME Vendedor, C.NOME Cliente, P.filial Filial, P.nu_pedido Pedido, " \
                   "P.vl_pedido Valor, P.DESCR_MOEDA DS_MOEDA, P.cod_fiscal||P.sequencia CD_CFO, " \
                   "P.data_emissao Emissao, P.DATA_ENTRADA Entrada, P.Ds_Motivo MotivoBloqueio, " \
                   "P.nu_pedido_filial PedidoFilial " \
                   " FROM PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
                   " WHERE C.cgc_cpf=P.cgc_cpf " \
                   "      AND P.NU_PEDIDO_FILIAL=:p_numero_pedido_filial " \
                   "      AND V.COD_VEND=P.COD_VEND1 "
    registros = database.engine.execute(str_consulta, {'p_numero_pedido_filial': f'{numero_pedido_filial}'})
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result


def get_bloqueios_pedido(numero_pedido_filial):
    str_consulta = "SELECT DS_MOTIVO, DT_INCLUSAO, SUBSTR(ds_motivo,1,1) ITEM_MOTIVO " \
                   " FROM BLOQUEIO_PEDIDO " \
                   " WHERE NU_PEDIDO_FILIAL =:p_numero_pedido_filial AND DS_MOTIVO!='DESBLOQUEADO' AND "\
                   "       DT_LIBERADO IS NULL"
    registros = database.engine.execute(str_consulta, {'p_numero_pedido_filial': f'{numero_pedido_filial}'})
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
                   " FROM ITENS I, PRODUTO_PIRAMIDE PP " \
                   " WHERE NU_PED_FIL_ITEM like '" + numero_pedido_filial + "%' " \
                                                                            "       AND PP.CD_ESTOQUE = I.COD_PROD " \
                                                                            " ORDER BY I.NU_ITEM"
    registros = database.engine.execute(str_consulta)
    # registros = database.engine.execute(str_consulta, {'p_npf': f'{numero_pedido_filial}' })
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result


def liberar_bloqueio(numero_pedido_filial, codigo_usuario_liberador, justificativa):
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    conn = database.engine.connect()
    trans = conn.begin()
    try:
        str_consulta1 = "UPDATE BLOQUEIO_PEDIDO SET dt_liberado=systimestamp, " \
                        "                           hr_liberado=SUBSTR(TO_CHAR(systimestamp, 'HH24MIssFF'),1,8), " \
                        "                           cd_usuario=\'" + codigo_usuario_liberador + "\', " \
                        "                           ds_Justificativa='" + justificativa + "', " \
                                                                                                                                                                  "                           ds_motivo = 'DESBLOQUEADO' " \
                                                                                                                                                                  " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"  # AND SUBSTR(ds_motivo,1,1)=\'3\'"
        database.engine.execute(str_consulta1)
        # Depois, a tabela PEDIDOS:
        str_consulta2 = "UPDATE PEDIDOS SET ds_motivo='DESBLOQUEADO' " \
                        " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
        # str_consulta2 = "UPDATE PEDIDOS SET fl_bloqueio='N', dt_liberado=systimestamp, " \
        #                 "       hr_liberado=SUBSTR(TO_CHAR(systimestamp, \'HH24MIssFF\'),1,8), " \
        #                 "       cd_usuario=\'" + codigo_usuario_liberador + "\', ds_motivo='DESBLOQUEADO', " \
        #                 "       ds_Justificativa='" + justificativa + "', " \
        #                 "       dt_impressao_of=NULL, hr_impressao_of=NULL " \
        #                 " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
        database.engine.execute(str_consulta2)
    except:
        trans.rollback()
        raise
    else:
        trans.commit()


def liberar_bloqueio_item(numero_pedido_filial, item_bloqueio, codigo_usuario_liberador, justificativa):
    # Primeiro, atualizar a tabela BLOQUEIO_PEDIDO:
    conn = database.engine.connect()
    trans = conn.begin()
    str_consulta1 = "UPDATE BLOQUEIO_PEDIDO SET dt_liberado=systimestamp, " \
                    "                           hr_liberado=SUBSTR(TO_CHAR(systimestamp, 'HH24MIssFF'),1,8), " \
                    "                           cd_usuario=\'" + codigo_usuario_liberador + "\', " \
                                                                                            "                           ds_Justificativa='" + justificativa + "', " \
                                                                                                                                                              "                           ds_motivo = 'DESBLOQUEADO' " \
                                                                                                                                                              " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\' AND SUBSTR(ds_motivo,1,1)=\'" + item_bloqueio + "\'"
    database.engine.execute(str_consulta1)
    # Depois, a tabela PEDIDOS:
    str_consulta2 = "UPDATE PEDIDOS SET ds_motivo='DESBLOQUEADO' " \
                    " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
    # str_consulta2 = "UPDATE PEDIDOS SET fl_bloqueio='N', dt_liberado=systimestamp, " \
    #                 "       hr_liberado=SUBSTR(TO_CHAR(systimestamp, \'HH24MIssFF\'),1,8), " \
    #                 "       cd_usuario=\'" + codigo_usuario_liberador + "\', ds_motivo='DESBLOQUEADO', " \
    #                 "       ds_Justificativa='" + justificativa + "', " \
    #                 "       dt_impressao_of=NULL, hr_impressao_of=NULL " \
    #                 " WHERE nu_pedido_filial=\'" + numero_pedido_filial + "\'"
    database.engine.execute(str_consulta2)
    trans.commit()


def get_filiais_com_pedidos_bloqueados():
    str_consulta = "SELECT 	DISTINCT P.filial Filial " \
                   "        FROM 	PEDIDOS P, CLIENTES C, TABVENDEDOR V " \
                   "        WHERE C.cgc_cpf=P.cgc_cpf " \
                   "	            AND V.COD_VEND=P.COD_VEND1 " \
                   "                AND P.FL_DOLAR='N' " \
                   "                AND P.Fl_Bloqueio='S' " \
                   " 	            AND P.Situacao='N' " \
                   " 	            AND P.FL_ANALISE_CRITICA='N' " \
                   "                AND (P.Fl_Rejeitado is null or P.Fl_Rejeitado<>'S') " \
                   "        ORDER BY  P.filial"
    registros = database.engine.execute(str_consulta)
    # registros = database.engine.execute(str_consulta, {'p_npf': f'{numero_pedido_filial}' })
    result = json.dumps([dict(r) for r in registros], default=alchemyencoder)
    return result

async def get_usuario_atual(db: _orm.Session = Depends(get_db),
                      token: str = Depends(oauth2schema),
):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        login_ad = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception
    if not login_ad:
        raise exception
    usuario = await get_usuario_by_login_ad(login_ad, db)

    if not usuario:
        raise exception
    return usuario

"""
async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.Usuario).get(payload["login_ad"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return schemas.User.from_orm(user)

"""
