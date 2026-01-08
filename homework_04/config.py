from os import getenv

sqla_max_overflow = 0
sqla_pool_size = 50

db_echo = False
if getenv("DB_ECHO") == "1":
    db_echo = True
