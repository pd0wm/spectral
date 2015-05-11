from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify
from flask.ext.bower import Bower
import random


app = Flask(__name__)
app.config.from_object(__name__)
Bower(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    r = random.randint(0,1000)
    sts = {'uptime' : r}
    return jsonify(**sts)

if __name__ == '__main__':
    app.run()
