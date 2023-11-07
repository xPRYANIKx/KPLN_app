import flask
from flask import render_template, current_app
import login_app

errorhandler_bp = flask.Blueprint('error_handlers', __name__)


@errorhandler_bp.before_request
def before_request():
    login_app.before_request()


# Обработчик ошибки 403
@errorhandler_bp.app_errorhandler(403)
def handle403(e):
    try:
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        return render_template('page403.html', title="Нет доступа", menu=hlink_menu,
                                   menu_profile=hlink_profile), 403
    except Exception as e:
        return f'permission_error ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 404
@errorhandler_bp.app_errorhandler(404)
def handle404(e):
    try:
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        return render_template('page404.html', title="Страница не найдена", menu=hlink_menu,
                                   menu_profile=hlink_profile), 404
    except Exception as e:
        return f'handle404 ❗❗❗ Ошибка \n---{e}'