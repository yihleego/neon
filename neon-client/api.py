import threading
from http import HTTPStatus

from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def index():
    return ""


@app.get("/ping")
def ping():
    return "ok"


@app.post("/messages")
def messages():
    body = request.json
    message = body["message"]
    position = body["position"]
    size = body["size"]
    print('message', message[:message.index(">") + 1])
    print('position', position)
    print('size', size)
    print()
    # window.setData(
    #     int(body["position"]["x"]),
    #     int(body["position"]["y"]),
    #     int(body["size"]["width"]),
    #     int(body["size"]["height"]),
    #     message[:message.index(">") + 1])
    return {}, HTTPStatus.OK


@app.after_request
def after_request(res):
    # CORS
    h = res.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "*"
    h["Access-Control-Allow-Methods"] = "*"
    return res


def run():
    threading.Thread(
        target=app.run,
        kwargs=dict(host="0.0.0.0", port=18000),
        daemon=True,
    ).start()
