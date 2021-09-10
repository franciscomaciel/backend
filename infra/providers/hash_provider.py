from passlib.context import CryptContext

import config

pwd_context = CryptContext(schemes=[config.HASH_ALGORITHM])

def verificar_hash(texto_plano, texto_codificado):
    return pwd_context.verify(texto_plano, texto_codificado)

""" 
    Gera um hash de 60 caracteres, codificando o texto fornecido, de acordo com as configurações declaradas em 
    config.py"""
def gerar_hash(texto_plano):
    return pwd_context.hash(texto_plano)