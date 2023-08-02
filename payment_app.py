import psycopg2
import psycopg2.extras
import time
import datetime
from pprint import pprint
from flask import Flask, g, request, render_template, redirect, flash, url_for, session, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from user_login import UserLogin
from forms import LoginForm, RegisterForm
from FDataBase import FDataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yyazaxkoaxb4w8vgj7a7p1lxfb7gee6n5hx'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "❗  Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

# PostgreSQL database configuration
db_name = "kpln_db"
# db_user = "kpln_user"
# db_password = "123"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"

dbase = None

# Меню страницы
hlnk_menu = None

# Меню профиля
hlnk_profile = None

# Как добавляется внешний ключ
insert_expression = '''INSERT
INTO
Table1(col1, col2, your_desired_value_from_select_clause, col3)
VALUES(
    'col1_value',
    'col2_value',
    (SELECT col_Table2 FROM Table2 WHERE IdTable2 = 'your_satisfied_value_for_col_Table2_selected'),
    'col3_value'
);'''


# Конект к БД
def coon_init():
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn
    except Exception as e:
        return f'coon_init ❗❗❗ Ошибка \n---{e}'

    # if not hasattr(g, 'link_db'):
    #     g.link_db = conn = psycopg2.connect(
    #         dbname=db_name,
    #         user=db_user,
    #         password=db_password,
    #         host=db_host,
    #         port=db_port
    #     )
    # return g.link_db


@login_manager.user_loader
def load_user(user_id):
    try:
        print("load_user")
        return UserLogin().from_db(user_id, dbase)
    except Exception as e:
        return f'load_user ❗❗❗ Ошибка \n---{e}'


@app.before_request
def before_request():
    try:
        """Установление соединения с БД перед выполнением запроса"""
        global dbase
        conn = coon_init()
        dbase = FDataBase(conn)
    except Exception as e:
        return f'before_request ❗❗❗ Ошибка \n---{e}'


def coon_cursor_init_dict():
    try:
        conn = coon_init()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cursor
    except Exception as e:
        return f'coon_cursor_init ❗❗❗ Ошибка \n---{e}'


def coon_cursor_init():
    try:
        conn = coon_init()
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        return f'coon_cursor_init ❗❗❗ Ошибка \n---{e}'


# Закрытие соединения
def coon_cursor_close(cursor, conn):
    try:
        cursor.close()
        conn.close()
    except Exception as e:
        return f'coon_cursor_close ❗❗❗ Ошибка \n---{e}'


@app.route('/', methods=["POST", "GET"])
def index():
    """Главная страница"""
    try:


        # Create profile name dict
        func_hlnk_profile()
        pprint('func_hlnk_profile')

        return render_template('index.html', menu=hlnk_menu,
                               menu_profile=hlnk_profile, title='Главная страница')
    except Exception as e:
        return f'❗❗❗ index \n---{e}'

# Новый договор
def new_contract():
    """Страница создания нового договора"""
    try:
        # Connect to the database
        conn, cursor = coon_cursor_init()

        # Список объектов из таблицы objects
        cursor.execute("SELECT object_name FROM objects")
        objects = cursor.fetchall()

        # Список типов договоров из таблицы contract_types
        cursor.execute("SELECT contract_type_name FROM contract_types")
        contract_types = cursor.fetchall()

        # Get the current date
        today = date.today().strftime("%Y-%m-%d")

        # Список наших компаний из таблицы contractors
        cursor.execute("SELECT contractor_name FROM our_companies")
        contractor_name = cursor.fetchall()

        # Список статусов договора из таблицы contract_statuses
        cursor.execute("SELECT contract_status_name FROM contract_statuses")
        contract_status_name = cursor.fetchall()

        # Список назначений договора из таблицы contract_purposes
        cursor.execute("SELECT contract_purpose_name FROM contract_purposes")
        contract_purpose_name = cursor.fetchall()

        # Список название НДС из таблицы vat
        cursor.execute("SELECT vat_name FROM vat")
        vat_name = cursor.fetchall()

        # Close the database connection
        coon_cursor_close(cursor, conn)

        # Create profile name dict
        func_hlnk_profile()

        return render_template('new_contr.html', objects=objects, contract_types=contract_types, today=today,
                               contractor_name=contractor_name, contract_status_name=contract_status_name,
                               contract_purpose_name=contract_purpose_name, vat_name=vat_name, menu=hlnk_menu,
                               menu_profile=hlnk_profile, title='Новый договор 📝')
    except Exception as e:
        return f'❗❗❗ new_contract \n---{e}'


