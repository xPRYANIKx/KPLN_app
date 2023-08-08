import psycopg2
import psycopg2.extras
import time
import datetime
from pprint import pprint
from flask import Flask, g, request, render_template, redirect, flash, url_for, session, abort, get_flashed_messages
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
        # Установление соединения с БД перед выполнением запроса
        global dbase
        conn = coon_init()
        dbase = FDataBase(conn)

        # Clear the flashed messages list
        get_flashed_messages()
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
            basis_of_payment = request.form.get('basis_of_payment')  # Наименование платежа
            responsible = request.form.get('responsible')  # Ответственный
            cost_items = request.form.get('cost_items').split('-@@@-')[1]  # Тип заявки
            try:
                object_id = request.form.get('objects_name')  # id объекта
            except:
                object_id = None
            payment_description = request.form.get('payment_description')  # Описание
            partner = request.form.get('partners')  # Контрагент
            payment_due_date = request.form.get('payment_due_date')  # Срок оплаты
            our_company = request.form.get('our_company')  # Компания
            payment_sum = request.form.get('payment_sum')  # Сумма оплаты
            # Превращаем строковое значение "payment_sum" с пропусками и руб. в число
            payment_sum = (payment_sum.replace(' руб.', '').
                           replace(" ", "").replace(",", "."))
            payment_number = f'PAY-{round(time.time())}-___-{our_company}'  # Номера платежа

            # Connect to the database
            conn, cursor = coon_cursor_init()

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
            )
            RETURNING payment_id;"""
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

            # Prepare the SQL query to insert the data into the payments_approval_history
            query_a_s = """
            INSERT INTO payments_approval_history (
                payment_id,
                status_id,
                user_id
            )
            VALUES (
                %s,
                %s,
                %s
            )"""

            try:
                """Запись в payments_summary_tab"""
                # Записываем новый платёж в БД и получаем обратно id записи для генерации номера платежа
                cursor.execute(query_s_t, values_s_t)
                last_payment_id = cursor.fetchone()[0]
                conn.commit()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                # Execute the SQL query
                conn, cursor = coon_cursor_init()
                """Обновляем номер платежа в payments_summary_tab"""
                payment_number = f'PAY-{round(time.time())}-{last_payment_id}-{our_company}'
                query = """
                    UPDATE payments_summary_tab
                    SET payment_number = %s
                    WHERE payment_id = %s;
                """
                value = [payment_number, last_payment_id]
                cursor.execute(query, value)

                """Запись в payments_approval_history"""
                status_id_a_s = 1  # id статуса "Черновик" из payments_approval_history
                user_id_a_s = current_user.get_id() if current_user.get_id() else responsible
                values_a_s = (last_payment_id, status_id_a_s, user_id_a_s)
                cursor.execute(query_a_s, values_a_s)
                conn.commit()

                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash(message=f'✔️ Платёж сохранён. ID: {payment_number}', category='success')
                session['submitted'] = True
                return redirect(url_for('new_payment'))
            except Exception as e:
                conn.rollback()
                # Close the database connection
                coon_cursor_close(cursor, conn)
                flash(message=['Платёж не сохранён', str(e)], category='error')
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
                        t6.object_name,
                        t1.partner,
                        t1.payment_sum,
                        t1.payment_sum - t7.approval_sum AS approval_sum,
                        '' AS amount,
                        t1.payment_due_date,
                        t2.status_id,
                        t1.payment_at,
                        t1.payment_full_agreed_status
                FROM payments_summary_tab AS t1
                LEFT JOIN (
                        SELECT DISTINCT ON (payment_id) 
                            payment_id,
                            status_id
                        FROM payments_approval_history
                        ORDER BY payment_id, create_at DESC
                ) AS t2 ON t1.payment_id = t2.payment_id
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
                ) AS t7 ON t1.payment_id = t7.payment_id
                WHERE not t1.payment_close_status
                ORDER BY t1.payment_number;
                """

            )
            all_payments = cursor.fetchall()

            # Обработка полученных данных
            for row in all_payments:
                # Изменяем объект None на пустоту
                if not row["object_name"]:
                    row["object_name"] = ''
                # Изменяем Остаток к оплате None на пустоту
                if not row["approval_sum"]:
                    row["approval_sum"] = row["payment_sum"]

                # Изменяем формат даты с '%Y-%m-%d %H:%M:%S.%f%z' на '%Y-%m-%d %H:%M:%S'
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

            # for key, value а: {key}, Значение: {value}")

            selected_rows = request.form.getlist('selectedRows')  # Выбранные столбцы
            payment_number = request.form.getlist('payment_number')  # Номера платежей (передаётся id)
            status_id = request.form.getlist('status_id')  # Статус заявки (передаётся строковое название)
            payment_approval_sum = request.form.getlist('amount')  # Согласованная стоимость
            payment_full_agreed_status = request.form.getlist('payment_full_agreed_status')  # Сохранить до полной опл.

            # Список изменений для таблицы payments_summary_tab
            pst_id_list = []  # Список id
            pst_change_full_agreed = []  # Статус "Сохранить до полной опл"
            pst_close_status = []  # Статус закрытия заявки

            # Список изменения для таблицы payments_approval_history
            pah_id_list = []  # Список id
            pah_status_id = []  # id статуса заявки
            pah_approval_sum = []  # Сумма согласования
            values_p_a_h = []  # Данные для записи в БД
            a_h_id = []  # Список id созданных записей

            # Список для внесения в таблицу payments_approval
            pa_id_list = []  # Список id
            pa_sum = []  # Список согласованных стоимость
            pa_confirm_id = []  # Список id записей из таблицы payments_approval_history
            values_p_a = []

            values_a_h = []  # Список согласованных заявок для записи на БД
            pay_id_list_raw = []  # Список согласованных id заявок без обработки ошибок
            approval_id_list = []  # Список согласованных id заявок, без аннулир. и неправильные суммы согласования
            error_list = []  # Список id неправильно внесенных данных

            print('##' * 35)
            print(selected_rows, payment_full_agreed_status)
            print('--' * 35)
            print(payment_number)
            print('**' * 35)
            print(status_id)
            print('_ ' * 35)
            print(payment_approval_sum)
            print('==' * 35)


            user_id = current_user.get_id()



            for i in range(len(selected_rows)):
                row = int(selected_rows[i]) - 1
                print(f"строка: {selected_rows[i]}")
                print(f"№ ПЛАТЕЖА: {payment_number[row]}, СОГЛАСОВАННАЯ СУММА *: {payment_approval_sum[row]}")

                # # Если заявку согласовали, добавляем id в список согласованных заявок
                # if status_id[row] == 'Реком.' or status_id[row] == 'Черновик':
                #     pay_id_list_raw.append(int(payment_number[row]))

                pay_id_list_raw.append(int(payment_number[row]))

                values_a_h.append([
                    payment_number[row],
                    status_id[row],
                    user_id,
                    payment_approval_sum[row]
                    ])

            print('%%' * 35)
            pprint(values_a_h)
            print('-*' * 35)
            conn, cursor = coon_cursor_init_dict()
            """
            Ищем сумму остатка согласования.
            - Если "согласованная сумма" равно остатку, то закрываем заявку, как полностью согласованную
            - Если не стоит галка "СОХРАНИТЬ ДО ПОЛНОЙ ОПЛАТЫ", полностью закрываем заявку со статусом "2"-
            Частичное согласование с закрытием
            """
            # Формируем обновленные данные для проверки:
            #  — id,
            #  — сумма оплаты,
            #  — ранее согласованное,
            #  — текущая сумма согл,
            #  — ранее согласованное + текущая сумма согл,
            #  — статус "Сохранить до полной опл",
            #  — статус закрытия,
            #  — статус Андрея
            query = """
                SELECT
                    t1.payment_id,
                    t1.payment_sum::float,
                    '' AS payment_approval_sum,
                    t2.approval_sum::float AS total_approval,
                    false AS payment_full_agreed_status,
                    false AS close_status,
                    'payment_agreed_statuses' AS status_id
                FROM payments_summary_tab AS t1
                LEFT JOIN (
                    SELECT 
                        payment_id, 
                        sum (approval_sum) AS approval_sum
                    FROM payments_approval_history
                    GROUP BY payment_id
                ) AS t2 ON t1.payment_id = t2.payment_id
                WHERE t1.payment_id in %s;    
                """

            cursor.execute(query, (tuple(pay_id_list_raw),))
            total_approval_sum = cursor.fetchall()

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id AS id, 
                          payment_agreed_status_name  AS name
                FROM payment_agreed_statuses 
                WHERE payment_agreed_status_category = 'Andrew'
                """
            )
            approval_statuses = cursor.fetchall()
            print('TYPE', type(total_approval_sum))

            print(total_approval_sum)
            print('_-=' * 35)
            print("total_approval_sum[0]['payment_id']", type(total_approval_sum[0]['payment_id']), total_approval_sum[0]['payment_id'])
            print("total_approval_sum[0]['payment_id']", total_approval_sum[0]['payment_id'])
            print('pay_id_list_raw', len(pay_id_list_raw), '_-=-_', pay_id_list_raw)
            print('payment_full_agreed_status', payment_full_agreed_status)

            # Добавляем недостающие данные и пл. Подготавливаем данные для внесения в БД
            for i in range(len(total_approval_sum)):

                for j in range(len(pay_id_list_raw)):
                    if total_approval_sum[i]['payment_id'] == pay_id_list_raw[j]:
                        # Сумма согласования
                        total_approval_sum[i]['payment_approval_sum'] = (
                            float(0 if payment_approval_sum[j] is None else payment_approval_sum[j]))

                        # ранее согласованное + текущая сумма согл
                        tot_app = float(0 if total_approval_sum[i]['total_approval'] is None
                                        else total_approval_sum[i]['total_approval'])
                        total_approval_sum[i]['total_approval'] = (
                                tot_app + total_approval_sum[i]['payment_approval_sum'])

                        # Статус "Сохранить до полной опл". Если галка стоит, то проставляем 1
                        for fas in payment_full_agreed_status:
                            if int(fas)-1 == j:
                                total_approval_sum[i]['payment_full_agreed_status'] = True
                                break

                        # Статус Андрея. Значения без учета сумм согласования
                        total_approval_sum[i]['status_id'] = status_id[j]

                        # Статус закрытия и статус Андрея
                        if total_approval_sum[i]['payment_full_agreed_status']:  # Если total_approval = payment_sum
                            if total_approval_sum[i]['payment_sum'] == total_approval_sum[i]['total_approval']:
                                total_approval_sum[i]['status_id'] = 3  # Полное согласование
                                total_approval_sum[i]['close_status'] = True  # Закрытие заявки
                        else:
                            total_approval_sum[i]['close_status'] = True  # Закрытие заявки

                            if total_approval_sum[i]['payment_sum'] != total_approval_sum[i]['total_approval']:
                                if total_approval_sum[i]['payment_sum'] == total_approval_sum[i]['total_approval']:
                                    total_approval_sum[i]['status_id'] = 3  # Полное согласование
                                else:
                                    total_approval_sum[i]['status_id'] = 2  # Частичное согласование с закрытием

                # Переводим значение статуса Андрея из name в id
                for j2 in range(len(approval_statuses)):
                    if total_approval_sum[i]['status_id'] == approval_statuses[j2]['name']:
                        total_approval_sum[i]['status_id'] = approval_statuses[j2]['id']

                # Проверка, что общая согласованная сумма меньше либо равна сумме к оплате
                if total_approval_sum[i]['total_approval'] > total_approval_sum[i]['payment_sum']:
                    error_list.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['payment_sum'],
                        total_approval_sum[i]['total_approval']
                    ])
                    total_approval_sum[i]['payment_id'] = None




            print('total_approval_sum\n', total_approval_sum)
            print('-\\' * 35)

            # Создаём списки с данными для записи в БД
            for i in range(len(total_approval_sum)):
                print(total_approval_sum[i]['payment_id'], '-', total_approval_sum[i]['status_id'])
                """для db payments_summary_tab"""
                if total_approval_sum[i]['payment_id']:
                    # Список id
                    pst_id_list.append(total_approval_sum[i]['payment_id'])
                    # Статус "Сохранить до полной опл"
                    pst_change_full_agreed.append(total_approval_sum[i]['payment_full_agreed_status'])
                    # Статус закрытия заявки
                    pst_close_status.append(total_approval_sum[i]['close_status'])

                """для db payments_approval_history"""
                if total_approval_sum[i]['payment_id'] and total_approval_sum[i]['status_id'] in [2, 3, 4, 5]:
                    values_p_a_h.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['status_id'],
                        user_id,
                        total_approval_sum[i]['payment_approval_sum']
                    ])
                    # # Список id
                    # pah_id_list.append(total_approval_sum[i]['payment_id'])
                    # # Статус Андрея
                    # pah_status_id.append(total_approval_sum[i]['status_id'])
                    # # Согласованная сумма
                    # pah_approval_sum.append(total_approval_sum[i]['payment_approval_sum'])

                """для db payments_approva"""
                if total_approval_sum[i]['payment_id']:
                    # Список id
                    pa_id_list.append(total_approval_sum[i]['payment_id'])
                    # Согласованная сумма
                    pa_sum.append(total_approval_sum[i]['status_id'])

            pprint([[pst_id_list], [pst_change_full_agreed], [pst_close_status]])
            pprint([[pah_id_list], [pah_status_id], [pah_approval_sum]])
            pprint([[pa_id_list], [pa_sum]])


            # Перезапись в payments_summary_tab
            query_s_t = """
                UPDATE payments_summary_tab
                SET payment_full_agreed_status = %s, payment_close_status = %s
                WHERE payment_id = %s;
            """
            for i in range(len(pst_id_list)):
                cursor.execute(query_s_t, [pst_change_full_agreed[i], pst_close_status[i], pst_id_list[i]])
            conn.commit()

            # Запись в payments_approval_history
            query_a_h = """
                INSERT INTO payments_approval_history (
                    payment_id,
                    status_id,
                    user_id,
                    approval_sum
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING payment_id, confirm_id;"""
            for i in range(len(values_p_a_h)):
                cursor.execute(query_a_h,
                               [values_p_a_h[i][0], values_p_a_h[i][1], values_p_a_h[i][2], values_p_a_h[i][3]])
                results = cursor.fetchall()
                tmp.append(results)
            conn.commit()
            cursor.execute(query_a_h, values_p_a_h)
            a_h_id = cursor.fetchall()
            conn.commit()







            query_a_h = """
                INSERT INTO payments_approval_history (
                  payment_id,
                  status_id,
                  user_id,
                  approval_sum 
                )
                VALUES (
                  %s,
                  %s,
                  %s,
                  %s
                )"""


            cursor.execute(query_a_h, values_a_h)
            conn.commit()

            query2 = """
              INSERT INTO payments_approval (
                  payment_id,
                  status_id,
                  user_id
              )
              VALUES (
                  %s,
                  %s,
                  %s
              )"""


            # Close the database connection
            coon_cursor_close(cursor, conn)



            query = """
            SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
            FROM   pg_index i
            JOIN   pg_attribute a ON a.attrelid = i.indrelid
                                 AND a.attnum = ANY(i.indkey)
            WHERE  i.indrelid = 'payments_approval_history'::regclass
            AND    i.indisprimary;
            """

            # Список согласованных платежей
            # conn, cursor = coon_cursor_init()
            # cursor.execute(query)
            # request_tmp = cursor.fetchall()
            # print('------------request_tmp', request_tmp)

            # Конструктор Номера платежа (payment_number). ИЗ БД берем id последнего платежа
            # cursor.execute(
            #     "SELECT nextval(pg_get_serial_sequence('payments_approval_history', 'confirm_id'))")
            # last_confirm_id = cursor.fetchall()
            # cursor.execute(
            #     "SELECT currval(pg_get_serial_sequence('payments_approval_history', 'confirm_id'))")
            # last_confirm_id = cursor.fetchall()
            # if not last_confirm_id:
            #     last_confirm_id = 1
            # # else:
            # #     last_confirm_id = last_confirm_id[0][0] + 1
            coon_cursor_close(cursor, conn)
            # print('last_confirm_id', last_confirm_id)



            # # Connect to the database
            # conn, cursor = coon_cursor_init()
            #
            # # Конструктор Номера платежа (payment_number). ИЗ БД берем id последнего платежа
            # cursor.execute(
            #     "SELECT nextval(pg_get_serial_sequence('payments_summary_tab', 'payment_id'))")
            # last_payment_id = cursor.fetchall()
            # if not last_payment_id:
            #     last_payment_id = 1
            # else:
            #     last_payment_id = last_payment_id[0][0] + 1
            # payment_number = f'PAY-{round(time.time())}-{last_payment_id}-{our_company}'



            # values_s_t = (
            #     our_company,
            #     cost_items,
            #     payment_number,
            #     basis_of_payment,
            #     payment_description,
            #     object_id,
            #     partner,
            #     payment_sum,
            #     payment_due_date,
            #     current_user.get_id(),
            #     responsible)

            # # Prepare the SQL query to insert the data into the payments_approval_history
            # query_a_s = """
            #   INSERT INTO payments_approval_history (
            #       payment_id,
            #       status_id,
            #       user_id
            #   )
            #   VALUES (
            #       %s,
            #       %s,
            #       %s
            #   )"""
            #
            # status_id_a_s = 1  # id статуса "Черновик" из payments_approval_history
            # user_id_a_s = current_user.get_id() if current_user.get_id() else responsible
            # values_a_s = (last_payment_id, status_id_a_s, user_id_a_s)
            #
            # try:
            #     """Запись в payments_summary_tab"""
            #     # Execute the SQL query
            #     cursor.execute(query_s_t, values_s_t)
            #     conn.commit()
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
            return permission_error(403)
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
                        FROM payments_approval_history
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
                    FROM payments_approval_history
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
        return render_template('page403.html', title="Нет доступа"), 403
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
