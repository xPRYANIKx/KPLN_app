import psycopg2
import psycopg2.extras
import time
import datetime
import itertools
from psycopg2.extras import execute_values
from pprint import pprint
from flask import g, request, render_template, redirect, flash, url_for, session, abort, get_flashed_messages, \
    jsonify, Blueprint
from datetime import date
from FDataBase import FDataBase
from flask_login import login_required
import error_handlers
import login_app

from wtforms import Form, BooleanField, StringField, DecimalField, IntegerField, DateField, validators

payment_app_bp = Blueprint('payment_app', __name__)

# PostgreSQL database configuration
db_name = "kpln_db"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"

dbase = None

# Меню страницы
hlink_menu = None

# Меню профиля
hlink_profile = None


@payment_app_bp.before_request
def before_request():
    login_app.before_request()


# class NewPayment(Form):
#     basis_of_payment = StringField(label='basis_of_payment', validators=[validators.Length(min=1)])
#     responsible = IntegerField(label='responsible')
#     cost_items = StringField(label='cost_items', validators=[validators.Length(min=7)])
#     payment_description = StringField('payment_description')
#     payment_due_date = DateField(label='payment_due_date', format='%YYYY-%mm-%dd')


@payment_app_bp.route('/new-payment')
# @login_required
def get_new_payment():
    """Страница создания новой заявки на оплату"""
    try:
        global hlink_menu, hlink_profile

        # Connect to the database
        conn, cursor = login_app.conn_cursor_init()

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
        cursor.execute("SELECT contractor_id, contractor_name FROM our_companies")
        our_companies = cursor.fetchall()

        # Close the database connection
        login_app.conn_cursor_close(cursor, conn)

        # Create profile name dict
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        not_save_val = session['n_s_v_new_payment'] if session.get('n_s_v_new_payment') else {}

        return render_template('new-payment.html', responsible=responsible, cost_items=cost_items,
                               objects_name=objects_name, partners=partners, today=today,
                               our_companies=our_companies, menu=hlink_menu, menu_profile=hlink_profile,
                               not_save_val=not_save_val, title='Новая заявка на оплату')
    except Exception as e:
        return f'payment ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/new-payment', methods=['POST'])
# @login_required
def set_new_payment():
    """Сохранение новой заявки на оплату в БД"""
    try:
        if request.method == 'POST':
            for key, val in request.form.items():
                print('   ', key, val)

            # Get the form data from the request
            basis_of_payment = request.form.get('basis_of_payment')  # Наименование платежа
            responsible = request.form.get('responsible').split('-@@@-')[0]  # Ответственный
            cost_items = request.form.get('cost_items').split('-@@@-')[1]  # Тип заявки
            try:
                object_id = request.form.get('objects_name').split('-@@@-')[0]  # id объекта
                object_name = request.form.get('objects_name').split('-@@@-')[-1]  # Название объекта
            except:
                object_id = None
                object_name = None
            payment_description = request.form.get('payment_description')  # Описание
            partner = request.form.get('partners')  # Контрагент
            payment_due_date = request.form.get('payment_due_date')  # Срок оплаты
            our_company_id = request.form.get('our_company').split('-@@@-')[0]  # id компании
            our_company = request.form.get('our_company').split('-@@@-')[1]  # Название компания
            payment_sum = request.form.get('payment_sum')  # Сумма оплаты
            payment_sum = convert_amount(payment_sum)
            payment_number = f'PAY-{round(time.time())}-___-{our_company}'  # Номера платежа

            # Connect to the database
            conn, cursor = login_app.conn_cursor_init()

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
                %s,
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
                our_company_id,
                cost_items,
                payment_number,
                basis_of_payment,
                payment_description,
                object_id,
                partner,
                payment_sum,
                payment_due_date,
                login_app.current_user.get_id(),
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
                login_app.conn_cursor_close(cursor, conn)

                # Execute the SQL query
                conn, cursor = login_app.conn_cursor_init()
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
                user_id_a_s = login_app.current_user.get_id() if login_app.current_user.get_id() else responsible
                values_a_s = (last_payment_id, status_id_a_s, user_id_a_s)
                cursor.execute(query_a_s, values_a_s)
                conn.commit()

                # Close the database connection
                login_app.conn_cursor_close(cursor, conn)

                flash(message=['Платёж сохранён', f'№: {payment_number}'], category='success')
                session.pop('n_s_v_new_payment', default=None)

                return redirect(url_for('.get_new_payment'))
            except Exception as e:
                conn.rollback()
                # Close the database connection
                login_app.conn_cursor_close(cursor, conn)
                session['n_s_v_new_payment'] = {
                    'b_o_p': basis_of_payment,
                    'resp': [
                        responsible,
                        request.form.get('responsible').split('-@@@-')[-1]
                    ],
                    'c_i': [
                        request.form.get('cost_items').split('-@@@-')[0],
                        cost_items,
                        request.form.get('cost_items').split('-@@@-')[-1]
                    ],
                    'p_d': payment_description,
                    'part': partner,
                    'p_d_d': payment_due_date,
                    'o_c': [our_company_id, our_company],
                    'p_s': request.form.get('payment_sum')
                }
                if object_id:
                    session['n_s_v_new_payment']['obj_n'] = [object_id, object_name]

                flash(message=['Платёж не сохранён', str(e)], category='error')
                return redirect(url_for('.get_new_payment'))
        return redirect(url_for('.get_new_payment'))

    except Exception as e:
        return f'set_new_payment ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/payment-approval')