# @app.route('/', methods=['POST'])
# @login_required
def new_contract_save_data():
    """Сохранение нового договора в БД"""
    try:
        if request.method == 'POST':
            # Get the form data from the request
            object_name = request.form.get('object')
            contract_type = request.form.get('contract_type')
            date_row = request.form.get('date')
            contract_number = request.form.get('contract_number')
            customer = request.form.get('customer')
            contractor = request.form.get('contractor')
            contract_comment = request.form.get('contract_comment')
            contract_status = request.form.get('contract_status')
            contract_purpose = request.form.get('contract_purpose')
            vat = request.form.get('vat')

            # Connect to the database
            conn, cursor = coon_cursor_init()

            # Prepare the SQL query to insert the data into the table
            query = """INSERT INTO new_objects (object_name, contract_type, date_row, contract_number, customer, contractor,
             contract_comment, contract_status, contract_purpose, vat, vat_value) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT vat_value FROM vat WHERE vat_name = %s))"""
            values = (object_name, contract_type, date_row, contract_number, customer, contractor, contract_comment,
                      contract_status, contract_purpose, vat, vat)

            try:
                # Execute the SQL query
                cursor.execute(query, values)
                conn.commit()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash('✔️ Договор сохранён', category='success')
                return redirect(url_for(''))
                # return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
            except Exception as e:
                conn.rollback()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash(f'❌ Договор НЕ сохранён \n---{e}', category='error')
                return redirect(url_for(''))
                # return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')

        return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
    except Exception as e:
        return f'new_contract_save_data ❗❗❗ Ошибка \n---{e}'


@app.route('/new_payment')
# @login_required
def new_payment():
    """Страница создания новой заявки на оплату"""
    try:
        # Connect to the database
        conn, cursor = coon_cursor_init()

        # Список ответственных
        cursor.execute(
            "SELECT user_id, last_name, first_name FROM users WHERE is_fired = FALSE")
        responsible = cursor.fetchall()

        # Список типов заявок
        cursor.execute(
            "SELECT cost_item_id, cost_item_name, cost_item_category FROM payment_cost_items")
        cost_items_list = cursor.fetchall()
        # передаём данные в виде словаря для создания сгруппированного выпадающего списка
        cost_items = {}
        for item in cost_items_list:
            key = item[2]
            value = [item[1], item[0]]
            if key in cost_items:
                cost_items[key].append(value)
            else:
                cost_items[key] = [value]

        # Список объектов
        cursor.execute("SELECT object_id, object_name FROM objects")
        objects_name = cursor.fetchall()

        # Список контрагентов
        cursor.execute("SELECT DISTINCT partner FROM payments_summary_tab")
        partners = cursor.fetchall()

        # Get the current date
        today = date.today().strftime("%Y-%m-%d")

        # Список наших компаний из таблицы contractors
        cursor.execute("SELECT contractor_name FROM our_companies")
        our_companies = cursor.fetchall()

        cursor.execute(
            "SELECT nextval(pg_get_serial_sequence('payments_summary_tab', 'payment_id'))")
        # "SELECT payment_id FROM payments_summary_tab ORDER BY payment_id DESC LIMIT 1")
        last_payment_id = cursor.fetchall()
        print(last_payment_id[0][0])

        # Close the database connection
        coon_cursor_close(cursor, conn)

        # Create profile name dict
        func_hlnk_profile()

        return render_template('new_payment.html', responsible=responsible, cost_items=cost_items,
                               objects_name=objects_name, partners=partners, today=today,
                               our_companies=our_companies, menu=hlnk_menu, menu_profile=hlnk_profile,
                               title='Новая заявка на оплату')
    except Exception as e:
        return f'❗❗❗ Ошибка \n---{e}'


