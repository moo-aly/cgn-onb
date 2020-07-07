from flask import Flask
from celery import Celery
import application.conf as cfg

flask_app = Flask(__name__)
flask_app.config.from_pyfile('conf.py')

app = Celery(flask_app.name, broker=cfg.CELERY_BROKER_URL)
app.conf.update(flask_app.config)
app.control.inspect().active()

# from service_ops.tasks import Tasks
# @flask_app.route('/create/<file_name>')
# def create_file(file_name):
#     # task = Tasks()
#     # task.create_random_file(file_name=file_name)
#     create_random_file.delay(file_name)
#     return 'creating file...'
#
# @app.task(name='application.__init__.create_random_file')
# def create_random_file(file_name):
#     print('start writing')
#     file = open(file_name + '.txt', mode='w+')
#     for i in range(100):
#         file.write('this is a new line by celery worker \r\n')
#     file.close()
#     return 'file created'

# if __name__ == '__main__':
#     flask_app.run()

from controller.file_api import file_bp
flask_app.register_blueprint(file_bp)