@login_required
def get_unapproved_payments():
    """Выгрузка из БД списка несогласованных платежей"""
    try:
        global hlink_menu, hlink_profile

        # Check if the user has access to the "List of contracts" page
        if login_app.current_user.get_role() != 1:
            return error_handlers.handle403(403)
        else:
            user_id = login_app.current_user.get_id()
            # Connect to the database
            conn, cursor = login_app.conn_cursor_init_dict()

            # Список платежей со статусом "new"
            cursor.execute(
                """SELECT 
                        t1.payment_id,
                        t3.contractor_name, 
                        t3.contractor_id, 
                        t4.cost_item_name, 
                        t1.payment_number,  
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
                        COALESCE(t1.payment_sum - t2.approval_sum, t1.payment_sum) AS approval_sum,
                        TRIM(to_char(COALESCE(t1.payment_sum - t2.approval_sum, t1.payment_sum), '9 999 999D99 ₽')) AS approval_sum_rub,
                        COALESCE(t8.amount, null) AS amount,
                        COALESCE(TRIM(to_char(t8.amount, '999 999 999D99 ₽')), '') AS amount_rub,
                        t1.payment_due_date,
                        t2.status_id,
                        date_trunc('second', timezone('UTC-3', t1.payment_at)::timestamp) AS payment_at,
                        t1.payment_full_agreed_status
                FROM payments_summary_tab AS t1
                LEFT JOIN (
                        SELECT DISTINCT ON (payment_id) 
                            payment_id,
                            status_id,
                            SUM(approval_sum) OVER (PARTITION BY payment_id) AS approval_sum
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
                        SELECT DISTINCT ON (payment_id) 
                            parent_id::int AS payment_id,
                            parameter_value::float AS amount
                        FROM payment_draft
                        WHERE page_name = %s AND parameter_name = %s AND user_id = %s
                        ORDER BY payment_id, create_at DESC
                ) AS t8 ON t1.payment_id = t8.payment_id
                WHERE not t1.payment_close_status
                ORDER BY t1.payment_due_date;
                """,
                ['payment-approval', 'amount', user_id]
            )
            all_payments = cursor.fetchall()

            # Список согласованных платежей
            cursor.execute("SELECT * FROM payments_approval")
            unapproved_payments = cursor.fetchall()

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id,
                          payment_agreed_status_name
                FROM payment_agreed_statuses WHERE payment_agreed_status_category = 'Andrew'""")
            approval_statuses = cursor.fetchall()

            # ДС на счету
            cursor.execute(
                """SELECT
                    sum(balance_sum) AS account_money
                FROM payments_balance
                """
            )
            account_money = cursor.fetchone()
            account_money = account_money[0] if account_money[0] else 0

            # Сумма ранее согласованных платежей
            cursor.execute(
                """SELECT
                    sum(approval_sum) AS approval_sum
                FROM payments_approval
                """
            )
            available_money = cursor.fetchone()
            available_money = account_money - available_money[0] if available_money[0] else account_money

            login_app.conn_cursor_close(cursor, conn)

            # Create profile name dict
            hlink_menu, hlink_profile = login_app.func_hlink_profile()

            return render_template(
                'payment-approval.html', menu=hlink_menu, menu_profile=hlink_profile,
                applications=all_payments, approval_statuses=approval_statuses, account_money=account_money,
                available_money=available_money, page=request.path[1:], title='Согласование платежей')
    except Exception as e:
        pprint(e)
        return f'get_unapproved_payments ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/payment-approval', methods=['POST'])
@login_required
def set_approved_payments():
    """Сохранение согласованные платежи на оплату в БД"""
    try:
        if request.method == 'POST':
            # Список выделенных столбцов
            selected_rows = request.form.getlist('selectedRows')  # Выбранные столбцы
            payment_number = request.form.getlist('payment_number')  # Номера платежей (передаётся id)
            status_id = request.form.getlist('status_id')  # Статус заявки (передаётся строковое название)
            payment_approval_sum = request.form.getlist('amount')  # Согласованная стоимость
            payment_full_agreed_status = request.form.getlist('payment_full_agreed_status')  # Сохранить до полной опл.

            print(payment_approval_sum)

            selected_rows = [int(i) for i in selected_rows]
            payment_number = [int(i) for i in payment_number]
            payment_approval_sum = [convert_amount(i) for i in payment_approval_sum]
            payment_full_agreed_status = [int(i) for i in payment_full_agreed_status]

            values_p_s_t = []  # Данные для записи в таблицу payments_summary_tab
            values_p_a_h = []  # Данные для записи в таблицу payments_approval_history
            values_p_a = []  # Данные для записи в таблицу payments_approval_history

            # Данные для удаления временных данных из таблицы payments_summary_tab
            values_p_d = []
            page_name = 'payment-approval'
            parameter_name = 'amount'

            values_a_h = []  # Список согласованных заявок для записи на БД
            pay_id_list_raw = []  # Список согласованных id заявок без обработки ошибок
            approval_id_list = []  # Список согласованных id заявок, без аннулир. и неправильные суммы согласования
            error_list = []  # Список id неправильно внесенных данных

            user_id = login_app.current_user.get_id()

            for i in selected_rows:
                row = i - 1

                pay_id_list_raw.append(payment_number[row])

                if not payment_approval_sum[row] and (status_id[row] == 'Черновик' or status_id[row] == 'Реком.'):
                    flash(message=['Не указана сумма согласования', ''], category='error')
                    return redirect(url_for('.get_unapproved_payments'))

                if status_id[row] == 'К рассмотрению':
                    flash(message=['Функция не работает', ''], category='error')

                    pprint(get_flashed_messages())
                    return redirect(url_for('.get_unapproved_payments'))

                values_a_h.append([
                    payment_number[row],
                    status_id[row],
                    user_id,
                    payment_approval_sum[row]
                ])

            if not values_a_h:
                flash(message=['Ничего не выбрано', ''], category='error')
                return redirect(url_for('.get_unapproved_payments'))

            conn, cursor = login_app.conn_cursor_init_dict()
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
            pprint(total_approval_sum)

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id AS id, 
                          payment_agreed_status_name  AS name
                FROM payment_agreed_statuses 
                WHERE payment_agreed_status_category = 'Andrew'
                """
            )
            approval_statuses = cursor.fetchall()

            # Добавляем недостающие данные и др. Подготавливаем данные для внесения в БД
            for i in range(len(total_approval_sum)):
                # Список id выбранных платежей
                for pay_id in pay_id_list_raw:
                    # Номер элемента в списках из формы
                    jj = payment_number.index(pay_id)
                    payment_approval_sum[jj] = payment_approval_sum[jj] if payment_approval_sum[jj] else 0

                    if total_approval_sum[i]['payment_id'] == pay_id:
                        # Сумма согласования
                        total_approval_sum[i]['payment_approval_sum'] = (
                            float(0 if payment_approval_sum[jj] is None else payment_approval_sum[jj]))

                        # ранее согласованное + текущая сумма согл
                        tot_app = float(0 if total_approval_sum[i]['total_approval'] is None
                                        else total_approval_sum[i]['total_approval'])
                        total_approval_sum[i]['total_approval'] = (
                                tot_app + total_approval_sum[i]['payment_approval_sum'])

                        # Статус "Сохранить до полной опл". Если галка стоит, то проставляем 1
                        for fas in payment_full_agreed_status:
                            if payment_number[fas-1] == total_approval_sum[i]['payment_id']:
                                total_approval_sum[i]['payment_full_agreed_status'] = True
                                break

                        print("total_approval_sum[i]['status_id'] ", total_approval_sum[i]['status_id'], '  ', status_id[jj])
                        # Статус Андрея. Значения без учета сумм согласования
                        total_approval_sum[i]['status_id'] = status_id[jj]

                        # Статус закрытия и статус Андрея
                        if total_approval_sum[i]['status_id'] == 'Аннулирован':
                            total_approval_sum[i]['status_id'] = 6  # Полное согласование
                            total_approval_sum[i]['close_status'] = True  # Закрытие заявки
                        elif total_approval_sum[i]['payment_full_agreed_status']:  # Если total_approval = payment_sum
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

            pprint(total_approval_sum)

            # Создаём списки с данными для записи в БД
            for i in range(len(total_approval_sum)):
                """для db payments_summary_tab"""
                if total_approval_sum[i]['payment_id']:
                    values_p_s_t.append([
                        total_approval_sum[i]['payment_id'],
                        total_approval_sum[i]['payment_full_agreed_status'],
                        total_approval_sum[i]['close_status']
                    ])
                    values_p_d.append((
                        page_name,
                        total_approval_sum[i]['payment_id'],
                        parameter_name,
                        user_id
                    ))

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

                    print('  -----------', total_approval_sum[i])

                    values_p_a.append([
                        total_approval_sum[i]['payment_approval_sum'],
                        total_approval_sum[i]['payment_id']
                    ])

            try:
                # Если есть что записывать в Базу данных
                if values_p_s_t:
                    # Перезапись в payments_summary_tab
                    columns_p_s_t = ("payment_id", "payment_full_agreed_status", "payment_close_status")
                    query_p_s_t = get_db_dml_query(action='UPDATE', table='payments_summary_tab', columns=columns_p_s_t)
                    execute_values(cursor, query_p_s_t, values_p_s_t)

                    columns_p_d = 'page_name, parent_id::int, parameter_name, user_id'
                    query_p_d = get_db_dml_query(action='DELETE', table='payment_draft', columns=columns_p_d)
                    execute_values(cursor, query_p_d, (values_p_d,))

                    conn.commit()

                    # Если есть что записывать в payments_approval_history
                    if values_p_a_h:
                        # Запись в payments_approval_history
                        action_p_a_h = 'INSERT INTO'
                        table_p_a_h = 'payments_approval_history'
                        columns_p_a_h = ('payment_id', 'status_id', 'user_id', 'approval_sum')
                        subquery = " RETURNING payment_id, confirm_id;"
                        query_a_h = get_db_dml_query(
                            action=action_p_a_h, table=table_p_a_h, columns=columns_p_a_h, subquery=subquery
                        )
                        a_h_id = execute_values(cursor, query_a_h, values_p_a_h, fetch=True)
                        conn.commit()

                    # Если есть что записывать в payments_approval_history
                    if values_p_a:
                        # # Запись в payments_approval
                        action_p_a = 'INSERT CONFLICT UPDATE'
                        table_p_a = 'payments_approval'
                        columns_p_a = ('approval_sum', 'payment_id')

                        expr_set = ', '.join([f"{col} = t1.{col} + EXCLUDED.{col}" for col in columns_p_a[:-1]])
                        query_p_a = get_db_dml_query(
                            action=action_p_a, table=table_p_a, columns=columns_p_a, expr_set=expr_set
                        )

                        execute_values(cursor, query_p_a, values_p_a)

                        conn.commit()

                    flash(message=['Заявки согласованы', ''], category='success')

                else:
                    flash(message=['Нет данных для сохранения', ''], category='error')
                # Если есть ошибки
                if error_list:
                    flash(message=[error_list, ''], category='error')

                login_app.conn_cursor_close(cursor, conn)

                return redirect(url_for('.get_unapproved_payments'))
            except Exception as e:
                conn.rollback()
                login_app.conn_cursor_close(cursor, conn)
                return f'отправка set_approved_payments ❗❗❗ Ошибка \n---{e}'

        return redirect(url_for('.get_unapproved_payments'))
        # return get_unapproved_payments()

    except Exception as e:
        return f'set_approved_payments ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/save_quick_changes_approved_payments', methods=['POST'])