@app.route('/new_payment', methods=['POST'])
# @login_required
def new_payment_save_data():
    """Сохранение новой заявки на оплату в БД"""
    try:
        if request.method == 'POST':
            # # Check if the form is resubmitted
            # if session.get('submitted'):
            #     flash('❗ Платёж был сохранен ранее. Повторная отправка отменена', category='success')
            #     # session['submitted'] = False
            #     return redirect(url_for('new_payment'))




            # Get the form data from the request
            basis_of_payment = request.form.get('basis_of_payment')
            responsible = request.form.get('responsible')
            cost_items = request.form.get('cost_items').split('-@@@-')[1]
            try:
                object_id = request.form.get('objects_name')
            except:
                object_id = None
            payment_description = request.form.get('payment_description')
            partner = request.form.get('partners')
            payment_due_date = request.form.get('payment_due_date')
            our_company = request.form.get('our_company')
            payment_sum = request.form.get('payment_sum')
            payment_sum = payment_sum.replace(' руб.', '').replace(" ", "").replace(",", ".")

            for key, value in request.form.items():
                print(f"Форма: {key}, Значение: {value}")

            # Connect to the database
            conn, cursor = coon_cursor_init()



            # return redirect(url_for('new_payment'))
            #
            # print(our_company)
            print(payment_sum)

            # Connect to the database
            conn, cursor = coon_cursor_init()

            cursor.execute(
                "SELECT nextval(pg_get_serial_sequence('payments_summary_tab', 'payment_id'))")
            # "SELECT payment_id FROM payments_summary_tab ORDER BY payment_id DESC LIMIT 1")
            last_payment_id = cursor.fetchall()

            # cursor.execute(
            #     "SELECT payment_id FROM payments_summary_tab ORDER BY payment_id DESC LIMIT 1")
            cursor.execute(
                "SELECT payment_id FROM payments_summary_tab ORDER BY payment_id DESC LIMIT 1")
            last_payment_id = cursor.fetchall()
            if not last_payment_id:
                last_payment_id = 1
            else:
                last_payment_id = last_payment_id[0][0] + 1

            payment_number = f'PAY-{round(time.time())}-{last_payment_id}-{our_company}'

            # Prepare the SQL query to insert the data into the payments_summary_tab
            query_s_t = """
            INSERT INTO payments_summary_tab (
                our_companies_id,
                cost_item_id,
                payment_number,
                basis_of_payment,
                payment_description,
                object_id,
                partner,
                payment_sum,
                payment_due_date,
                payment_owner,
                responsible
            )
            VALUES (
                (SELECT contractor_id FROM our_companies WHERE contractor_name = %s LIMIT 1),
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )"""
            values_s_t = (
                our_company,
                cost_items,
                payment_number,
                basis_of_payment,
                payment_description,
                object_id,
                partner,
                payment_sum,
                payment_due_date,
                current_user.get_id(),
                responsible)

            pprint(values_s_t)

            # Prepare the SQL query to insert the data into the payments_andrew_statuses
            query_a_s = """
            INSERT INTO payments_andrew_statuses (
                payment_id,
                status_id,
                user_id
            )
            VALUES (
                %s,
                %s,
                %s
            )"""

            status_id_a_s = 1  # id статуса "Черновик" из payments_andrew_statuses
            user_id_a_s = current_user.get_id() if current_user.get_id() else responsible
            values_a_s = (last_payment_id, status_id_a_s, user_id_a_s)

            try:
                """Запись в payments_summary_tab"""
                # Execute the SQL query
                cursor.execute(query_s_t, values_s_t)
                conn.commit()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                """Запись в payments_andrew_statuses"""
                # Execute the SQL query
                conn, cursor = coon_cursor_init()
                cursor.execute(query_a_s, values_a_s)
                conn.commit()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash(
                    f'✔️ Платёж сохранён. ID: {payment_number}', category='success')
                session['submitted'] = True
                return redirect(url_for('new_payment'))
            except Exception as e:
                conn.rollback()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash(f' Платёж НЕ сохранён \\n{str(e)}', category='error')
                return redirect(url_for('new_payment'))
        return redirect(url_for('new_payment'))

    except Exception as e:
        return f'new_payment_save_data ❗❗❗ Ошибка \n---{e}'


