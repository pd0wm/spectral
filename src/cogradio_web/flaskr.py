from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask.ext.bower import Bower
from element import TextElement, SliderElement, CheckBoxElement
from content import Content
import random
import Pyro4
import socket

settings = Pyro4.Proxy("PYRONAME:cg.settings")

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
Bower(app)

el1 = TextElement(key="uptime", title="Uptime", value=123)
el2 = TextElement(key="system_status", title="System Status", value="Critical")
el3 = SliderElement(
    key="slider", title="Test slider", value=42, range=(0, 100))
el4 = SliderElement(
    key="gain", title="Wide Slider", value=10, width=2, range=(0, 100000))

cnt = Content()
cnt.add(el1, (0, 1))
cnt.add(el2, (1, 0))
cnt.add(el3, (2, 2))
cnt.add(el4, (1, 3))


@app.route('/')
def index():
    content = "test"
    return render_template('index.html', content=cnt.html, js_init=cnt.js_init)


@app.route('/status')
def status():
    sts = cnt.update_eval
    return jsonify(**sts)


@app.route('/update', methods=["POST"])
def update():
    data = request.get_json()

    uuid = data['id']
    value = data['value']

    cnt.set_by_uuid(uuid, value)
    settings.update(cnt.values)

    return jsonify({uuid: value})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