def save_quick_changes_approved_payments():
    try:
        # print('save_quick_changes_approved_payments')
        # Сохраняем изменения в полях (согл сумма, статус, сохр до полн оплаты) заявки без нажатия кнопки "Отправить"
        # try:
        page = request.form['page']
        payment_id = int(request.form['payment_number'])
        row_id = request.form['row_id']
        amount = convert_amount(request.form['amount'])
        if page == 'payment-approval':
            status_id = request.form['status_id']
            status_id2 = request.form.getlist('status_id')
        else:
            status_id = None
            status_id2 = None
        agreed_status = request.form['payment_full_agreed_status']
        # for key, val in request.form.items():
        #     print('  - ', key, val)
        # Преобразовываем в нужный тип данных
        if agreed_status == 'false':
            agreed_status = False
        else:
            agreed_status = True
        if amount:
            amount = float(amount)

        # print(f"""payment_id {payment_id}
        # row_id {row_id}
        # amount {amount}
        # status_id {status_id}
        # status_id2 {status_id2}
        # agreed_status {agreed_status}
        # """)

        user_id = login_app.current_user.get_id()

        # Execute the SQL query
        conn, cursor = login_app.conn_cursor_init()

        if page == 'payment-approval':
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
            try:
                last_status_id = cursor.fetchone()[0]
            except:
                last_status_id = ''
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
                query_a_h = get_db_dml_query(action=action_p_a_h, table=table_p_a_h, columns=columns_p_a_h)
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

        if page == 'payment-pay':
            # ЗАКРЫТЬ ТОЛЬКО ПОСЛЕ ПОЛНОЙ ОПЛАТЫ
            columns_p_a = ("payment_id", "approval_fullpay_close_status")
            values_p_a = [[payment_id, agreed_status]]
            query_p_a = get_db_dml_query(action='UPDATE', table='payments_approval', columns=columns_p_a)
            execute_values(cursor, query_p_a, values_p_a)


        # СОГЛАСОВАННАЯ СУММА
        # Неотправленная согласованная сумма
        query_last_amount = """
        SELECT DISTINCT ON (payment_id) 
            parent_id::int AS payment_id,
            parameter_value::float AS amount
        FROM payment_draft
        WHERE page_name = %s AND parent_id::int = %s AND parameter_name = %s AND user_id = %s
        ORDER BY payment_id, create_at DESC;
        """
        parameter_name = 'amount'
        value_last_amount = [page, payment_id, parameter_name, user_id]
        cursor.execute(query_last_amount, value_last_amount)
        last_amount = cursor.fetchone()
        if last_amount:
            last_amount = last_amount[1]
        # Если суммы не совпадают, добавляем запись
        if amount != last_amount:
            # Если неотправленна сумма была, то удаляем её и вносим новую (удаляем, а не перезаписываем т.к.
            # возможно в таблице может быть несколько записей)
            if last_amount:
                # Удаление всех неотправленных сумм
                cursor.execute("""
                DELETE FROM payment_draft 
                WHERE page_name = %s AND parent_id::int = %s AND parameter_name = %s AND user_id = %s
                """, value_last_amount)
            # Если указали сумму согласования, то вносим в таблицу временных значений, иначе не вносим
            if amount:
                action_d_p = 'INSERT INTO'
                table_d_p = 'payment_draft'
                columns_d_p = ('page_name', 'parent_id', 'parameter_name', 'parameter_value', 'user_id')
                values_d_p = [[page, payment_id, parameter_name, amount, user_id]]
                query_d_p = get_db_dml_query(action=action_d_p, table=table_d_p, columns=columns_d_p)
                execute_values(cursor, query_d_p, values_d_p)

        conn.commit()

        login_app.conn_cursor_close(cursor, conn)

        return 'Data saved successfully'
    except Exception as e:
        return f'save_quick_changes_approved_payments ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/cash-inflow')
