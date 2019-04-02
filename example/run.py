from example.celery import add


if __name__ == '__main__':
    add.runtask(1,2)