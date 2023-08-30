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

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

user_id = 2


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


cursor.execute(
    """SELECT 
                            DISTINCT t0.payment_id AS payment_id,
                            t1.payment_number,
                            t3.contractor_name,
                            t4.cost_item_name,
                            SUBSTRING(t1.basis_of_payment, 1,70) AS basis_of_payment_short,
                            t1.basis_of_payment,  
                            t5.first_name,
                            t5.last_name,
                            SUBSTRING(t1.payment_description, 1,135) AS payment_description_short,
                            t1.payment_description,  
                            COALESCE(t6.object_name, '') AS object_name,
                            t1.partner,
                            t1.payment_sum,
                            COALESCE(TRIM(to_char(t1.payment_sum, '999 999 999D99 ₽')), '') AS payment_sum_rub,
                            t0.approval_sum,
                            TRIM(to_char(t0.approval_sum, '9 999 999D99 ₽')) AS approval_sum_rub,
                            t1.payment_due_date,
                            date_trunc('second', timezone('UTC-3', t1.payment_at)::timestamp) AS payment_at,
                            t8.status_name
                        FROM payments_approval_history AS t0
                        LEFT JOIN (
                            SELECT 
                                payment_id, 
                                payment_number, 
                                basis_of_payment,
                                payment_description,
                                partner,
                                payment_sum,
                                payment_due_date,
                                payment_at,
                                our_companies_id,
                                cost_item_id,
                                responsible,
                                object_id
                            FROM payments_summary_tab
                        ) AS t1 ON t0.payment_id = t1.payment_id
                        LEFT JOIN (
                            SELECT contractor_id,
                                contractor_name
                            FROM our_companies            
                        ) AS t3 ON t1.our_companies_id = t3.contractor_id
                        LEFT JOIN (
                            SELECT cost_item_id,
                                cost_item_name
                            FROM payment_cost_items            
                        ) AS t4 ON t1.cost_item_id = t4.cost_item_id
                        LEFT JOIN (
                                SELECT user_id,
                                    first_name,
                                    last_name
                                FROM users
                        ) AS t5 ON t1.responsible = t5.user_id
                        LEFT JOIN (
                                SELECT object_id,
                                    object_name
                                FROM objects
                        ) AS t6 ON t1.object_id = t6.object_id
                        LEFT JOIN (
                                SELECT payment_agreed_status_id AS status_id,
                                    payment_agreed_status_name AS status_name
                                FROM payment_agreed_statuses
                        ) AS t8 ON t0.status_id = t8.status_id


                        ORDER BY t1.payment_due_date;
                        """
)
companies_balance = cursor.fetchall()
pprint(companies_balance)
print(len(companies_balance))

cursor.close()
conn.close()
