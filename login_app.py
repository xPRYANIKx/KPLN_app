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
login_manager.login_message = ["❗  Не достаточно прав для доступа", '']
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
hlnk_menu = None

# Меню профиля
hlnk_profile = None


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

        # Clear the flashed messages list
        get_flashed_messages()
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
        global hlnk_menu, hlnk_profile

        # Create profile name dict
        hlnk_menu, hlnk_profile = func_hlnk_profile()

        return render_template('index.html', menu=hlnk_menu,
                               menu_profile=hlnk_profile, title='Главная страница')
    except Exception as e:
        return f'❗❗❗ index \n---{e}'


@login_bp.route("/login", methods=["POST", "GET"])
def login():
    try:
        global hlnk_menu, hlnk_profile

        # Create profile name dict
        hlnk_menu, hlnk_profile = func_hlnk_profile()
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

            flash(message=['❌ Логин или пароль указан неверно', ''], category='error')
            conn.close()
            # return redirect(url_for('login'))
            return render_template(
                "login.html", title="Авторизация", menu=hlnk_menu, menu_profile=hlnk_profile,
                error_msg='❌ Логин или пароль указан неверно')

        # return redirect(url_for('login'))
        return render_template("login.html", title="Авторизация", menu=hlnk_menu,
                               menu_profile=hlnk_profile)
    except Exception as e:
        return f'login ❗❗❗ Ошибка \n---{e}'


@login_bp.route('/logout')
@login_required
def logout():
    try:
        global hlnk_menu, hlnk_profile

        logout_user()
        hlnk_menu, hlnk_profile = func_hlnk_profile()
        # flash(message=['Вы вышли из аккаунта', ''], category='success')

        return redirect(request.args.get('next') or request.referrer)
    except Exception as e:
        return f'logout ❗❗❗ Ошибка \n---{e}'


@login_bp.route('/profile')
@login_required
def profile():
    try:
        global hlnk_menu, hlnk_profile
        name = current_user.get_name()

        # Create profile name dict
        hlnk_menu, hlnk_profile = func_hlnk_profile()

        return render_template("profile.html", title="Профиль", menu=hlnk_menu,
                               menu_profile=hlnk_profile, name=name)
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

            return render_template("register.html", title="Регистрация", menu=hlnk_menu,
                                   menu_profile=hlnk_profile)
    except Exception as e:
        return f'register ❗❗❗ Ошибка \n---{e}'


#
# # Обработчик ошибки 403
# @login_bp.errorhandler(403)
# def permission_error(error):
#     try:
#         return render_template('page403.html', title="Нет доступа"), 403
#     except Exception as e:
#         return f'permission_error ❗❗❗ Ошибка \n---{e}'
#
#
# # Обработчик ошибки 404
# @login_bp.errorhandler(404)
# def page_not_fount(error):
#     try:
#         return render_template('page404.html', title="Страница не найдена"), 404
#     except Exception as e:
#         return f'page_not_fount ❗❗❗ Ошибка \n---{e}'


def func_hlnk_profile():
    # try:
    global hlnk_menu, hlnk_profile

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
            #              {"name": "Новый платеж", "url": "new-payment",
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
            #             [{"name": "Новый платеж", "url": "new-payment",
            #               "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
            #              {"name": "Список платежей", "url": "payment_list",
            #               "img": "https://cdn-icons-png.flaticon.com/512/1572/1572585.png"}, ]
            #          },
            #     ]
            #

            hlnk_menu = [
                {"name": "Главная страница", "url": "/",
                 "img": "https://cdn-icons-png.flaticon.com/512/6489/6489329.png"},
                {"name": "Добавить поступления", "url": "cash-inflow",
                 "img": "https://cdn-icons-png.flaticon.com/512/617/617002.png"},
                {"name": "Новый платеж", "url": "new-payment",
                 "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
                {"name": "Согласование платежей", "url": "payment-approval",
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
                {"name": "Новый платеж", "url": "new-payment",
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
            {"name": "Новый платеж", "url": "new-payment",
             "img": "https://cdn-icons-png.flaticon.com/512/5776/5776429.png"},
            # {"name": "Авторизация", "url": "login",
            #  "img": "https://cdn-icons-png.flaticon.com/512/2574/2574003.png"},
        ]

    return hlnk_menu, hlnk_profile
    # except Exception as e:
    #     return f'func_hlnk_profile ❗❗❗ Ошибка \n---{e}'
