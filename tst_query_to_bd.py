import datetime

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

query_a_h = """
    INSERT INTO payments_approval_history (
        payment_id,
        status_id,
        user_id,
        approval_sum
    )
    VALUES (%s, %s, %s, %s)
    RETURNING payment_id, confirm_id;"""

# for i in range(2):
#     values_p_a_h.append(
#         (26, 2, 2, 2)
#     )
values_p_a_h = [
    (26, 2, 2, 2),
    (27, 2, 2, 3),
    (80, 2, 2, 4)
]
# Execute the SQL query
# cursor.executemany(query_a_h, values_p_a_h)
# execute_batch(cursor, query_a_h, values_p_a_h)
tmp = []
for i in range(len(values_p_a_h)):
    cursor.execute(query_a_h, [values_p_a_h[i][0], values_p_a_h[i][1], values_p_a_h[i][2], values_p_a_h[i][3]])
    results = cursor.fetchall()
    tmp.append(results)
conn.commit()
# Fetch the results
# results = cursor.fetchall()
pprint(tmp)

# # Fetch the results
# num_rows = cursor.rowcount
# print(f"Inserted {num_rows} rows.")


# pprint(values_p_a_h)

conn.commit()
cursor.close()
conn.close()
