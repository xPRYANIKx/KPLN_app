import psycopg2
import psycopg2.extras
import time
import datetime
import itertools
from psycopg2.extras import execute_values
from pprint import pprint
from flask import Flask, g, request, render_template, redirect, flash, url_for, session, abort, get_flashed_messages, \
    jsonify
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
login_manager.login_message = "❗  Не достаточно прав для доступа"
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

                flash(message=['Договор сохранён', ''], category='success')
                return redirect(url_for(''))
                # return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
            except Exception as e:
                conn.rollback()
                # Close the database connection
                coon_cursor_close(cursor, conn)

                flash(message=['Договор НЕ сохранён', str(e)], category='error')
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
def set_new_payment():
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

                flash(message=['Платёж сохранён', f'№: {payment_number}'], category='success')
                session['submitted'] = True
                return redirect(url_for('new_payment'))
            except Exception as e:
                conn.rollback()
                # Close the database connection
                coon_cursor_close(cursor, conn)
                flash(message=['Платёж не сохранён', str(e)], category='error')
        return redirect(url_for('new_payment'))

    except Exception as e:
        return f'set_new_payment ❗❗❗ Ошибка \n---{e}'


@app.route('/payment_approval_3')
@login_required
def get_unapproved_payments_3():
    """Выгрузка из БД списка несогласованных платежей"""
    try:
        # Check if the user has access to the "List of contracts" page
        if current_user.get_role() != 1:
            return permission_error(403)
        else:
            user_id = current_user.get_id()
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
                        t8.amount,
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
                LEFT JOIN (
                        SELECT DISTINCT ON (payment_id) 
                            parent_id::int AS payment_id,
                            parameter_value::float AS amount
                        FROM draft_payment
                        WHERE page_name = %s AND parameter_name = %s AND user_id = %s
                        ORDER BY payment_id, create_at DESC
                ) AS t8 ON t1.payment_id = t8.payment_id
                WHERE not t1.payment_close_status
                ORDER BY t1.payment_number;
                """,
                ['payment_approval', 'amount', user_id]
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
def set_approved_payments_3():
    print(current_user.get_role())
    """Сохранение согласованные платежи на оплату в БД"""
    try:
        if request.method == 'POST':
            # Список выделенных столбцов
            selected_rows = request.form.getlist('selectedRows')  # Выбранные столбцы
            payment_number = request.form.getlist('payment_number')  # Номера платежей (передаётся id)
            status_id = request.form.getlist('status_id')  # Статус заявки (передаётся строковое название)
            payment_approval_sum = request.form.getlist('amount')  # Согласованная стоимость
            payment_full_agreed_status = request.form.getlist('payment_full_agreed_status')  # Сохранить до полной опл.

            print('-- selected_rows', selected_rows)
            print('-- payment_number', payment_number)
            print('-- status_id', status_id)
            print('-- payment_approval_sum', payment_approval_sum)
            print('-- payment_full_agreed_status', payment_full_agreed_status)

            values_p_s_t = []  # Данные для записи в таблицу payments_summary_tab
            values_p_a_h = []  # Данные для записи в таблицу payments_approval_history
            values_p_a = []  # Данные для записи в таблицу payments_approval_history

            values_a_h = []  # Список согласованных заявок для записи на БД
            pay_id_list_raw = []  # Список согласованных id заявок без обработки ошибок
            approval_id_list = []  # Список согласованных id заявок, без аннулир. и неправильные суммы согласования
            error_list = []  # Список id неправильно внесенных данных

            user_id = current_user.get_id()

            for i in range(len(selected_rows)):
                row = int(selected_rows[i]) - 1

                pay_id_list_raw.append(int(payment_number[row]))

                if not payment_approval_sum[row] and (status_id[row] == 'Черновик' or status_id[row] == 'Реком.'):
                    flash(message=['Не указана сумма согласования', ''], category='error')
                    return redirect(url_for('get_unapproved_payments_3'))

                if status_id[row] == 'К рассмотрению':
                    flash(message=['Функция не работает', ''], category='error')
                    return redirect(url_for('get_unapproved_payments_3'))

                values_a_h.append([
                    payment_number[row],
                    status_id[row],
                    user_id,
                    payment_approval_sum[row]
                    ])

            print('values_a_h  ', len(values_a_h), not values_a_h, [values_a_h])
            if not values_a_h:
                flash(message=['Ничего не выбрано', ''], category='error')
                return redirect(url_for('get_unapproved_payments_3'))

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
            print(total_approval_sum)

            # Добавляем недостающие данные и др. Подготавливаем данные для внесения в БД
            for i in range(len(total_approval_sum)):

                for j in range(len(pay_id_list_raw)):
                    payment_approval_sum[j] = payment_approval_sum[j] if payment_approval_sum[j] else 0
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
                        # Если статус Аннулировано (id 6), то закрываем заявку
                        if total_approval_sum[i]['status_id'] == 6:
                            total_approval_sum[i]['close_status'] = True  # Закрытие заявки

                # Проверка, что общая согласованная сумма меньше либо равна сумме к оплате
                if total_approval_sum[i]['total_approval'] > total_approval_sum[i]['payment_sum']:
                    error_list.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['payment_sum'],
                        total_approval_sum[i]['total_approval'],
                        total_approval_sum[i]['payment_approval_sum'],
                        'Общая сумма согласования больше остатка'

                    ])
                    total_approval_sum[i]['payment_id'] = None

            # Создаём списки с данными для записи в БД
            for i in range(len(total_approval_sum)):
                print(total_approval_sum[i]['payment_id'], '-', total_approval_sum[i]['status_id'])
                """для db payments_summary_tab"""
                if total_approval_sum[i]['payment_id']:
                    values_p_s_t.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['payment_full_agreed_status'],
                        total_approval_sum[i]['close_status']
                    ])

                """для db payments_approval_history"""
                if total_approval_sum[i]['payment_id'] and total_approval_sum[i]['status_id'] in [2, 3, 4, 5, 6]:
                    values_p_a_h.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['status_id'],
                        user_id,
                        total_approval_sum[i]['payment_approval_sum']
                    ])

                """для db payments_approva"""
                # Если есть id заявки и не Аннулировано (status_id 6)
                if total_approval_sum[i]['payment_id'] and total_approval_sum[i]['status_id'] != 6:
                    values_p_a.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['payment_approval_sum'],
                        ''
                    ])

            print('pst    ', values_p_s_t)
            print('pah    ', values_p_a_h)
            print('pa    ', values_p_a)
            print('ERRORS    ', error_list)
            for i in total_approval_sum:
                print(i)

            try:
                # Если есть что записывать в Базу данных
                if values_p_s_t:
                    # Перезапись в payments_summary_tab
                    columns_p_s_t = ("payment_id", "payment_full_agreed_status", "payment_close_status")
                    query_p_s_t = get_db_dml_query(action='UPDATE', table='payments_summary_tab', columns=columns_p_s_t)
                    execute_values(cursor, query_p_s_t, values_p_s_t)
                    conn.commit()

                    # Если есть что записывать в payments_approval_history
                    if values_p_a_h:
                        # Запись в payments_approval_history
                        action_p_a_h = 'INSERT INTO'
                        table_p_a_h = 'payments_approval_history'
                        columns_p_a_h = ('payment_id', 'status_id', 'user_id', 'approval_sum')
                        subquery = " RETURNING payment_id, confirm_id;"
                        query_a_h = get_db_dml_query(action_p_a_h, table_p_a_h, columns_p_a_h, subquery)
                        a_h_id = execute_values(cursor, query_a_h, values_p_a_h, fetch=True)
                        conn.commit()

                    # Если есть что записывать в payments_approval_history
                    if values_p_a:
                        # Запись в payments_approval
                        # добавляем id согласования
                        for i in values_p_a:
                            for j in a_h_id:
                                if i[0] == j[0]:
                                    i[2] = j[1]
                        action_p_a = 'INSERT INTO'
                        table_p_a = 'payments_approval'
                        columns_p_a = ('payment_id', 'approval_sum', 'confirm_id')
                        query_p_a = get_db_dml_query(action_p_a, table_p_a, columns_p_a)
                        execute_values(cursor, query_p_a, values_p_a)
                        conn.commit()

                    # Close the database connection

                    flash(message=['Заявки согласованы', ''], category='success')

                    # else:
                    #     # Close the database connection
                    #     coon_cursor_close(cursor, conn)
                    #     flash(message=['Заявки согласованы', ''], category='success')
                else:
                    flash(message=['Нет данных для сохранения', ''], category='error')
                # Если есть ошибки
                if error_list:
                    flash(message=[error_list, ''], category='error')

                coon_cursor_close(cursor, conn)

                return redirect(url_for('get_unapproved_payments_3'))
            except Exception as e:
                conn.rollback()
                coon_cursor_close(cursor, conn)
                return f'отправка set_approved_payments_3 ❗❗❗ Ошибка \n---{e}'

        return redirect(url_for('get_unapproved_payments_3'))
        # return get_unapproved_payments_3()

    except Exception as e:
        return f'set_approved_payments_3 ❗❗❗ Ошибка \n---{e}'


@app.route('/run_function', methods=['POST'])
def run_function():
    status_id = request.form.getlist('status_id')
    print('-'*10, '\n', '-'*10, '\n', '-'*10)
    print(status_id)
    return jsonify(updated_data='11111111')


@app.route('/save_quick_changes_approved_payments', methods=['POST'])
def save_quick_changes_approved_payments():
    # Сохраняем изменения в полях (согл сумма, статус, сохр до полн оплаты) заявки без нажатия кнопки "Отправить"
    try:
        payment_id = int(request.form['payment_number'])
        row_id = request.form['row_id']
        amount = request.form['amount']
        status_id = request.form['status_id']
        status_id2 = request.form.getlist('status_id')
        agreed_status = request.form['payment_full_agreed_status']
        # Преобразовываем в нужный тип данных
        if agreed_status == 'false':
            agreed_status = False
        else:
            agreed_status = True
        if amount:
            amount = float(amount)


        user_id = current_user.get_id()

        print('row_id -', row_id, '\n', 'payment_id -', payment_id, '\n', 'amount -', amount, '\n',
              'status_id -', status_id, '\n', 'agreed_status -', agreed_status)

        # Execute the SQL query
        conn, cursor = coon_cursor_init()

        # Статусы Андрея
        query_approval_statuses = """
            SELECT payment_agreed_status_id AS id
            FROM payment_agreed_statuses 
            WHERE payment_agreed_status_name = %s
        """
        cursor.execute(query_approval_statuses, (status_id,))
        approval_statuses = cursor.fetchone()[0]

        # СТАТУС ПЛАТЕЖА
        # Последний статус платежа
        query_last_status = """
            SELECT DISTINCT ON (payment_id) 
                     status_id
            FROM payments_approval_history
            WHERE payment_id = %s
            ORDER BY payment_id, create_at DESC
        """
        cursor.execute(query_last_status, (payment_id,))
        last_status_id = cursor.fetchone()[0]
        # Если статус New (id 1), приравниваем его к id 4 - Черновик
        if last_status_id == 1:
            last_status_id = 4
        # Если статусы не совпадают, создаём новую запись
        if last_status_id != approval_statuses:
            # Запись в payments_approval_history
            action_p_a_h = 'INSERT INTO'
            table_p_a_h = 'payments_approval_history'
            columns_p_a_h = ('payment_id', 'status_id', 'user_id')
            values_p_a_h = [[payment_id, approval_statuses, user_id]]
            query_a_h = get_db_dml_query(action_p_a_h, table_p_a_h, columns_p_a_h)
            execute_values(cursor, query_a_h, values_p_a_h)

        # СОХРАНИТЬ ДО ПОЛНОЙ ОПЛАТЫ
        # Последний статус сохранения до полной оплаты
        query_last_f_a_status = """
            SELECT payment_full_agreed_status
            FROM payments_summary_tab
            WHERE payment_id = %s
        """
        cursor.execute(query_last_f_a_status, (payment_id,))
        last_f_a_status = cursor.fetchone()[0]
        # Если статусы не совпадают, обновляем запись
        if last_f_a_status != agreed_status:
            columns_p_s_t = ("payment_id", "payment_full_agreed_status")
            values_p_s_t = [[payment_id, agreed_status]]
            query_p_s_t = get_db_dml_query(action='UPDATE', table='payments_summary_tab', columns=columns_p_s_t)
            execute_values(cursor, query_p_s_t, values_p_s_t)

        # СОГЛАСОВАННАЯ СУММА
        # Неотправленная согласованная сумма
        query_last_amount = """
        SELECT DISTINCT ON (payment_id) 
            parent_id::int AS payment_id,
            parameter_value::float AS amount
        FROM draft_payment
        WHERE page_name = %s AND parent_id::int = %s AND parameter_name = %s AND user_id = %s
        ORDER BY payment_id, create_at DESC;
        """
        page_name = 'payment_approval'
        parameter_name = 'amount'
        value_last_amount = [page_name, payment_id, parameter_name, user_id]
        cursor.execute(query_last_amount, value_last_amount)
        last_amount = cursor.fetchone()
        if last_amount:
            last_amount = last_amount[1]
        print('amount  ', type(amount), '   last_amount    ', type(last_amount), last_amount)
        print(amount == last_amount)
        # Если суммы не совпадают, добавляем запись
        if amount != last_amount:
            # Если неотправленна сумма была, то удаляем её и вносим новую (удаляем, а не перезаписываем т.к.
            # возможно в таблице может быть несколько записей)
            if last_amount:
                # Удаление всех неотправленных сумм
                cursor.execute("""
                DELETE FROM draft_payment 
                WHERE page_name = %s AND parent_id::int = %s AND parameter_name = %s AND user_id = %s
                """, value_last_amount)
            # Если указали сумму согласования, то вносим в таблицу временных значений, иначе не вносим
            if amount:
                action_d_p = 'INSERT INTO'
                table_d_p = 'draft_payment'
                columns_d_p = ('page_name', 'parent_id', 'parameter_name', 'parameter_value', 'user_id')
                values_d_p = [[page_name, payment_id, parameter_name, amount, user_id]]
                query_d_p = get_db_dml_query(action_d_p, table_d_p, columns_d_p)
                execute_values(cursor, query_d_p, values_d_p)












        # # Запись в payments_approval_history
        # action_p_a_h = 'INSERT INTO'
        # table_p_a_h = 'payments_approval_history'
        # columns_p_a_h = ('payment_id', 'status_id', 'user_id')
        # values_p_a_h = [[payment_id, status_id, user_id]]
        # query_a_h = get_db_dml_query(action_p_a_h, table_p_a_h, columns_p_a_h)
        # execute_values(cursor, query_a_h, values_p_a_h)
        # print(query_a_h)
        # cursor.execute(query_a_h, (payment_id, status_id, user_id))
        #
        # # Перезапись в payments_summary_tab
        # columns_p_s_t = ("payment_id", "payment_full_agreed_status")
        # values_p_s_t = [[payment_id, agreed_status]]
        # query_p_s_t = get_db_dml_query(action='UPDATE', table='payments_summary_tab', columns=columns_p_s_t)
        # execute_values(cursor, query_p_s_t, values_p_s_t)



        conn.commit()


        coon_cursor_close(cursor, conn)

        # """
        # UPDATE payments_approval_history
        # SET payment_id = %s, status_id = %s, user_id = %s
        #
        # SELECT DISTINCT ON (payment_id)
        #                         payment_id,
        #                         status_id
        #                     FROM payments_approval_history
        #                     ORDER BY payment_id, create_at DESC
        #
        # """
        # value = [payment_number, last_payment_id]
        # cursor.execute(query, value)
        # """Обновляем номер платежа в payments_summary_tab"""
        # # payment_number = f'PAY-{round(time.time())}-{last_payment_id}-{our_company}'
        # query = """
        #                     UPDATE payments_summary_tab
        #                     SET payment_number = %s
        #                     WHERE payment_id = %s;
        #                 """
        #
        #
        #
        #
        # # Update the data in the database using psycopg2

        return 'Data saved successfully'
    except Exception as e:
        return f'save_quick_changes_approved_payments ❗❗❗ Ошибка \n---{e}'

