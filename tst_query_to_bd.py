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

values = ['payment_approval', 'amount', 2]
cursor.execute("SELECT contractor_name FROM our_companies WHERE inflow_active is true"
               )
historical_data = cursor.fetchall()
print(historical_data)



# conn.commit()
# conn.rollback()


conn.commit()
cursor.close()
conn.close()
