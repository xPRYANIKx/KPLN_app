import flask
from flask import render_template

errorhandler_bp = flask.Blueprint('error_handlers', __name__)


# Обработчик ошибки 403
@errorhandler_bp.errorhandler(403)
def permission_error(error):
    try:
        return render_template('page403.html', title="Нет доступа"), 403
    except Exception as e:
        return f'permission_error ❗❗❗ Ошибка \n---{e}'


# Обработчик ошибки 404
@errorhandler_bp.errorhandler(404)
def page_not_fount(error):
    try:
        return render_template('page404.html', title="Страница не найдена"), 404
    except Exception as e:
        return f'page_not_fount ❗❗❗ Ошибка \n---{e}'