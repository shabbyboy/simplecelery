from example.celery import add


if __name__ == '__main__':
    print(add.runtask(1,2))