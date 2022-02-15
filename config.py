class Config:

    # Constantes:
    HTTP_STATUS_OK = 200

    # Conexão com o Oracle:
    ORACLE_USERNAME = 'IMPAR_PERRELLI'
    ORACLE_PASSWORD = 'IMPAR_2022'
    ORACLE_SERVER_IP = '10.10.10.211'
    ORACLE_SERVER_PORT = '1521'
    ORACLE_SID = 'TESTE'
    # ORACLE_SCHEMA = 'CTL'

    # Configurações de segurança:
    HASH_ALGORITHM = 'bcrypt'
    SECRET_KEY = 'caa9c8f8620cbb30679026bb6427e11f'     # TODO: Substituir por variável de ambiente
    ALGORITHM = 'HS256'
    EXPIRES_IN_MIN = 60*24*7                            # Token é válido por uma semana

    """
        Para gerar uma nova SECRET_KEY, no console do Python:
        Nota: O parâmetro da função urandom() corresponde à quantidade de caracteres que o valor randômico produzido terá;
              na sequência, é aplicada a função hexlify() ao resultado, convertendo-o para hexadecimal, dobrando assim, o
              tamanho da chave gerada.
        >>> import os
    >>> import binascii
    >>> binascii.hexlify(os.urandom(24))
    b'deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f'
    """


config = Config()
