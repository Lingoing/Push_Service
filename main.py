from flask import Flask

app = Flask(__name__)


# 指定 URL='/' 的路由规则
@app.route('/')
def index():
    return "Hello World!"


if __name__ == '__main__':
    print('app_running')
    app.run()