@app.route('/payment_approval_3')
@login_required
def get_unapproved_payments_3():
    print('current_user.get_role()', current_user.get_role())
    """Выгрузка из БД списка несогласованных платежей"""
    try:
        # Check if the user has access to the "List of contracts" page
        if current_user.get_role() != 1:
            abort(403)
        else:

            # Connect to the database
            conn, cursor = coon_cursor_init_dict()

            # Список платежей со статусом "new"
            cursor.execute(
                """SELECT 
                        t1.payment_id,
                        t3.contractor_name, 
                        t4.cost_item_name, 
                        t1.payment_number, 
                        t1.basis_of_payment, 
                        t5.first_name,
                        t5.last_name,
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
                INNER JOIN (
                        SELECT user_id,
                            first_name,
                            last_name
                        FROM users
                ) AS t5 ON t1.responsible = t5.user_id
                WHERE t1.payment_status = 'new'"""

            )
            all_payments = cursor.fetchall()

            # Изменяем формат даты с '%Y-%m-%d %H:%M:%S.%f%z' на '%Y-%m-%d %H:%M:%S'
            for row in all_payments:
                payment_at_date = row["payment_at"].strftime('%Y-%m-%d %H:%M:%S')
                row["payment_at"] = datetime.datetime.strptime(payment_at_date, '%Y-%m-%d %H:%M:%S')


            # cursor.execute("""SELECT *
            # FROM payments_summary_tab
            # WHERE payment_status = 'new'""")
            # all_payments = cursor.fetchall()

            # """Список столбцов и описаний таблицы payments_summary_tab.
            # Если вдруг будем делать конструктор таблицы для пользователя"""
            # cursor.execute(
            #     "SELECT column_name, "
            #     "col_description('public.payments_summary_tab'::regclass, ordinal_position) AS comment "
            #     "FROM information_schema.columns "
            #     "WHERE table_name = 'payments_summary_tab'")
            # col_description = cursor.fetchall()
            # pprint(col_description)

            # Список согласованных платежей
            cursor.execute("SELECT * FROM payments_approval")
            unapproved_payments = cursor.fetchall()

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id,
                          payment_agreed_status_name
                FROM payment_agreed_statuses WHERE payment_agreed_status_category = 'Andrew'""")
            approval_statuses = cursor.fetchall()

            # pprint(all_payments[0])
            # print(all_payments[0]["basis_of_payment"])
            # pprint(unapproved_payments)

            # Create profile name dict
            func_hlnk_profile()

            return render_template('payment_approval_3.html', menu=hlnk_menu, menu_profile=hlnk_profile,
                                   applications=all_payments, approval_statuses=approval_statuses,
                                   title='СОГЛАСОВАНИЕ ПЛАТЕЖЕЙ')
    except Exception as e:
        return f'get_unapproved_payments_3 ❗❗❗ Ошибка \n---{e}'


@app.route('/payment_approval_3', methods=['POST'])
@login_required
def approved_payments_save_data_3():
    print(current_user.get_role())
    """Сохранение согласованные платежи на оплату в БД"""
    try:
        if request.method == 'POST':
            # Список выделенных столбцов
            # list_approved_payments = list(map(int, request.form.getlist('selectedRows')))
            # print(list_approved_payments)

            tab_dict = request.form.to_dict(flat=False)
            # print(list(map(int, tab_dict['amount'])))
            pprint(tab_dict)
            print(tab_dict['amount'])

            # amount_list = []
            # for i in list_approved_payments:
            #     amount_list.append()

            # print("request.form.getlist('selectedRows')", request.form.getlist('selectedRows'))
            pprint(request.form.getlist('selectedRows'))
            print('\n', '\n', '\n')
            pprint(request.form.to_dict(flat=False))
            print('==' * 20)

            flash(f'✔️ Заявки согласованы', category='success')
            # time.sleep(10)
            # return flash(f'✔️ Заявки согласованы', category='success')
            return redirect(url_for('get_unapproved_payments_3'))
            # return get_unapproved_payments_3()

    except Exception as e:
        return f'approved_payments_save_data_3 ❗❗❗ Ошибка \n---{e}'


@app.route('/payment_pay')
@login_required
def get_unpaid_payments():
    print(current_user.get_role())
    """Выгрузка из БД списка несогласованных платежей"""
    try:
        # Check if the user has access to the "List of contracts" page
        if current_user.get_role() != 1:
            abort(403)
        else:

            # Connect to the database
            conn, cursor = coon_cursor_init_dict()

            # Список платежей со статусом "new"
            cursor.execute(
                """SELECT 
                        t1.payment_id,
                        t3.contractor_name, 
                        t4.cost_item_name, 
                        t1.payment_number, 
                        t1.basis_of_payment, 
                        t5.first_name,
                        t5.last_name,
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
                INNER JOIN (
                        SELECT user_id,
                            first_name,
                            last_name
                        FROM users
                ) AS t5 ON t1.responsible = t5.user_id
                WHERE t1.payment_status = 'new'"""

            )
            all_payments = cursor.fetchall()

            # Изменяем формат даты с '%Y-%m-%d %H:%M:%S.%f%z' на '%Y-%m-%d %H:%M:%S'
            for row in all_payments:
                payment_at_date = row["payment_at"].strftime('%Y-%m-%d %H:%M:%S')
                row["payment_at"] = datetime.datetime.strptime(payment_at_date, '%Y-%m-%d %H:%M:%S')


            # Список согласованных платежей
            cursor.execute("SELECT * FROM payments_approval")
            unapproved_payments = cursor.fetchall()

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id,
                          payment_agreed_status_name
                FROM payment_agreed_statuses WHERE payment_agreed_status_category = 'Andrew'""")
            approval_statuses = cursor.fetchall()


            # Create profile name dict
            func_hlnk_profile()

            return render_template('payment_pay.html', menu=hlnk_menu, menu_profile=hlnk_profile,
                                   applications=all_payments, approval_statuses=approval_statuses,
                                   title='ОПЛАТА ПЛАТЕЖЕЙ')
    except Exception as e:
        return f'get_unpaid_payments ❗❗❗ Ошибка \n---{e}'


