from flask import Flask
from payment_app import payment_app_bp
from login_app import login_bp
from error_handlers import errorhandler_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yyazaxkoaxb4w8vgj7a7p1lxfb7gee6n5hx'

app.register_blueprint(login_bp)
app.register_blueprint(payment_app_bp)
app.register_blueprint(errorhandler_bp)

if __name__ == '__main__':
    app.run(debug=True)
