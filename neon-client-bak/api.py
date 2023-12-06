import threading
from http import HTTPStatus

from flask import Flask, request


api_app = Flask(__name__)
global _r


@api_app.get("/")
def index():
    return ""


@api_app.get("/ping")
def ping():
    return "ok"


@api_app.post("/messages")
def messages():
    body = request.json
    message = body["message"]
    position = body["position"]
    size = body["size"]
    selector = body["selector"]
    xpath = body["xpath"]
    print('message', message[:message.index(">") + 1])
    print('position', position)
    print('size', size)
    print('selector', selector)
    print('xpath', xpath)
    print()
    _r.draw(
        (int(body["position"]["x"]),
         int(body["position"]["y"]),
         int(body["size"]["width"]),
         int(body["size"]["height"])),
        message[:message.index(">") + 1])
    app.browser_info = body
    app.recording = False
    return {}, HTTPStatus.OK


@api_app.after_request
def after_request(res):
    # CORS
    h = res.headers
    h["Access-Control-Allow-Origin"] = "*"
    h["Access-Control-Allow-Headers"] = "*"
    h["Access-Control-Allow-Methods"] = "*"
    return res


def run(r):
    global _r
    _r = r
    threading.Thread(
        target=api_app.run,
        kwargs=dict(host="0.0.0.0", port=18000),
        daemon=True,
    ).start()