@login_required
def get_cash_inflow():
    """Страница для добавления платежа"""
    # try:
    global hlink_menu, hlink_profile

    # Check if the user has access to the "List of contracts" page
    if login_app.current_user.get_role() != 1:
        return error_handlers.handle403(403)
    else:

        user_id = login_app.current_user.get_id()
        # Connect to the database
        conn, cursor = login_app.conn_cursor_init_dict()

        # Список наших компаний из таблицы contractors
        cursor.execute(
            "SELECT contractor_id, contractor_name FROM our_companies WHERE inflow_active is true"
        )
        our_companies = cursor.fetchall()

        # Список типов поступлений из таблицы payment_inflow_type
        cursor.execute("SELECT * FROM payment_inflow_type")
        inflow_types = cursor.fetchall()

        # Последние 5 поступлений из таблицы payment_inflow_type
        cursor.execute("""
        SELECT 
            date_trunc('second', timezone('UTC-3', t1.inflow_at)::timestamp) AS inflow_at,
            t1.inflow_sum,
            t2.contractor_name,
            t1.inflow_description            
        FROM payments_inflow_history AS t1
        LEFT JOIN (
                    SELECT  
                        contractor_id,
                        contractor_name
                    FROM our_companies
            ) AS t2 ON t1.inflow_company_id = t2.contractor_id
        ORDER BY inflow_at DESC LIMIT 5""")
        historical_data = cursor.fetchall()

        # Список балансов компаний
        cursor.execute("""
        SELECT 
            t1.contractor_name,
            COALESCE(t2.balance_sum, 0) AS balance_sum           
        FROM our_companies AS t1
        LEFT JOIN (
                    SELECT  
                        company_id,
                        balance_sum
                    FROM payments_balance
            ) AS t2 ON t1.contractor_id = t2.company_id
        ORDER BY t1.contractor_id 
        LIMIT 3
        """)
        companies_balances = cursor.fetchall()

        # Список балансов других компаний
        cursor.execute("""
        SELECT 
            t1.contractor_name,
            COALESCE(t2.balance_sum, 0) AS balance_sum           
        FROM our_companies AS t1
        LEFT JOIN (
                    SELECT  
                        company_id,
                        balance_sum
                    FROM payments_balance
            ) AS t2 ON t1.contractor_id = t2.company_id
        ORDER BY t1.contractor_id 
        OFFSET 3
        """)
        subcompanies_balances = cursor.fetchall()

        print(companies_balances)
        print(subcompanies_balances)

        login_app.conn_cursor_close(cursor, conn)

        # Create profile name dict
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        not_save_val = session['n_s_v_cash_inflow'] if session.get('n_s_v_cash_inflow') else {}

        return render_template(
            template_name_or_list='cash-inflow.html', menu=hlink_menu, menu_profile=hlink_profile,
            our_companies=our_companies, inflow_types=inflow_types, historical_data=historical_data,
            not_save_val=not_save_val, companies_balances=companies_balances, page=request.path[1:],
            subcompanies_balances=subcompanies_balances, title='Поступления денежных средств')
    # except Exception as e:
    #     return f'get_cash_inflow ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/cash-inflow', methods=['POST'])
