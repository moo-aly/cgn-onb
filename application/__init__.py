from flask import Flask
from celery import Celery
import application.conf as cfg

app = Flask(__name__)
app.config.from_pyfile(cfg)

celery = Celery(app.name, broker=cfg.CELERY_BROKER_URL)
celery.conf.update(app.config)
