from flask import Flask
from payment_app import payment_app_bp
from login_app import login_bp
import error_handlers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kLzQ%5vYkv*2rh)P_?Npvv2AZT@TkbPp=i?]#=cR]R)>YXL1Wpz?PvFNZf9A'



app.register_blueprint(login_bp)
app.register_blueprint(payment_app_bp)
app.register_blueprint(error_handlers.errorhandler_bp)


if __name__ == '__main__':
    app.run(debug=True)