# Создание запроса в БД для множественного внесения данных
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


@app.route('/cash_inflow')
@login_required
def get_cash_inflow():
    """Страница для добавления платежа"""
    try:
        # Check if the user has access to the "List of contracts" page
        if current_user.get_role() != 1:
            return permission_error(403)
        else:
            return index()
    except Exception as e:
        return f'get_cash_inflow ❗❗❗ Ошибка \n---{e}'


@app.route('/cash_inflow', methods=['POST'])
@login_required
def set_cash_inflow():
    """Сохранение платежа"""
    try:
        # Check if the user has access to the "List of contracts" page
        if current_user.get_role() != 1:
            return permission_error(403)
        else:
            return index()
    except Exception as e:
        return f'get_cash_inflow ❗❗❗ Ошибка \n---{e}'


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
        # flash(message=['Вы вышли из аккаунта', ''], category='success')

        # Меню профиля
        hlnk_profile = {
            "name": ["Вы используете гостевой доступ", '(Войти)'], "url": "login"}

        # return redirect(url_for('login'))
        # return render_template('new_contr.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
        # return render_template('index.html', menu=hlnk_menu, menu_profile=hlnk_profile, title='Новый договор 📝')
        # return index()
        return redirect(request.referrer)
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
                # flash(message=['Вы вошли в систему', ''], category='success')
                return redirect(request.args.get("next") or url_for("profile"))

            flash(message=['❌ Логин или пароль указан неверно', ''], category='error')
            conn.close()
            print('ERROR')
            # return redirect(url_for('login'))
            return render_template(
                "login.html", title="Авторизация", menu=hlnk_menu, menu_profile=hlnk_profile,
                error_msg='❌ Логин или пароль указан неверно')

        # return redirect(url_for('login'))
        return render_template("login.html", title="Авторизация", menu=hlnk_menu, menu_profile=hlnk_profile)
    except Exception as e:
        return f'login ❗❗❗ Ошибка \n---{e}'


