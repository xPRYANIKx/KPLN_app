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
    SELECT 
        DISTINCT (payment_id) AS payment_id,
        SUM(approval_sum) OVER (PARTITION BY payment_id) AS approval_sum,
        MAX(approval_at) OVER (PARTITION BY payment_id) AS approval_at,
    FROM payments_approval AS t1
"""

user_id = 2
# Список статусов платежей Андрея
cursor.execute(
    """
SELECT 
    DISTINCT (t0.payment_id) AS payment_id,
    SUM(t0.approval_sum) OVER (PARTITION BY t0.payment_id) AS approval_sum,
    MAX(t0.approval_at) OVER (PARTITION BY t0.payment_id) AS approval_at,t1.payment_number, 
    t1.payment_id,
    t3.contractor_name, 
    t4.cost_item_name, 
    t1.payment_number, 
    t1.basis_of_payment, 
    t5.first_name,
    t5.last_name,
    t1.payment_description, 
    COALESCE(t6.object_name, '') AS object_name,
    t1.partner,
    t1.payment_sum,
    COALESCE(t1.payment_sum - t7.approval_sum, t1.payment_sum) AS approval_sum,
    COALESCE(t8.amount, null) AS amount,
    t1.payment_due_date,
    t2.status_id,
    date_trunc('second', timezone('UTC-3', t1.payment_at)::timestamp) AS payment_at,
    t1.payment_full_agreed_status
FROM payments_approval AS t0
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
        payment_full_agreed_status,
        our_companies_id,
        cost_item_id,
        responsible,
        object_id,
        payment_close_status
    FROM payments_summary_tab
) AS t1 ON t0.payment_id = t1.payment_id

LEFT JOIN (
        SELECT DISTINCT ON (payment_id) 
            payment_id,
            status_id
        FROM payments_approval_history
        ORDER BY payment_id, create_at DESC
) AS t2 ON t0.payment_id = t2.payment_id
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
        SELECT payment_id,
            sum (approval_sum) AS approval_sum
        FROM payments_approval_history
        GROUP BY payment_id
) AS t7 ON t0.payment_id = t7.payment_id
LEFT JOIN (
        SELECT DISTINCT ON (payment_id) 
            parent_id::int AS payment_id,
            parameter_value::float AS amount
        FROM payment_draft
        WHERE page_name = %s AND parameter_name = %s AND user_id = %s
        ORDER BY payment_id, create_at DESC
) AS t8 ON t0.payment_id = t8.payment_id
WHERE not t1.payment_close_status
ORDER BY t1.payment_number;
""",
['payment-pay', 'amount', user_id]
)

zzz = cursor.fetchall()
pprint(zzz)


cursor.close()
conn.close()
