# from celery import shared_task
from application import app


@app.task(name='service_ops.tasks.create_random_file')
def create_random_file_task(file_name):
    print('start writing')
    file = open(file_name + '.txt', mode='w+')
    for i in range(100):
        file.write('this is a new line by celery worker \r\n')
    file.close()
    return 'file is created'
