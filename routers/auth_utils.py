from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import sqlalchemy.orm as _orm
from services import get_db, get_usuario_by_login
from sqlalchemy.orm import Session
from providers import token_provider
from jose import JWTError

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

async def get_usuario_atual(token: str = Depends(oauth2_schema),
                            db: _orm.Session = Depends(get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        login = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception
    if not login:
        raise exception
    usuario = await get_usuario_by_login(login, db)
    if not usuario:
        raise exception
    return usuario