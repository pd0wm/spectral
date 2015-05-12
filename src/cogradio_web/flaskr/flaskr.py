from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask.ext.bower import Bower
import random


app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
Bower(app)


from element import TextElement, SliderElement
from content import Content
el1 = TextElement(key="uptime", title="Uptime", value=123)
el2 = TextElement(key="system_status", title="System Status", value="Critical")
el3 = SliderElement(key="slider", title="Test slider", value=42)

cnt = Content()
cnt.add(el1, (0, 1))
cnt.add(el2, (1, 0))
cnt.add(el3, (2, 2))

    

@app.route('/')
def index():
    content = "test"
    return render_template('index.html', content=cnt.html, js_init=cnt.js_init)

@app.route('/status')
def status():
    sts = cnt.values
    return jsonify(**sts)

@app.route('/update/<id>/<value>')
def update(id, value):
    print id, value
    cnt.set_by_uuid(id, value)
    cnt.set_by_uuid(el1.uuid, value)
    return jsonify({id: value})

if __name__ == '__main__':
    app.run()
