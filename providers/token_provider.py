from datetime import datetime, timedelta
from jose import jwt
from config.general_config import Config


def criar_access_token(data: dict):
    dados = data.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=Config.EXPIRES_IN_MIN)
    dados.update({'exp': expiracao})
    dados.update({'token_type': 'bearer'})
    token_jwt = jwt.encode(dados, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token_jwt


def verificar_access_token(token: str):
    carga = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
    return carga.get('sub')
