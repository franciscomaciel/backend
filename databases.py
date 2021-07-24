from sqlalchemy import create_engine
import cx_Oracle
import config

# self.oracle_dsn = "(DESCRIPTION=(CONNECT_TIMEOUT=3)(RETRY_COUNT=2)(FAILOVER=ON)(LOAD_BALANCE=NO) (ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=host_1)(PORT=1521))) (ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=host_2)(PORT=1521))) (CONNECT_DATA=(SERVICE_NAME=service_name)))"

dsn = cx_Oracle.makedsn(config.ORACLE_SERVER_IP, config.ORACLE_SERVER_PORT, sid=config.ORACLE_SID)
connection_string = config.SQLALCHEMY_DATABASE_URL

engine =  create_engine(
    connection_string,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True,
)

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
