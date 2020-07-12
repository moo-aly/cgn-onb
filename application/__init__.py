import sqlite3
from flask import Flask, render_template, g
from flask_graphql import GraphQLView
from celery import Celery
import application.conf as cfg
from repository.database import db_session
from repository.schema import schema
from graphene_file_upload.flask import FileUploadGraphQLView


flask_app = Flask(__name__)
flask_app.config.from_pyfile('conf.py')

with flask_app.app_context():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(cfg.DB_FILE)
    with flask_app.open_resource('patient.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


app = Celery(flask_app.name, broker=cfg.CELERY_BROKER_URL)
app.conf.update(flask_app.config)
app.control.inspect().active()

flask_app.add_url_rule('/graphql', view_func=FileUploadGraphQLView.as_view('graphql', schema=schema, graphiql=True, context={'session': db_session}))

from controller.file_api import file_bp
flask_app.register_blueprint(file_bp)

# if __name__ == '__main__':
#     flask_app.run()