@login_required
def set_cash_inflow():
    """Сохранение согласованные платежи на оплату в БД"""
    try:
        if request.method == 'POST':
            # Список выделенных столбцов
            inflow_company_id = int(request.form.get('our_company').split('-@@@-')[0])  # id компании
            inflow_company = request.form.get('our_company').split('-@@@-')[1]  # Название компания
            inflow_type_id = int(request.form.get('inflow_type').split('-@@@-')[0])  # id типа поступления
            inflow_type = request.form.get('inflow_type').split('-@@@-')[1]  # Название типа поступления
            inflow_sum = convert_amount(request.form['cash_inflow_sum'])  # Сумма поступления
            try:
                taker_company_id = int(request.form.get('taker_company').split('-@@@-')[0])  # id компании
                taker_company = request.form.get('taker_company').split('-@@@-')[1]  # Название компания
            except:
                taker_company_id = None
                taker_company = None
            try:
                inflow_description = request.form['cash_inflow_description']  # Комментарий
            except:
                inflow_description = None

            user_id = login_app.current_user.get_id()

            print('inflow_company_id =', type(inflow_company_id), inflow_company_id, '\ninflow_type_id =', inflow_type_id,
                  '\ninflow_sum =', inflow_sum, '\ninflow_description =', inflow_description)

            action_i_h = 'INSERT INTO'
            table_i_h = 'payments_inflow_history'
            columns_i_h = ('inflow_company_id', 'inflow_description', 'inflow_type_id', 'inflow_sum', 'inflow_owner')
            query_i_h = get_db_dml_query(action=action_i_h, table=table_i_h, columns=columns_i_h)
            values_i_h = [[inflow_company_id, inflow_description, inflow_type_id, inflow_sum, user_id]]

            action_b = 'INSERT CONFLICT UPDATE'
            table_b = 'payments_balance'
            columns_b = ('balance_sum', 'company_id')

            conn, cursor = login_app.conn_cursor_init()

            try:
                # Если Тип поступления "Поступление ДС",
                # то добавляем данные в таблицы payments_inflow_history и payments_balance
                if inflow_type_id == 1:
                    # Запись в таблицу payments_inflow_history
                    execute_values(cursor, query_i_h, values_i_h)

                    # Запись в таблицу payments_balance
                    # Генерируем выражение: к текущему значению всех колонок добавляем новое
                    expr_set = ', '.join([f"{col} = t1.{col} + EXCLUDED.{col}" for col in columns_b[:-1]])

                    query_b = get_db_dml_query(action=action_b, table=table_b, columns=columns_b, expr_set=expr_set)
                    values_b = [[inflow_sum, inflow_company_id]]
                    execute_values(cursor, query_b, values_b)
                    flash(message=['Поступление добавлено', ''], category='success')

                # Если Тип поступления "П.О.", то пока ничего не делаем
                elif inflow_type_id == 2:
                    flash(message=['Действие отменено', 'Тип поступления П.О. не работает'], category='error')
                    return redirect(url_for('.get_cash_inflow'))

                # Если Тип поступления "Корректирующий платеж",
                # то перемещаем средства между компания в таблице payments_balance
                elif inflow_type_id == 3:
                    flash(message=['Действие отменено', 'Тип поступления \"Корректирующий платеж\" не работает'],
                          category='error')
                    return redirect(url_for('.get_cash_inflow'))

                # Если Тип поступления "Внутренний платеж",
                # то перемещаем средства между компания в таблице payments_balance
                elif inflow_type_id == 4:
                    # Проверяем, хватает ли средств у inflow_company
                    query = """
                    SELECT 
                        balance_sum 
                    FROM payments_balance 
                    WHERE company_id::int = %s
                    """
                    execute_values(cursor, query, [[inflow_company_id]])
                    balance_sum = cursor.fetchone()
                    balance_sum = 0 if not balance_sum else balance_sum[0]
                    if balance_sum < inflow_sum:
                        print('balance_sum < inflow_sum')
                        flash(message=[
                            'Действие отменено',
                            f'На счету компании: {inflow_company} недостаточно средств ({balance_sum} ₽) '
                            f'для перевода.\nНе хватает:  {inflow_sum - float(balance_sum)} ₽\n\nОтмена операции'],
                              category='error')
                        return redirect(url_for('.get_cash_inflow'))

                    # Запись в таблицу payments_inflow_history
                    inflow_description = f"из {inflow_company} {inflow_sum} ₽"
                    query_i_h = get_db_dml_query(action=action_i_h, table=table_i_h, columns=columns_i_h)
                    values_i_h = [[taker_company_id, inflow_description, inflow_type_id, inflow_sum, user_id]]
                    execute_values(cursor, query_i_h, values_i_h)

                    # Запись в таблицу payments_balance
                    # Генерируем выражение: к текущему значению всех колонок добавляем новое. Прибавляем у taker_comp
                    expr_set = ', '.join([f"{col} = t1.{col} + EXCLUDED.{col}" for col in columns_b[:-1]])
                    query_b = get_db_dml_query(action=action_b, table=table_b, columns=columns_b, expr_set=expr_set)
                    values_b = [[inflow_sum, taker_company_id]]
                    execute_values(cursor, query_b, values_b)
                    # Генерируем выражение: из тек. знач. вычитаем (прибалвяем отрицательную inflow_sum. Вычитание у inflow_company
                    expr_set = ', '.join([f"{col} = t1.{col} + EXCLUDED.{col}" for col in columns_b[:-1]])
                    query_b = get_db_dml_query(action=action_b, table=table_b, columns=columns_b, expr_set=expr_set)
                    # inflow_sum = -inflow_sum
                    values_b = [[-inflow_sum, inflow_company_id]]
                    execute_values(cursor, query_b, values_b)

                    flash(message=['Внутренний платеж осуществлён', ''], category='success')

                conn.commit()

                login_app.conn_cursor_close(cursor, conn)
                session.pop('n_s_v_cash_inflow', default=None)

                return redirect(url_for('.get_cash_inflow'))

            except Exception as e:
                conn.rollback()
                login_app.conn_cursor_close(cursor, conn)

                session['n_s_v_cash_inflow'] = {
                    'o_c': [inflow_company_id, inflow_company],
                    'i_t': [inflow_type_id, inflow_type],
                    'c_i_s': request.form.get('cash_inflow_sum'),
                }
                if taker_company_id:
                    session['n_s_v_cash_inflow']['t_c'] = [taker_company_id, taker_company]
                if inflow_description:
                    session['n_s_v_cash_inflow']['i_d'] = inflow_description

                print(f'отправка set_cash_inflow ❗❗❗ Ошибка \n---{e}')
                flash(message=['Ошибка. Данные не сохранены', str(e)], category='error')
                return redirect(url_for('.get_cash_inflow'))

    except Exception as e:
        return f'set_cash_inflow ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/payment-pay')
