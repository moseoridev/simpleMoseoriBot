from flask import Flask

app = Flask(__name__)


@app.route('/')
def mainpage():
    return '<h1>모서리봇 moseoribot</h1><br><p>안녕하세요. 저는 모서리봇입니다.<br>Hello. I\'m moseoribot.<br>Bonjour. Je suis moseoribot.</p>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
