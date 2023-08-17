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

conn = psycopg2.connect(dbname=db_name, user=db_user,  password=db_password, host=db_host, port=db_port)

cursor = conn.cursor()

# execute_values(cursor, query_p_s_t, values_p_s_t)

query = """INSERT INTO payments_balance AS t1 (balance_sum, company_id)
VALUES %s
ON CONFLICT (company_id) DO UPDATE SET
balance_sum = t1.balance_sum + EXCLUDED.balance_sum; """

def get_db_dml_query(action, table, columns, subquery=";"):
    query = None
    if action == 'INSERT CONFLICT UPDATE':
        # Кортеж колонок переводим в строки и удаляем кавычки
        expr_cols = str(columns).replace('\'', '').replace('"', '')
        # Список столбцов в SET
        expr_set = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns[:-1]])
        # Конструктор запроса
        query = f"INSERT INTO {table} {expr_cols} VALUES %s ON CONFLICT ({columns[-1]}) DO UPDATE SET {expr_set};"

    return query

columns = ('balance_sum', 'company_id')
query_p_s_t = get_db_dml_query(action='INSERT CONFLICT UPDATE', table='payments_balance', columns=columns)
print(query_p_s_t)


# values = [[30, 2], [20, 1], [1200, 3]]
# execute_values(cursor, query_p_s_t, values)
values = [[30, 2]]
execute_values(cursor, query, values)



# conn.commit()
# conn.rollback()


conn.commit()
cursor.close()
conn.close()
