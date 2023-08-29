import datetime
import itertools
import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_batch, execute_values
import time
from pprint import pprint

# PostgreSQL database configuration
db_name = "kpln_db"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

cursor = conn.cursor()

"""
    SUM(t0.approval_sum) OVER (PARTITION BY t0.payment_id)
    TRIM(to_char(COALESCE(t0.approval_sum - t7.approval_sum, t0.approval_sum), '9 999 999D99 ₽')) AS approval_sum,
    COALESCE(t8.amount, null) AS amount,
"""

user_id = 2
# Список статусов платежей Андрея
query = """
SELECT 
    payment_id, 
    approval_sum
FROM payments_approval 
WHERE payment_id::int in %s
"""
vars = [(7,), (34,)]
# cursor.execute(query, vars)
#
#
#
# zzz = cursor.fetchall()
# pprint(zzz)
vars = [[7, 34]]
execute_values(cursor, query, vars)
balance_sum = cursor.fetchall()
pprint(balance_sum)


cursor.close()
conn.close()
