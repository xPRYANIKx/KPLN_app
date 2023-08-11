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
status_id = 'Черновик'

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


# Запись в payments_approval_history
# print('Запись в payment_full_agreed_status')
columns_p_s_t = ("payment_id", "payment_full_agreed_status")
payment_id = '26'
agreed_status = False
# print('agreed_status', type(agreed_status), agreed_status)
values_p_s_t = [[payment_id, agreed_status]]
query_p_s_t = get_db_dml_query(action='UPDATE', table='payments_summary_tab', columns=columns_p_s_t)
# execute_values(cursor, query_p_s_t, values_p_s_t)

values = ['payment_approval', 'amount', 2]
cursor.execute("""
DELETE FROM draft_payment WHERE page_name = %s AND parent_id::int = %s AND parameter_name = %s AND user_id = %s""",
               ['payment_approval', 26, 'amount', 2])
# cursor.execute("""
# SELECT
#     parent_id::int AS payment_id,
#     parameter_value::float AS amount
# FROM draft_payment
# WHERE page_name = 'payment_approval' AND parameter_name = 'amount' AND user_id = 2
# ORDER BY create_at DESC
# """)
# all_payments = cursor.fetchall()
# print(all_payments)
# print('approval_statuses', approval_statuses)


# conn.commit()
# conn.rollback()


conn.commit()
cursor.close()
conn.close()
