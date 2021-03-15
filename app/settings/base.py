import os


TESTING = False


DB_CONF = {
    'database': os.getenv('POSTGRES_DB', 'billing'),
    'host': os.getenv('POSTGRES_HOST', '127.0.0.1'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'minsize': 1,
    'maxsize': 20,
    'pool_recycle': 60,
    'reconnect_delay': 0.001,  # sec
    'reconnect_retries': 3,
}


DB_URL = f"postgresql://{DB_CONF['user']}:{DB_CONF['password']}@{DB_CONF['host']}:"\
         f"{DB_CONF['port']}/{DB_CONF['database']}"

TEST_DB_URL = f"postgresql://{DB_CONF['user']}:{DB_CONF['password']}@{DB_CONF['host']}:" \
              f"{DB_CONF['port']}/{DB_CONF['database']}_test"
