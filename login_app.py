import psycopg2
import psycopg2.extras
from pprint import pprint
from flask import g, abort, request, render_template, redirect, flash, url_for, get_flashed_messages, Blueprint
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from user_login import UserLogin
from FDataBase import FDataBase

login_bp = Blueprint('login_app', __name__)

login_manager = LoginManager()
login_manager.login_view = 'login_app.login'
login_manager.login_message = ["Не достаточно прав для доступа", '']
login_manager.login_message_category = "success"


@login_bp.record_once
def on_load(state):
    try:
        login_manager.init_app(state.app)
    except Exception as e:
        return f'on_load ❗❗❗ Ошибка \n---{e}'


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
        global hlink_menu, hlink_profile

        # Create profile name dict
        hlink_menu, hlink_profile = func_hlink_profile()
        if current_user.is_authenticated:
            return redirect(url_for('login_app.index'))

        if request.method == 'POST':
            conn = conn_init()
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
                return redirect(request.args.get("next") or url_for("login_app.index"))

            conn.close()
            return redirect(url_for('.login'))

        return render_template("login.html", title="Авторизация", menu=hlink_menu,
                               menu_profile=hlink_profile)
    except Exception as e:
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

        return render_template("profile.html", title="Профиль", menu=hlink_menu,
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
                    if res:
                        # Close the database connection
                        conn.close()
                        return redirect(url_for('.register'))
                    else:
                        conn.rollback()
                        conn.close()
                        return redirect(url_for('.register'))

                except Exception as e:
                    flash(message=['register ❗❗❗ Ошибка', str(e)], category='error')
                    return redirect(url_for('.register'))

            return render_template("register.html", title="Регистрация", menu=hlink_menu,
                                   menu_profile=hlink_profile)
    except Exception as e:
        return f'register ❗❗❗ Ошибка \n---{e}'


def func_hlink_profile():
    # try:
    global hlink_menu, hlink_profile

    if current_user.is_authenticated:
        # Меню профиля
        hlink_profile = {
            "name": [current_user.get_profile_name(), '(Выйти)'], "url": "logout"},

        # Check user role.
        # Role: Admin
        if current_user.get_role() == 1:

            # НОВЫЙ СПИСОК МЕНЮ - СПИСОК СЛОВАРЕЙ со словарями
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [
                        {"name": "Добавить поступления", "url": "cash-inflow",
                         "img": "https://cdn-icons-png.flaticon.com/512/617/617002.png"},
                        {"name": "Новая заявка на оплату", "url": "new-payment",
                         "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                        {"name": "Согласование платежей", "url": "payment-approval",
                         "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"},
                        {"name": "Оплата платежей", "url": "payment-pay",
                         "img": "https://cdn-icons-png.flaticon.com/512/3673/3673443.png"},
                        {"name": "Список платежей", "url": "payment_list",
                         "img": "https://cdn-icons-png.flaticon.com/512/4631/4631071.png"},
                    ]
                 },
                {"menu_item": "Администрирование", "sub_item":
                    [{"name": "Регистрация пользователей", "url": "register",
                      "img": "https://cdn-icons-png.flaticon.com/512/477/477801.png"}, ]
                 },
            ]
        else:
            hlink_menu = [
                {"menu_item": "Платежи", "sub_item":
                    [{"name": "Новая заявка на оплату", "url": "new-payment",
                      "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                     {"name": "Список платежей", "url": "payment_list",
                      "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"}, ]
                 },
            ]

    else:
        # Меню профиля
        hlink_profile = {
            "name": ["Вы используете гостевой доступ", '(Войти)'], "url": "login"},

        hlink_menu = [
            {"menu_item": "Платежи", "sub_item":
                [
                    {"name": "Новая заявка на оплату", "url": "new-payment",
                     "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                ]
             },
        ]

    return hlink_menu, hlink_profile
    # except Exception as e:
    #     return f'func_hlink_profile ❗❗❗ Ошибка \n---{e}'