@login_required
def get_unpaid_payments():

    """Выгрузка из БД списка несогласованных платежей"""
    try:
        global hlink_menu, hlink_profile

        # Check if the user has access to the "List of contracts" page
        if login_app.current_user.get_role() != 1:
            return error_handlers.handle403(403)
        else:
            user_id = login_app.current_user.get_id()
            # Connect to the database
            conn, cursor = login_app.conn_cursor_init_dict()

            # Список неоплаченных платежей
            cursor.execute(
                """SELECT 
                    t0.payment_id AS payment_id,
                    t1.payment_number,
                    t3.contractor_name,
                    t3.contractor_id,
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
                    COALESCE(t7.paid_sum, null) AS paid_sum,
                    COALESCE(TRIM(to_char(t7.paid_sum, '999 999 999D99 ₽')), '') AS paid_sum_rub,
                    COALESCE(t8.amount, null) AS amount,
                    COALESCE(TRIM(to_char(t8.amount, '999 999 999D99 ₽')), '') AS amount_rub,
                    t1.payment_due_date,
                    t0.approval_fullpay_close_status AS payment_full_agreed_status,
                    date_trunc('second', timezone('UTC-3', t1.payment_at)::timestamp) AS payment_at
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
                        SELECT 
                            DISTINCT payment_id,
                            SUM(paid_sum) OVER (PARTITION BY payment_id) AS paid_sum
                        FROM payments_paid_history
                ) AS t7 ON t0.payment_id = t7.payment_id
                LEFT JOIN (
                        SELECT DISTINCT ON (payment_id) 
                            parent_id::int AS payment_id,
                            parameter_value::float AS amount
                        FROM payment_draft
                        WHERE page_name = %s AND parameter_name = %s AND user_id = %s
                        ORDER BY payment_id, create_at DESC
                ) AS t8 ON t0.payment_id = t8.payment_id
                ORDER BY t1.payment_due_date;
                """,
                ['payment-pay', 'amount', user_id]
            )
            all_payments = cursor.fetchall()

            # Список согласованных платежей
            cursor.execute("SELECT * FROM payments_approval")
            unapproved_payments = cursor.fetchall()

            # Список статусов платежей Андрея
            cursor.execute(
                """SELECT payment_agreed_status_id,
                          payment_agreed_status_name
                FROM payment_agreed_statuses WHERE payment_agreed_status_category = 'Andrew'""")
            approval_statuses = cursor.fetchall()

            # ДС на счету
            cursor.execute(
                """SELECT
                    sum(balance_sum) AS account_money
                FROM payments_balance
                """
            )
            account_money = cursor.fetchone()
            account_money = account_money[0] if account_money[0] else 0

            # Сумма ранее согласованных платежей
            cursor.execute(
                """SELECT
                    sum(approval_sum) AS approval_sum
                FROM payments_approval
                """
            )
            available_money = cursor.fetchone()
            login_app.conn_cursor_close(cursor, conn)
            available_money = account_money - available_money[0] if available_money[0] else account_money

            # Create profile name dict
            hlink_menu, hlink_profile = login_app.func_hlink_profile()


            return render_template(
                'payment-pay.html', menu=hlink_menu, menu_profile=hlink_profile,
                applications=all_payments, approval_statuses=approval_statuses, account_money=account_money,
                available_money=available_money, page=request.path[1:], title='Оплата платежей')
    except Exception as e:
        pprint(e)
        return f'get_unpaid_payments ❗❗❗ Ошибка \n---{e}'




