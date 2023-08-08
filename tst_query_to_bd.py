import datetime
import itertools
import psycopg2
import psycopg2.extras
from psycopg2.extras import execute_batch
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


def get_db_query(table, columns, values, subquery=";"):
    # Добавляем кортежи (%s, %s...), (%s, %s...)...
    val_list = ','.join(['(' + ('%s,'*len(value))[:-1] + ')' for value in values])
    # Кортеж колонок переводим в строки и удаляем кавычки
    columns = str(columns).replace('\'', '').replace('"', '')
    # Конструктор запроса
    query = f"INSERT INTO {table} {columns} VALUES " + val_list + subquery
    # Переводим двумерный список данных в одномерный
    values = list(itertools.chain(*values))
    return query, values


query_a_h1 = """
    INSERT INTO payments_approval_history (
        payment_id,
        status_id,
        user_id,
        approval_sum
    )
    VALUES """
values_p_a_h = [
    (26, 2, 2, 2),
    (27, 2, 2, 3),
    (80, 2, 2, 4)
]
columns = ('payment_id', 'status_id', 'user_id', 'approval_sum')
table = 'payments_approval_history'
subquery = " RETURNING payment_id, confirm_id;"
xxx = get_db_query(table, columns, values_p_a_h)

pprint(xxx)
cursor.execute(xxx[0], xxx[1])
result3 = ','.join(['(' + ('%s,'*len(item))[:-1] + ')' for item in values_p_a_h])
query_a_h1 += result3 + " RETURNING payment_id, confirm_id;"




values_p_a_h = [
    (26, 2, 2, 2),
    (27, 2, 2, 3),
    (80, 2, 2, 4)
]


# cursor.execute(query_a_h1, list(itertools.chain(*values_p_a_h)))

# query_a_h = f"""
#     INSERT INTO payments_approval_history (
#         payment_id,
#         status_id,
#         user_id,
#         approval_sum
#     )
#     VALUES ({','.join('%s' for col in columns)})
#     RETURNING payment_id, confirm_id;"""
#
# query_string = f"INSERT INTO `{}` {} VALUES ({})".format(table, columns, placeholders)

columns = (
        'payment_id',
        'status_id',
        'user_id',
        'approval_su'
)
placeholders = ','.join('%s' for col in columns)
query_string = "INSERT INTO payments_approval_history {} VALUES ({})".format(columns, placeholders)
# cursor.execute(query_string, values_p_a_h)




# print(x)
# cursor.execute(query_a_h)
# results = cursor.fetchall()
# print(query_a_h)
# print('\n')
# print(values_p_a_h)
# print('\n')
# print(results)
# conn.commit()
# cursor.execute(x)
# results = cursor.fetchall()
# print(results)
conn.rollback()

# Execute the SQL query
# cursor.executemany(query_a_h, values_p_a_h)
# execute_batch(cursor, query_a_h, values_p_a_h)
# tmp = []
# for i in range(len(values_p_a_h)):
#     cursor.execute(query_a_h, [values_p_a_h[i][0], values_p_a_h[i][1], values_p_a_h[i][2], values_p_a_h[i][3]])
#     results = cursor.fetchall()
#     tmp.append(results)
# conn.commit()
# # Fetch the results
# # results = cursor.fetchall()
# print(tmp)
# for i in tmp:
#     print(i, type(i), '    ', i[0], type(i[0]), '    ', i[0][0], type(i[0][0]))

# # Fetch the results
# num_rows = cursor.rowcount
# print(f"Inserted {num_rows} rows.")


# pprint(values_p_a_h)

conn.commit()
cursor.close()
conn.close()
