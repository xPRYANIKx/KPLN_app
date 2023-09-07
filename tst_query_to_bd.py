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

payment_id = 1

cursor.execute(
            """WITH
                t0 AS (SELECT 
                    payment_id,
                    SUM(paid_sum) AS paid_sum
                          FROM payments_paid_history
                          GROUP BY payment_id)
            SELECT 
                    t1.payment_id,
                    date_trunc('second', timezone('UTC-3', t1.create_at)::timestamp) AS payment_at,
                    t2.payment_agreed_status_name, 
                    t0.paid_sum,
                    TRIM(to_char(t1.paid_sum, '9 999 999D99 ₽')) AS paid_sum_rub
            FROM payments_paid_history AS t1
            LEFT JOIN (
                    SELECT  
                        payment_agreed_status_id,
                        payment_agreed_status_name
                    FROM payment_agreed_statuses
            ) AS t2 ON t1.status_id = t2.payment_agreed_status_id
            LEFT JOIN t0 ON t1.payment_id = t0.payment_id
            
            WHERE t1.payment_id = %s
            ORDER BY t1.create_at;
            """,
            [payment_id]
        )
logs = cursor.fetchall()
pprint(logs)
print(len(logs))

cursor.close()
conn.close()

'''
WITH
     inv_2011 AS (SELECT country_code,
                         AVG(funding_total),
                         COUNT(id)
                  FROM company
                  WHERE EXTRACT(YEAR FROM CAST(founded_at AS date)) = 2011
                  GROUP BY country_code),
     inv_2012 AS (SELECT country_code,
                         AVG(funding_total),
                         COUNT(id)
                  FROM company
                  WHERE EXTRACT(YEAR FROM CAST(founded_at AS date)) = 2012
                  GROUP BY country_code),
     inv_2013 AS (SELECT country_code,
                         AVG(funding_total),
                         COUNT(id)
                  FROM company
                  WHERE EXTRACT(YEAR FROM CAST(founded_at AS date)) = 2013
                  GROUP BY country_code)
SELECT inv_2011.country_code,
       inv_2011.avg,
       inv_2012.avg,
       inv_2013.avg
FROM inv_2011 
INNER JOIN inv_2012 ON inv_2011.country_code = inv_2012.country_code
INNER JOIN inv_2013 ON inv_2011.country_code = inv_2013.country_code
ORDER BY inv_2011.avg DESC


'''