@app.route('/payment_list')
@login_required
def get_payments_list():
    print(current_user.get_role())
    """Выгрузка из БД списка несогласованных платежей"""
    try:

        # Connect to the database
        conn, cursor = coon_cursor_init_dict()

        # Список платежей со статусом "new"
        cursor.execute(
            """SELECT 
                    t1.payment_id,
                    t3.contractor_name, 
                    t4.cost_item_name, 
                    t1.payment_number, 
                    t1.basis_of_payment, 
                    t5.first_name,
                    t5.last_name,
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
            INNER JOIN (
                    SELECT user_id,
                        first_name,
                        last_name
                    FROM users
            ) AS t5 ON t1.responsible = t5.user_id
            WHERE t1.payment_status = 'new'"""

        )
        all_payments = cursor.fetchall()

        # Изменяем формат даты с '%Y-%m-%d %H:%M:%S.%f%z' на '%Y-%m-%d %H:%M:%S'
        for row in all_payments:
            payment_at_date = row["payment_at"].strftime('%Y-%m-%d %H:%M:%S')
            row["payment_at"] = datetime.datetime.strptime(payment_at_date, '%Y-%m-%d %H:%M:%S')


        # Список согласованных платежей
        cursor.execute("SELECT * FROM payments_approval")
        unapproved_payments = cursor.fetchall()

        # Список статусов платежей Андрея
        cursor.execute(
            """SELECT payment_agreed_status_id,
                      payment_agreed_status_name
            FROM payment_agreed_statuses WHERE payment_agreed_status_category = 'Andrew'""")
        approval_statuses = cursor.fetchall()


        # Create profile name dict
        func_hlnk_profile()

        return render_template('payment_list.html', menu=hlnk_menu, menu_profile=hlnk_profile,
                               applications=all_payments, approval_statuses=approval_statuses,
                               title='СПИСОК ПЛАТЕЖЕЙ ПОЛЬЗОВАТЕЛЯ')
    except Exception as e:
        return f'get_payments_list ❗❗❗ Ошибка \n---{e}'