@payment_app_bp.route('/payment-pay', methods=['POST'])
@login_required
def set_paid_payments():
    """Сохранение оплаченных платежей в БД"""
    try:
        if request.method == 'POST':
            # Список выделенных столбцов
            selected_rows = request.form.getlist('selectedRows')  # Выбранные столбцы
            contractor_id = request.form.getlist('contractor_id')  # id наших компаний (передаётся id)
            payment_number = request.form.getlist('payment_number')  # Номера платежей (передаётся id)
            payment_pay_sum = request.form.getlist('amount')  # Оплаченные суммы
            payment_full_agreed_status = request.form.getlist('payment_full_agreed_status')  # Сохранить до полной опл.

            selected_rows = [int(i) for i in selected_rows]
            contractor_id = [int(i) for i in contractor_id]
            payment_number = [int(i) for i in payment_number]
            payment_pay_sum = [convert_amount(i) for i in payment_pay_sum]
            payment_full_agreed_status = [int(i) for i in payment_full_agreed_status]

            # Данные для удаления временных данных из таблицы payment_draft
            values_p_d = []
            page_name = 'payment-pay'
            parameter_name = 'amount'

            values_b = []  # Список измененных балансов для БД payments_balance
            values_a_u = []  # Список измененных согласованных заявок
            values_a_d = []  # Список удалённых согласованных заявок
            values_p_h = []  # Список оплаченных заявок для записи на БД payments_paid_history
            pay_id_list_raw = []  # Список согласованных id заявок без обработки ошибок
            pay_id_closed = []  # Список закрывающихся заявок

            user_id = login_app.current_user.get_id()
            #
            # print('   selected_rows   ')
            # print(selected_rows)
            # print('   payment_number   ')
            # print(payment_number)
            # print('   payment_pay_sum   ')
            # print(payment_pay_sum)
            # print('   payment_full_agreed_status   ')
            # print(payment_full_agreed_status)

            # for key, val in request.form.items():
            #     print('  - ', key, val)

            for i in selected_rows:
                row = i - 1

                if payment_pay_sum[row] is None:
                    flash(message=['Не указана сумма к оплате', f'№ строки {i}'], category='error')
                    return redirect(url_for('.get_unpaid_payments'))

                pay_id_list_raw.append(payment_number[row])

            conn, cursor = login_app.conn_cursor_init_dict()

            # Список балансов компании
            query = """
            SELECT 
                company_id,
                balance_sum
            FROM payments_balance;
            """
            cursor.execute(query)
            companies_balance = cursor.fetchall()

            # Список согласованных сумм. Их используем при проверке статуса закрытия платежа
            query = """
            SELECT 
                payment_id, 
                approval_sum
            FROM payments_approval 
            WHERE payment_id::int in %s
            """
            execute_values(cursor, query, [pay_id_list_raw])
            approval_sum = cursor.fetchall()

            for i in selected_rows:
                row = i - 1

                # Если согласованная сумма больше суммы к оплате и не стоит галка "закрыть после полной оплаты",
                # то статус оплаты - "Частичная оплата с закрытием" (id=11); если галка стоит -"Частичная оплата (id=10)
                # иначе "Полная оплата" (id=9)
                for s in approval_sum:
                    if s[0] == payment_number[row]:
                        if s[1] > payment_pay_sum[row]:
                            if i not in payment_full_agreed_status:
                                status_id = 11
                                values_a_d.append((
                                    payment_number[row],
                                ))
                            else:
                                status_id = 10
                                values_a_u.append((
                                    payment_number[row],
                                    float(s[1]) - payment_pay_sum[row]
                                ))
                        else:
                            status_id = 9
                            values_a_d.append(payment_number[row])



                if i not in payment_full_agreed_status:
                    pay_id_closed.append((
                        payment_number[row],
                    ))

                values_p_h.append([
                    payment_number[row],
                    status_id,
                    user_id,
                    payment_pay_sum[row]
                ])

                values_b.append([
                    contractor_id[row],
                    payment_pay_sum[row]
                ])

                values_p_d.append((
                    page_name,
                    payment_number[row],
                    parameter_name,
                    user_id
                ))

            # Пересчитываем баланс компаний
            for val in values_b:
                for com in companies_balance:
                    if val[0] == com[0]:
                        com[1] = float(com[1]) - val[1]

            print('values_p_h', values_p_h)

            print('pay_id_closed', pay_id_closed)

            print('values_a_u', values_a_u)
            print('values_a_d', values_a_d)

            try:
                # Если есть что записывать в Базу данных
                if values_p_h:
                    # Перезапись в payments_paid_history
                    action_p_h = 'INSERT INTO'
                    table_p_h = 'payments_paid_history'
                    columns_p_h = ('payment_id', 'status_id', 'user_id', 'paid_sum')
                    query_p_h = get_db_dml_query(action=action_p_h, table=table_p_h, columns=columns_p_h)
                    execute_values(cursor, query_p_h, values_p_h)

                    # Обновляем балансы компаний
                    columns_b = ("company_id", "balance_sum")
                    query_b = get_db_dml_query(action='UPDATE', table='payments_balance', columns=columns_b)
                    execute_values(cursor, query_b, companies_balance)

                    # Удаляем временные данные из payment_draft
                    columns_p_d = 'page_name, parent_id::int, parameter_name, user_id::int'
                    query_p_d = get_db_dml_query(action='DELETE', table='payment_draft', columns=columns_p_d)
                    execute_values(cursor, query_p_d, (values_p_d,))

                # Если есть заявки с закрытием
                if values_a_d:
                    columns_a_d = 'payment_id'
                    query_a_d = get_db_dml_query(action='DELETE', table='payments_approval', columns=columns_a_d)
                    execute_values(cursor, query_a_d, (values_a_d,))

                # Если есть заявки с частичным закрытием
                if values_a_u:
                    columns_a_u = ("payment_id", "approval_sum")
                    query_a_u = get_db_dml_query(action='UPDATE', table='payments_approval', columns=columns_a_u)
                    execute_values(cursor, query_a_u, values_a_u)

                flash(message=['Заявки проведены', ''], category='success')

                conn.commit()
                login_app.conn_cursor_close(cursor, conn)

                return redirect(url_for('.get_unpaid_payments'))

            except Exception as e:
                conn.rollback()

                flash(message=['Не указана сумма к оплате', f'№ строки {i}'], category='error')

                login_app.conn_cursor_close(cursor, conn)

                print(e)
                return f'отправка set_paid_payments 1 ❗❗❗ Ошибка \n---{e}'

    except Exception as e:
        print(e)
        return f'отправка set_approved_payments 2 ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/payment-approval-list')
