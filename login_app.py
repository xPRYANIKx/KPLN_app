import psycopg2
import psycopg2.extras
from pprint import pprint
from flask import g, abort, request, render_template, redirect, flash, url_for, get_flashed_messages, Blueprint, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from user_login import UserLogin
from FDataBase import FDataBase
from db_data_conf import db_data, recapcha_key
from flask_wtf.recaptcha import RecaptchaField
import requests
import error_handlers


login_bp = Blueprint('login_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'login_app.login'
login_manager.login_message = ["Недостаточно прав для доступа", '']
login_manager.login_message_category = "error"

# reCAPCHA v3
RECAPTCHA_PUBLIC_KEY = recapcha_key()['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = recapcha_key()['RECAPTCHA_PRIVATE_KEY']
# reCAPCHA v3 - localHost
RECAPTCHA_PUBLIC_KEY_LH = recapcha_key()['RECAPTCHA_PUBLIC_KEY_LH']
RECAPTCHA_PRIVATE_KEY_LH = recapcha_key()['RECAPTCHA_PRIVATE_KEY_LH']

RECAPTCHA_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

@login_bp.record_once
def on_load(state):
    try:
        login_manager.init_app(state.app)
    except Exception as e:
        return f'on_load ❗❗❗ Ошибка \n---{e}'


# PostgreSQL database configuration
db_name = db_data()['db_name']
db_user = db_data()['db_user']
db_password = db_data()['db_password']
db_host = db_data()['db_host']
db_port = db_data()['db_port']

dbase = None

# Меню страницы
hlink_menu = None

# Меню профиля
hlink_profile = None


# Конект к БД
def conn_init():
    try:
        g.conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return g.conn
    except Exception as e:
        return f'conn_init ❗❗❗ Ошибка \n---{e}'


# Закрытие соединения
def conn_cursor_close(cursor, conn):
    try:
        g.cursor.close()
        g.conn.close()
    except Exception as e:
        return f'conn_cursor_close ❗❗❗ Ошибка \n---{e}'


@login_manager.user_loader
def load_user(user_id):
    try:
        # conn = conn_init()

        return UserLogin().from_db(user_id, dbase)
    except Exception as e:
        return None


@login_bp.before_request
def before_request():
    try:
        # Установление соединения с БД перед выполнением запроса
        global dbase
        conn = conn_init()
        dbase = FDataBase(conn)

    except Exception as e:
        return f'before_request ❗❗❗ Ошибка \n---{e}'


@login_bp.teardown_app_request
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'conn'):
        g.conn.close()


def conn_cursor_init_dict():
    try:
        conn = conn_init()
        g.cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, g.cursor
    except Exception as e:
        return f'conn_cursor_init ❗❗❗ Ошибка \n---{e}'


def conn_cursor_init():
    try:
        conn = conn_init()
        g.cursor = conn.cursor()
        return conn, g.cursor
    except Exception as e:
        return f'conn_cursor_init ❗❗❗ Ошибка \n---{e}'


@login_bp.route('/', methods=["POST", "GET"])
@login_required
def index():
    """Главная страница"""
    try:
        global hlink_menu, hlink_profile

        # Create profile name dict
        hlink_menu, hlink_profile = func_hlink_profile()

        return render_template('index.html', menu=hlink_menu,
                               menu_profile=hlink_profile, title='Главная страница')
    except Exception as e:
        return f'❗❗❗ index \n---{e}'


@login_bp.route("/login", methods=["POST", "GET"])
def login():
    try:
        global hlink_menu, hlink_profile, RECAPTCHA_PUBLIC_KEY, RECAPTCHA_PRIVATE_KEY

        # Create profile name dict
        hlink_menu, hlink_profile = func_hlink_profile()
        if current_user.is_authenticated:
            return redirect(url_for('login_app.index'))

        if request.headers['Host'] == '127.0.0.1:5000':
            RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY_LH
            RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY_LH

        if request.method == 'POST':
            conn = conn_init()
            dbase = FDataBase(conn)

            email = request.form.get('email')
            password = request.form.get('password')
            remain = request.form.get('remainme')

            secret_response = request.form['g-recaptcha-response']
            verify_response = requests.post(url=f'{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_PRIVATE_KEY}&response={secret_response}').json()

            # if verify_response['success'] == False or verify_response['score'] < 0.5:
            if verify_response['success'] == False:
                return error_handlers.handle401(401)

            user = dbase.get_user_by_email(email)

            if user and check_password_hash(user['password'], password):
                userlogin = UserLogin().create(user)
                login_user(userlogin, remember=remain)
                conn.close()
                # flash(message=['Вы вошли в систему', ''], category='success')
                return redirect(request.args.get("next") or url_for("login_app.index"))

            else:
                flash(message=['Пользователь не найден', ''], category='error')

            conn.close()
            return redirect(url_for('.login'))

        return render_template("login.html", site_key=RECAPTCHA_PUBLIC_KEY,
                               title="Авторизация", menu=hlink_menu,
                               menu_profile=hlink_profile)
    except Exception as e:
        current_app.logger.info(f"url {request.path[1:]}  -  id {current_user.get_id()}  -  {e}")
        return f'login ❗❗❗ Ошибка \n---{e}'


@login_bp.route('/logout')
@login_required
def logout():
    try:
        global hlink_menu, hlink_profile

        logout_user()
        hlink_menu, hlink_profile = func_hlink_profile()
        # flash(message=['Вы вышли из аккаунта', ''], category='success')

        return redirect(request.args.get('next') or request.referrer)
    except Exception as e:
        return f'logout ❗❗❗ Ошибка \n---{e}'


@login_bp.route('/profile')
@login_required
def profile():
    try:
        global hlink_menu, hlink_profile
        name = current_user.get_name()

        # Create profile name dict
        hlink_menu, hlink_profile = func_hlink_profile()

        return render_template("__profile.html", title="Профиль", menu=hlink_menu,
                               menu_profile=hlink_profile, name=name)
    except Exception as e:
        return f'profile ❗❗❗ Ошибка \n---{e}'


@login_bp.route("/register", methods=["POST", "GET"])
@login_required
def register():
    try:
        if current_user.get_role() != 1:
            return abort(403)
        else:

            if request.method == 'POST':
                try:
                    conn = conn_init()
                    dbase = FDataBase(conn)
                    form_data = request.form
                    res = dbase.add_user(form_data)

                    conn, cursor = conn_cursor_init_dict()
                    cursor.execute(
                        """SELECT 
                                *
                        FROM user_role;"""
                    )
                    roles = cursor.fetchall()
                    conn_cursor_close(cursor, conn)
                    if res:
                        # Close the database connection
                        conn.close()
                        return render_template("register.html",
                                               title="Регистрация новых пользователей", menu=hlink_menu,
                                               menu_profile=hlink_profile, roles=roles)
                    else:
                        conn.rollback()
                        conn.close()
                        return render_template("register.html",
                                               title="Регистрация новых пользователей", menu=hlink_menu,
                                               menu_profile=hlink_profile, roles=roles)

                except Exception as e:
                    flash(message=['register ❗❗❗ Ошибка', str(e)], category='error')
                    return render_template("register.html", title="Регистрация новых пользователей",
                                           menu=hlink_menu,
                                           menu_profile=hlink_profile, roles=roles)

            if request.method == 'GET':
                conn, cursor = conn_cursor_init_dict()
                cursor.execute(
                    """SELECT 
                            *
                    FROM user_role;"""
                )
                roles = cursor.fetchall()
                conn_cursor_close(cursor, conn)

            return render_template("register.html", title="Регистрация новых пользователей", menu=hlink_menu,
                                   menu_profile=hlink_profile, roles=roles)
    except Exception as e:
        return f'register ❗❗❗ Ошибка \n---{e}'


def func_hlink_profile():
    # try:
    global hlink_menu, hlink_profile

    if current_user.is_authenticated:
        # Меню профиля
        hlink_profile = {
            "name": [current_user.get_profile_name(), '(Выйти)'], "url": "logout", "role_id": current_user.get_role()},

        # Check user role.
        # Role: Admin
        if current_user.get_role() == 1:
            # НОВЫЙ СПИСОК МЕНЮ - СПИСОК СЛОВАРЕЙ со словарями
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [
                        {"name": "Добавить поступления", "url": "cash-inflow",
                         "img": "/static/img/mainpage/cashinflow.png"},
                        {"name": "Новая заявка на оплату", "url": "new-payment",
                         "img": "/static/img/mainpage/newpayment.png"},
                        {"name": "Согласование платежей", "url": "payment-approval",
                         "img": "/static/img/mainpage/paymentapproval.png"},
                        {"name": "Оплата платежей", "url": "payment-pay",
                         "img": "/static/img/mainpage/paymentpay.png"},
                        {"name": "Список платежей", "url": "payment-list",
                         "img": "/static/img/mainpage/paymentlist.png"},
                    ]
                 },
                {"menu_item": "Администрирование", "sub_item":
                    [{"name": "Регистрация пользователей", "url": "register",
                      "img": "/static/img/mainpage/register.png"}, ]
                 },
            ]

        # Role: Director
        elif current_user.get_role() == 4:
            # НОВЫЙ СПИСОК МЕНЮ - СПИСОК СЛОВАРЕЙ со словарями
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [
                        {"name": "Новая заявка на оплату", "url": "new-payment",
                         "img": "/static/img/mainpage/newpayment.png"},
                        {"name": "Согласование платежей", "url": "payment-approval",
                         "img": "/static/img/mainpage/paymentapproval.png"},
                        {"name": "Список платежей", "url": "payment-list",
                         "img": "/static/img/mainpage/paymentlist.png"},
                    ]
                 },
            ]

        # Role: buh
        elif current_user.get_role() == 6:
            # НОВЫЙ СПИСОК МЕНЮ - СПИСОК СЛОВАРЕЙ со словарями
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [
                        {"name": "Добавить поступления", "url": "cash-inflow",
                         "img": "/static/img/mainpage/cashinflow.png"},
                        {"name": "Новая заявка на оплату", "url": "new-payment",
                         "img": "/static/img/mainpage/newpayment.png"},
                        {"name": "Согласование платежей", "url": "payment-approval",
                         "img": "/static/img/mainpage/paymentapproval.png"},
                        {"name": "Оплата платежей", "url": "payment-pay",
                         "img": "/static/img/mainpage/paymentpay.png"},
                        {"name": "Список платежей", "url": "payment-list",
                         "img": "/static/img/mainpage/paymentlist.png"},
                    ]
                 },
            ]

        else:
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [{"name": "Новая заявка на оплату", "url": "new-payment",
                      "img": "/static/img/mainpage/newpayment.png"},
                     {"name": "Список платежей", "url": "payment-list",
                      "img": "/static/img/mainpage/paymentlist.png"}, ]
                 },
            ]

    else:
        # Меню профиля
        hlink_profile = {
            "name": ["Гостевой доступ", '(Войти)'], "url": "login"},

        hlink_menu = [
            # {"menu_item": "Платежи", "sub_item":
            #     [
            #         {"name": "Новая заявка на оплату", "url": "new-payment",
            #          "img": "/static/img/menu/new-payment.png"},
            #     ]
            #  },
        ]

    return hlink_menu, hlink_profile
    # except Exception as e:
    #     return f'func_hlink_profile ❗❗❗ Ошибка \n---{e}'

