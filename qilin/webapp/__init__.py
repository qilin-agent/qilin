from flask import Flask


STATIC_FOLDER = '../../qilin-fe/build/'
STATIC_URL_PATH = ''


def create_webapp():
    app = Flask(__name__, static_folder=STATIC_FOLDER, static_url_path=STATIC_URL_PATH)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return app.send_static_file("index.html")

    return app