@login_required
def get_payments_approval_list():
    """Выгрузка из БД списка оплаченных платежей"""
    try:
        global hlink_menu, hlink_profile

        # Check if the user has access to the "List of contracts" page
        if login_app.current_user.get_role() != 1:
            return error_handlers.handle403(403)
        else:
            user_id = login_app.current_user.get_id()
            # Connect to the database
            conn, cursor = login_app.conn_cursor_init_dict()

            # Список оплаченных платежей
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
                        COALESCE(TRIM(to_char(t0.approval_sum, '999 999 999D99 ₽')), '') AS approval_sum_rub,
                        date_trunc('second', timezone('UTC-3', t0.create_at)::timestamp) AS create_at,
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
                ORDER BY create_at;
                """
            )
            all_payments = cursor.fetchall()

            # ДС на счету
            cursor.execute(
                """SELECT
                    sum(balance_sum) AS account_money
                FROM payments_balance
                """
            )
            account_money = cursor.fetchone()
            account_money = account_money[0] if account_money[0] else 0

            # Сумма ранее согласованных платежей
            cursor.execute(
                """SELECT
                    sum(approval_sum) AS approval_sum
                FROM payments_approval
                """
            )
            available_money = cursor.fetchone()
            available_money = account_money - available_money[0] if available_money[0] else account_money

            login_app.conn_cursor_close(cursor, conn)

            # Create profile name dict
            hlink_menu, hlink_profile = login_app.func_hlink_profile()

            return render_template(
                'payment-approval-list.html', menu=hlink_menu, menu_profile=hlink_profile,
                applications=all_payments, account_money=account_money, available_money=available_money,
                title='СПИСОК СОГЛАСОВАННЫХ ПЛАТЕЖЕЙ')
    except Exception as e:
        pprint(e)
        return f'get_payments_approval_list ❗❗❗ Ошибка \n---{e}'


@payment_app_bp.route('/payment-paid-list')
@login_required
def get_payments_paid_list():
    """Выгрузка из БД списка оплаченных платежей"""
    try:
        global hlink_menu, hlink_profile

        # Check if the user has access to the "List of contracts" page
        if login_app.current_user.get_role() != 1:
            return error_handlers.handle403(403)
        else:
            user_id = login_app.current_user.get_id()
            # Connect to the database
            conn, cursor = login_app.conn_cursor_init_dict()

            # Список оплаченных платежей
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
                        t2.approval_sum,
                        TRIM(to_char(t2.approval_sum, '9 999 999D99 ₽')) AS approval_sum_rub,
                        SUM(t0.paid_sum) OVER (PARTITION BY t0.payment_id) AS paid_sum,
                        COALESCE(TRIM(to_char(SUM(t0.paid_sum) OVER (PARTITION BY t0.payment_id), '999 999 999D99 ₽')), '') AS paid_sum_rub,
                        t1.payment_due_date,
                        date_trunc('second', timezone('UTC-3', t1.payment_at)::timestamp) AS payment_at,
                        t8.status_name
                    FROM payments_paid_history AS t0
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
                            SELECT DISTINCT ON (payment_id) 
                                payment_id,
                                status_id,
                                SUM(approval_sum) OVER (PARTITION BY payment_id) AS approval_sum
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
                            SELECT DISTINCT ON (payment_id) 
                                payment_id,
                                status_id
                            FROM payments_approval_history
                            ORDER BY payment_id, create_at DESC
                    ) AS t7 ON t0.payment_id = t7.payment_id
                    LEFT JOIN (
                            SELECT payment_agreed_status_id AS status_id,
                                payment_agreed_status_name AS status_name
                            FROM payment_agreed_statuses
                    ) AS t8 ON t7.status_id = t8.status_id
                    ORDER BY t1.payment_due_date;
                    """
            )
            all_payments = cursor.fetchall()

            # ДС на счету
            cursor.execute(
                """SELECT
                    sum(balance_sum) AS account_money
                FROM payments_balance
                """
            )
            account_money = cursor.fetchone()
            account_money = account_money[0] if account_money[0] else 0

            # Сумма ранее согласованных платежей
            cursor.execute(
                """SELECT
                    sum(approval_sum) AS approval_sum
                FROM payments_approval
                """
            )
            available_money = cursor.fetchone()
            available_money = account_money - available_money[0] if available_money[0] else account_money

            login_app.conn_cursor_close(cursor, conn)

            # Create profile name dict
            hlink_menu, hlink_profile = login_app.func_hlink_profile()

            return render_template(
                'payment-paid-list.html', menu=hlink_menu, menu_profile=hlink_profile,
                applications=all_payments, account_money=account_money, available_money=available_money,
                title='СПИСОК ОПЛАЧЕННЫХ ПЛАТЕЖЕЙ')
    except Exception as e:
        pprint(e)
        return f'get_payments_paid_list ❗❗❗ Ошибка \n---{e}'


# Создание запроса в БД для множественного внесения данных
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


# Превращаем строковое значение стоимости с пропусками и руб. в число
def convert_amount(amount):
    try:
        amount = float(amount.replace('₽', '').replace(' руб.', '').replace(" ", "").replace(",", "."))
    except:
        amount = None
    return amount
