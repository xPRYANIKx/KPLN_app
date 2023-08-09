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
# cursor = conn.cursor()
# values_p_a_h = []


def get_db_dml_query(action, table, columns, subquery=";"):
    query = None
    if action == 'UPDATE':
        # Список столбцов в SET
        expr_set = ', '.join([f"{col} = c.{col}" for col in columns[1:]])

        # Список столбцов для таблицы "с"
        expr_s_tab = str(columns).replace('\'', '').replace('"', '')

        # Выражение для WHERE
        expr_where = result = f"c.{columns[0]} = t.{columns[0]}"

        # Конструктор запроса
        query = f"{action} {table} AS t SET {expr_set} FROM (VALUES %s) AS c {expr_s_tab} WHERE {expr_where} {subquery}"

    elif action == 'INSERT INTO':
        # Кортеж колонок переводим в строки и удаляем кавычки
        expr_cols = str(columns).replace('\'', '').replace('"', '')

        # Конструктор запроса
        query = f"{action} {table} {expr_cols} VALUES  %s {subquery}"

    return query

values_s_t = [
    (80, 10, 300), (87, 2, 500)
]
values_s_t = [
    (80, 6), (87, 6)
]

columns = ("payment_id", "user_id", "approval_sum")
columns = ("payment_id", "user_id")
query_s_t2 = get_db_dml_query('UPDATE', 'payments_approval_history', columns)
print(query_s_t2)

# execute_values(cursor, query_s_t2, values_s_t)


conn.commit()
conn.rollback()



cursor.close()
conn.close()
