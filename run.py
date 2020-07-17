from application import flask_app
from application import cfg

if __name__ == '__main__':
    flask_app.run(host=cfg.APP_IP, port=cfg.APP_PORT)
