import psycopg2
import psycopg2.extras
from flask import Flask, g, request, render_template, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from werkzeug.security import check_password_hash
from user_login import UserLogin
from FDataBase import FDataBase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yyazaxkoaxb4w8vgj7a7p1lxfb7gee6n5hx'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

db_name = "kpln_db"
# db_user = "kpln_user"
# db_password = "123"
db_user = "postgres"
db_password = "postgres"
db_host = "localhost"
db_port = "5432"

dbase = None

hlnk = [{"name": "Список объектов", "url": "contracts_list"},]


def coon_init():
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    return conn


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().from_db(user_id, dbase)


@app.before_request
def before_request():
    global dbase
    conn = coon_init()
    dbase = FDataBase(conn)


def coon_cursor_init():
    conn = coon_init()
    cursor = conn.cursor()
    return conn, cursor


def coon_cursor_close(cursor, conn):
    cursor.close()
    conn.close()


@app.route('/')
def index():
    try:
        conn, cursor = coon_cursor_init()
        cursor.execute("SELECT object_name FROM objects")
        objects = cursor.fetchall()
        cursor.execute("SELECT contract_type_name FROM contract_types")
        contract_types = cursor.fetchall()
        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("SELECT contractor_name FROM contractors")
        contractor_name = cursor.fetchall()
        cursor.execute("SELECT contract_status_name FROM contract_statuses")
        contract_status_name = cursor.fetchall()
        cursor.execute("SELECT contract_purpose_name FROM contract_purposes")
        contract_purpose_name = cursor.fetchall()
        cursor.execute("SELECT vat_name FROM vat")
        vat_name = cursor.fetchall()
        coon_cursor_close(cursor, conn)

        return render_template('new_contr.html', objects=objects, contract_types=contract_types, today=today, contractor_name=contractor_name, contract_status_name=contract_status_name, contract_purpose_name=contract_purpose_name, vat_name=vat_name, menu=hlnk, title='Новый договор 📝')
    except Exception as e:
        return f'❗❗❗ Ошибка \n---{e}'


@app.route('/', methods=['POST'])
def save_data():
    if request.method == 'POST':
        object = request.form.get('object')
        contract_type = request.form.get('contract_type')
        date_row = request.form.get('date')
        contract_number = request.form.get('contract_number')
        customer = request.form.get('customer')
        contractor = request.form.get('contractor')
        contract_comment = request.form.get('contract_comment')
        contract_status = request.form.get('contract_status')
        contract_purpose = request.form.get('contract_purpose')
        vat = request.form.get('vat')
        conn, cursor = coon_cursor_init()
        query = "INSERT INTO new_objects (object_name, contract_type, date_row, contract_number, customer, contractor, contract_comment, contract_status, contract_purpose, vat, vat_value) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT vat_value FROM vat WHERE vat_name = %s))"
        values = (object, contract_type, date_row, contract_number, customer, contractor, contract_comment,contract_status, contract_purpose, vat, vat)

        try:
            cursor.execute(query, values)
            conn.commit()
            coon_cursor_close(cursor, conn)
            flash('✔️ Договор сохранён', category='success')
            return render_template('new_contr.html', menu=hlnk, title='Новый договор 📝')
        except Exception as e:
            conn.rollback()
            coon_cursor_close(cursor, conn)
            flash(f'❌ Договор НЕ сохранён \n---{e}', category='error')
            return render_template('new_contr.html', menu=hlnk, title='Новый договор 📝')
    return render_template('new_contr.html')


def get_contracts(filter_by=None, sort_by=None):
    try:
        conn, cursor = coon_cursor_init()
        if filter_by is not None:
            query = f"SELECT * FROM new_objects WHERE contract_status = '{filter_by}'"
        else:
            query = "SELECT * FROM new_objects"
        if sort_by is not None:
            query += f" ORDER BY {sort_by}"
        cursor.execute(query)
        contracts = cursor.fetchall()
        coon_cursor_close(cursor, conn)
        return contracts
    except:
        return 'error'


@app.route('/profile')
@login_required
def profile():
    name = current_user.get_name()
    return render_template("profile.html", title="Профиль", menu=hlnk, name=name)


@app.route("/login", methods=["POST", "GET"])
def login():
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
        return render_template("login.html", title="Авторизация", menu=hlnk)

    return render_template("login.html", title="Авторизация", menu=hlnk)


if __name__ == '__main__':
    app.run()
