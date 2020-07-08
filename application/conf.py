
ENV = "development"
DEBUG = True
APP_IP = "127.0.0.1"
APP_PORT = "5000"

# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://localhost'

DB_URL = 'sqlite:///cgn-demo.db'
DB_FILE = 'cgn-demo.db'