@app.route("/register", methods=["POST", "GET"])
@login_required
def register():
    try:
        if current_user.get_role() != 1:
            return permission_error(403)
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
                    flash(message=['register ❗❗❗ Ошибка', str(e)], category='error')
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


            # НОВЫЙ СПИСОК МЕНЮ - СПИСОК СЛОВАРЕЙ со словарями
            #     hlnk_menu = [
            #         {"menu_item": "Платежи", "sub_item":
            #             [{"name": "Добавить поступления", "url": "cash_inflow",
            #               "img": "https://cdn-icons-png.flaticon.com/512/617/617002.png"},
            #              {"name": "Новый платеж", "url": "new_payment",
            #               "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
            #              {"name": "Согласование платежей", "url": "payment_approval_3",
            #               "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"},
            #              {"name": "Оплата платежей", "url": "payment_pay",
            #               "img": "https://cdn-icons-png.flaticon.com/512/3673/3673443.png"},
            #              {"name": "Список платежей", "url": "payment_list",
            #               "img": "https://cdn-icons-png.flaticon.com/512/4631/4631071.png"}, ]
            #          },
            #         {"menu_item": "Admin", "sub_item":
            #             [{"name": "Регистрация пользователей", "url": "register",
            #               "img": "https://cdn-icons-png.flaticon.com/512/477/477801.png"}, ]
            #          },
            #     ]
            # else:
            #     print('user role else', current_user.get_role())
            #     hlnk_menu = [
            #         {"menu_item": "Платежи", "sub_item":
            #             [{"name": "Новый платеж", "url": "new_payment",
            #               "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
            #              {"name": "Список платежей", "url": "payment_list",
            #               "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"}, ]
            #          },
            #     ]
            #



                hlnk_menu = [
                    {"name": "Главная страница", "url": "/",
                     "img": "https://cdn-icons-png.flaticon.com/512/6489/6489329.png"},
                    {"name": "Добавить поступления", "url": "cash_inflow",
                     "img": "https://cdn-icons-png.flaticon.com/512/617/617002.png"},
                    {"name": "Новый платеж", "url": "new_payment",
                     "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                    {"name": "Согласование платежей", "url": "payment_approval_3",
                     "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"},
                    {"name": "Оплата платежей", "url": "payment_pay",
                     "img": "https://cdn-icons-png.flaticon.com/512/3673/3673443.png"},
                    {"name": "Список платежей", "url": "payment_list",
                     "img": "https://cdn-icons-png.flaticon.com/512/4631/4631071.png"},
                    {"name": "Регистрация пользователей", "url": "register",
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
