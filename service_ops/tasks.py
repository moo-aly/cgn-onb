# from celery import shared_task
from application import app
from werkzeug.datastructures import FileStorage
from io import StringIO, BytesIO

@app.task(name='service_ops.tasks.create_random_file')
def create_random_file_task(file_name):
    print('start writing')
    file = open(file_name + '.txt', mode='w+')
    for i in range(100):
        file.write('this is a new line by celery worker \r\n')
    file.close()
    return 'file is created'


@app.task(name='service_ops.tasks.save_file', serializer='pickle')
def save_file(stream, filename, name, content_length, content_type, headers):
    # send it to hdfs, elastic, some analysis tool, ..etc
    doc = FileStorage(stream=BytesIO(stream), filename=filename, name=name, content_type=content_type, content_length=content_length)
    doc.save(dst=filename)
    return 'file is being saved'