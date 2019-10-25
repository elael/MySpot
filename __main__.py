import logging

from flask import Flask
from threading import Thread
from blueprints import kitchen_blueprint

logger = logging.getLogger(__name__)

app = Flask(__name__)


def thread_web_app(http_port):
    logger.info(f'Starting web server on port {http_port}')

    root_path = '/v1'

    app.register_blueprint(kitchen_blueprint(), url_prefix=root_path + '/ros')

    app.run(host='0.0.0.0', port=http_port, debug=True, use_reloader=False)


def start_webapp_thread(http_port):
    """Start a self-dying thread for the Web App"""
    web_app = Thread(name='Web App', target=thread_web_app, args=(http_port,), daemon=True)
    web_app.start()
    return web_app
