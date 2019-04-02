from simple import Celery

app = Celery("test")

app.config_from_object('example.config')

@app.task()
def add(x,y):
    #print(x+y)
    return x+y

@app.task()
def mutl(x,y,z):
    return x*y*z


if __name__ == '__main__':
    app.start()