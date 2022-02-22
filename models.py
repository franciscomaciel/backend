import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import database as _database
from sqlalchemy import Table
from database import Base, engine

"""
Usuario = Table('WCONNECTOR_CREDENCIAL',
    Base.metadata,
    autoload=True,
    autoload_with=engine,
    schema='CTL')
"""
class Usuario(_database.Base):
    __tablename__ = 'WCONNECTOR_CREDENCIAL'
    # __table_args__ = { "schema": "CTL" }
    login_ad = _sql.Column(_sql.String, primary_key=True, index=True)
    hash_senha = _sql.Column(_sql.String, primary_key=False, index=False)
    flag_admin = _sql.Column(_sql.String, primary_key=False, index=False)
    temp_passwd = _sql.Column(_sql.String, primary_key=False, index=False)
    def verificar_senha(self, password: str):
        return _hash.bcrypt.verify(password, self.hash_senha)