# Function to fetch data from the database
def get_contracts(filter_by=None, sort_by=None):
    """Выгрузка из БД списка договоров"""
    try:
        conn, cursor = coon_cursor_init()

        # Filter data if filter_by parameter is provided
        if filter_by is not None:
            query = f"SELECT * FROM new_objects WHERE contract_status = '{filter_by}'"
        else:
            query = "SELECT * FROM new_objects"

        # Sort data if sort_by parameter is provided
        if sort_by is not None:
            query += f" ORDER BY {sort_by}"

        cursor.execute(query)
        contracts = cursor.fetchall()

        # Close the database connection
        coon_cursor_close(cursor, conn)

        return contracts
    except Exception as e:
        return f'get_contracts ❗❗❗ Ошибка \n---{e}'


@app.route('/contracts_list')
@login_required
def contracts_list():
    try:
        contracts = get_contracts()

        # Connect to the database
        conn, cursor = coon_cursor_init()

        # Список название НДС из таблицы vat
        cursor.execute("""SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'new_objects'
        ORDER BY ordinal_position;""")
        sort_list = cursor.fetchall()

        # Create profile name dict
        func_hlnk_profile()

        return render_template('contracts_list.html', menu=hlnk_menu, menu_profile=hlnk_profile, contracts=contracts,
                               sort_list=sort_list,
                               title='Список договоров')
    except Exception as e:
        return f'index2 ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_fount(error):
    try:
        return render_template('page404.html', title="Страница не найдена"), 404
    except Exception as e:
        return f'page_not_fount ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 403
@app.errorhandler(403)
def permission_error(error):
    try:
        return render_template('page403.html', title="Ytn ljcnegf"), 404
    except Exception as e:
        return f'permission_error ❗❗❗ Ошибка \n---{e}'


