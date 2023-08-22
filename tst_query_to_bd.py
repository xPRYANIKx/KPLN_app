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


def get_db_dml_query(action, table, columns, expr_set=None, subquery=";"):
    query = None
    if action == 'UPDATE':
        # В columns первым значением списка должна быть колонка для WHERE.
        # Связано с правилом выполнения sql-запроса

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
        query = f"{action} {table} {expr_cols} VALUES %s {subquery}"

    elif action == 'INSERT CONFLICT UPDATE':
        # В columns последним значением списка должна быть колонка для ON CONFLICT.
        # Связано с тем, что из value мы берем значения по порядку, все кроме ON CONFLICT колонки

        # Кортеж колонок переводим в строки и удаляем кавычки
        expr_cols = str(columns).replace('\'', '').replace('"', '')
        # Конструктор запроса
        query = f"INSERT INTO {table} AS t1 {expr_cols} VALUES %s ON CONFLICT ({columns[-1]}) DO UPDATE SET {expr_set};"

    elif action == 'DELETE':
        query = f"DELETE FROM {table} WHERE ({columns}) IN %s;"

    return query


## Удаляем из таблицы payment_draft данные о согласованной сумме пользователя
page_name = 'payment_approval'
parameter_name = 'amount'
user_id = 2
payment_id1 = 61
payment_id2 = 2
payment_id = (payment_id1, payment_id2)
columns = 'page_name, parent_id::int, parameter_name, user_id'

value_last_amount = [
    (page_name, payment_id1, parameter_name, user_id),
    (page_name, payment_id2, parameter_name, user_id)
]
value = []
for i in range(2):
    value.append((
        page_name,
        payment_id[i],
        parameter_name,
        user_id
    ))

query = f"""
    DELETE FROM payment_draft
    WHERE ({columns}) IN %s
    """

print(query)
print(value_last_amount)

# Удаление всех неотправленных сумм
execute_values(cursor, query, (value_last_amount,))

query = get_db_dml_query(action='DELETE', table='payment_draft', columns=columns)
print(query)
print(value)
print(value_last_amount)
execute_values(cursor, query, (value,))


conn.commit()
cursor.close()
conn.close()
