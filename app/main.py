from flask import Flask

from app import config

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config['SECRET_KEY'] = config.secret

from .views import *

if __name__ == '__main__':
    logger = get_logger()
    try:
        app.run(host="0.0.0.0", port=80, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start, Error {e}")
