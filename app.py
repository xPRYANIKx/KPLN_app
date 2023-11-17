from flask import Flask
from payment_app import payment_app_bp
from login_app import login_bp
import error_handlers
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta


app = Flask(__name__)

app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)  # hours

app.config['SECRET_KEY'] = 'kLzQ%5vYkv*2rh)P_?Npvv2AZT@TkbPp=i?]#=cR]R)>YXL1Wpz?PvFNZf9A'

app.logger.setLevel(logging.INFO)  # Set the log level to INFO
# Create a file handler for logging to a file
file_handler = RotatingFileHandler('kpln_payment_log.log', maxBytes=1024 * 1024 * 10, backupCount=10)
# Set the log format
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
app.logger.addHandler(file_handler)

app.logger.info('This is an info message')

app.register_blueprint(login_bp)
app.register_blueprint(payment_app_bp)
app.register_blueprint(error_handlers.errorhandler_bp)


if __name__ == '__main__':
    app.run(debug=True)