from sqlalchemy import create_engine
import cx_Oracle
import config

dsn = cx_Oracle.makedsn(config.ORACLE_SERVER_IP, config.ORACLE_SERVER_PORT, sid=config.ORACLE_SID)

connection_str = 'oracle://{user}:{password}@{sid}'.format(
    user=config.ORACLE_USERNAME,
    password=config.ORACLE_PASSWORD,
    sid=dsn
)

engine = create_engine(
    connection_str,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)