@app.route('/logout')
@login_required
def logout():
    try:
        global hlnk_profile
        # if not current_user.is_authenticated:
        #     flash(f'❌ Перед выходом из сети необходимо войти в сеть', category='error')
        #     return redirect(url_for('login'))
        logout_user()
        func_hlnk_profile()
        flash(f'✔️ Вы вышли из аккаунта', category='success')

        # Меню профиля
        hlnk_profile = {
            "name": ["Вы используете гостевой доступ", '(Войти)'], "url": "login"}

        # return redirect(url_for('login'))
        # return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
        return render_template('index.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
        return index()
    except Exception as e:
        return f'logout ❗❗❗ Ошибка \n---{e}'


@app.route('/profile')
@login_required
def profile():
    try:
        name = current_user.get_name()

        # Create profile name dict
        func_hlnk_profile()


        return render_template("profile.html", title="Профиль", menu=hlnk_menu, menu_profile=hlnk_profile, name=name)
    except Exception as e:
        return f'profile ❗❗❗ Ошибка \n---{e}'


@app.route("/login", methods=["POST", "GET"])
def login():
    try:
        # Create profile name dict
        func_hlnk_profile()

        print('login', current_user.is_authenticated)
        if current_user.is_authenticated:
            return redirect(url_for('profile'))

        if request.method == 'POST':
            conn = coon_init()
            dbase = FDataBase(conn)
            form_data = request.form

            email = request.form.get('email')
            password = request.form.get('password')
            remain = request.form.get('remainme')

            user = dbase.get_user_by_email(email)

            if user and check_password_hash(user['password'], password):
                userlogin = UserLogin().create(user)
                login_user(userlogin, remember=remain)
                conn.close()
                flash('✔️ Вы вошли в систему', category='success')
                return redirect(request.args.get("next") or url_for("profile"))

            flash(f'❌ Логин или пароль указан неверно', category='error')
            conn.close()
            print('ERROR')
            # return redirect(url_for('login'))
            return render_template("login.html", title="Авторизация", menu=hlnk_menu, menu_profile=hlnk_profile)

        # return redirect(url_for('login'))
        return render_template("login.html", title="Авторизация", menu=hlnk_menu, menu_profile=hlnk_profile)
    except Exception as e:
        return f'login ❗❗❗ Ошибка \n---{e}'


@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    try:
        if current_user.get_role() != 1:
            abort(403)
        else:

            if request.method == 'POST':
                try:
                    conn = coon_init()
                    dbase = FDataBase(conn)
                    form_data = request.form
                    res = dbase.add_user(form_data)
                    if res:
                        # Close the database connection
                        conn.close()
                        return redirect(url_for('register'))
                    else:
                        conn.rollback()
                        conn.close()
                        return redirect(url_for('register'))

                except Exception as e:
                    flash(f'❗❗❗ Ошибка \n---{e}', category='error')
                    return redirect(url_for('register'))

            return render_template("register.html", title="Регистрация", menu=hlnk_menu, menu_profile=hlnk_profile)
    except Exception as e:
        return f'register ❗❗❗ Ошибка \n---{e}'


def func_hlnk_profile():
    try:
        global hlnk_profile, hlnk_menu

        if current_user.is_authenticated:
            # Меню профиля
            hlnk_profile = {
                "name": [current_user.get_profile_name(), '(Выйти)'], "url": "logout"},

            # Check user role.
            # Role: Admin
            if current_user.get_role() == 1:
                print('user role', current_user.get_role())
                hlnk_menu = [
                    {"name": "Главная страница", "url": "/",
                     "img": "https://cdn-icons-png.flaticon.com/512/6489/6489329.png"},
                    {"name": "Новый платеж", "url": "new_payment",
                     "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                    {"name": "Согласование платежей", "url": "payment_approval_3",
                     "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"},
                    {"name": "Оплата платежей", "url": "payment_pay",
                     "img": "https://cdn-icons-png.flaticon.com/512/3673/3673443.png"},
                    {"name": "Список платежей", "url": "payment_list",
                     "img": "https://cdn-icons-png.flaticon.com/512/4631/4631071.png"},
                    {"name": "Регистрация", "url": "register",
                     "img": "https://cdn-icons-png.flaticon.com/512/477/477801.png"},
                ]
            else:
                print('user role else', current_user.get_role())
                hlnk_menu = [
                    {"name": "Главная страница", "url": "/",
                     "img": "https://cdn-icons-png.flaticon.com/512/6489/6489329.png"},
                    {"name": "Новый платеж", "url": "new_payment",
                     "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                    {"name": "Список платежей", "url": "payment_list",
                     "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"},
                ]
        else:
            # Меню профиля
            hlnk_profile = {
                "name": ["Вы используете гостевой доступ", '(Войти)'], "url": "login"},
            hlnk_menu = [
                {"name": "Главная страница", "url": "/",
                 "img": "https://cdn-icons-png.flaticon.com/512/6489/6489329.png"},
                {"name": "Новый платеж", "url": "new_payment",
                 "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                # {"name": "Авторизация", "url": "login",
                #  "img": "https://cdn-icons-png.flaticon.com/512/2574/2574003.png"},
            ]

        return
    except Exception as e:
        return f'func_hlnk_profile ❗❗❗ Ошибка \n---{e}'


if __name__ == '__main__':
    app.run(debug=True)
