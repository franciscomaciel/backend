import cx_Oracle
import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from config.general_config import Config

dsn = cx_Oracle.makedsn(Config.ORACLE_SERVER_IP, Config.ORACLE_SERVER_PORT, sid=Config.ORACLE_SID)

connection_str = 'oracle://{user}:{password}@{sid}'.format(
    user=Config.ORACLE_USERNAME,
    password=Config.ORACLE_PASSWORD,
    sid=dsn
)

engine = _sql.create_engine(
    connection_str,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = _declarative.declarative_base()
