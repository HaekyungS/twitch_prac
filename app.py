from flask import Flask
from connect import MyClient

app = Flask(__name__)


@app.route('/')
def chat():
    return MyClient()


if __name__ == '__main__':
    app.run(debug=True)
