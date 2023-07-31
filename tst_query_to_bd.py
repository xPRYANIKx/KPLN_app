import psycopg2
import psycopg2.extras
import time
from pprint import pprint


# PostgreSQL database configuration
db_name = "kpln_db"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"

conn = psycopg2.connect( dbname=db_name, user=db_user,  password=db_password, host=db_host, port=db_port)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""SELECT pst.payment_id, 
                         pst.our_companies_id,
                         ag.payment_agreed_status_name
                  FROM payments_summary_tab AS pst
                  INNER JOIN payments_andrew_statuses AS ans ON pst.payment_id = ans.payment_id
                  INNER JOIN payment_agreed_statuses AS ag ON ans.status_id = ag.payment_agreed_status_id;
                  """)
response = cursor.fetchall()
pprint(response)

cursor.execute("""SELECT DISTINCT ON (payment_id) 
                        payment_id,
                        status_id
                  FROM payments_andrew_statuses
                  ORDER BY payment_id, create_at DESC;
                  """)
response = cursor.fetchall()
pprint(response)

cursor.execute("""SELECT pst.payment_id, 
                         ag.payment_agreed_status_name
                  FROM payments_summary_tab AS pst
                  INNER JOIN (
                      SELECT DISTINCT ON (payment_id) 
                            payment_id,
                            status_id
                      FROM payments_andrew_statuses
                      ORDER BY payment_id, create_at DESC
                  ) AS ans ON pst.payment_id = ans.payment_id
                  INNER JOIN payment_agreed_statuses AS ag ON ans.status_id = ag.payment_agreed_status_id;
                  """)
response = cursor.fetchall()
pprint(response)

cursor.execute(
    """SELECT 
            t1.payment_id,
            t3.contractor_name, 
            t4.cost_item_name, 
            t1.payment_number, 
            t1.basis_of_payment, 
            t1.responsible,
            t1.payment_description, 
            t1.object_id,
            t1.partner,
            t1.payment_sum,
            '',
            '',
            t1.payment_due_date,
            t2.status_id,
            t1.payment_at,
            t1.payment_full_agreed_status
    FROM payments_summary_tab AS t1
    INNER JOIN (
            SELECT DISTINCT ON (payment_id) 
                payment_id,
                status_id
            FROM payments_andrew_statuses
            ORDER BY payment_id, create_at DESC
    ) AS t2 ON t1.payment_id = t2.payment_id
    INNER JOIN (
        SELECT contractor_id,
            contractor_name
        FROM our_companies            
    ) AS t3 ON t1.our_companies_id = t3.contractor_id
    INNER JOIN (
        SELECT cost_item_id,
            cost_item_name
        FROM payment_cost_items            
    ) AS t4 ON t1.cost_item_id = t4.cost_item_id
    WHERE t1.payment_status = 'new'"""

)
response = cursor.fetchall()
pprint(response)
print(len(response))
# pprint(response)



cursor.execute("""
                    SELECT DISTINCT ON (payment_id) 
                payment_id,
                status_id
            FROM payments_andrew_statuses
            ORDER BY payment_id, create_at DESC
                    """
               )
response = cursor.fetchall()
pprint(response)



# """Список столбцов и описаний таблицы payments_summary_tab.
# Если вдруг будем делать конструктор таблицы для пользователя"""
# cursor.execute(
#     "SELECT column_name, "
#     "col_description('public.payments_summary_tab'::regclass, ordinal_position) AS comment "
#     "FROM information_schema.columns "
#     "WHERE table_name = 'payments_summary_tab'")
# col_description = cursor.fetchall()
# pprint(col_description)

cursor.close()
conn.close()