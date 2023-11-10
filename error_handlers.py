import flask
from flask import render_template, current_app, request
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
        current_app.logger.info(f"url {request.path[1:]}  -  id {login_app.current_user.get_id()}  -  {e}")
        return f'permission_error ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 404
@errorhandler_bp.app_errorhandler(404)
def handle404(e):
    try:
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        return render_template('page404.html', title="Страница не найдена", menu=hlink_menu,
                                   menu_profile=hlink_profile), 404
    except Exception as e:
        current_app.logger.info(f"url {request.path[1:]}  -  id {login_app.current_user.get_id()}  -  {e}")
        return f'handle404 ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 401
@errorhandler_bp.app_errorhandler(401)
def handle401(e):
    try:
        hlink_menu, hlink_profile = login_app.func_hlink_profile()
        return render_template('page401.html', title="Отказ в авторизации. Проверка не пройдена", menu=hlink_menu,
                                   menu_profile=hlink_profile), 401
    except Exception as e:
        current_app.logger.info(f"url {request.path[1:]}  -  id {login_app.current_user.get_id()}  -  {e}")
        return f'permission_error ❗❗❗ Ошибка \n---{e}'
