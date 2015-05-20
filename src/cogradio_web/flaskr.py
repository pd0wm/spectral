from flask import Flask, request, render_template, jsonify
from flask.ext.bower import Bower
from element import TextElement, SliderElement, CheckBoxElement
from content import Content
import Pyro4
import logging

settings = Pyro4.Proxy("PYRONAME:cg.settings")

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

Bower(app)

gain_slider = SliderElement(key="antenna_gain", title="Antenna gain", value=10, width=3, range=(0, 50))
freq_slider = SliderElement(key="center_freq", title="Center Frequency", value=2400, width=3, range=(2.4e3, 2.5e3))

cnt = Content()
cnt.add(gain_slider, position=(0, 0))
cnt.add(freq_slider, position=(0, 1))


@app.route('/')
def index():
    return render_template('index.html', content=cnt.html, js_init=cnt.js_init)


@app.route('/status')
def status():
    # Generate code to run on the client to update elements
    update_code = cnt.update_eval
    return jsonify(**update_code)


@app.route('/update', methods=["POST"])
def update():
    data = request.get_json()

    uuid = data['id']
    value = data['value']

    cnt.set_by_uuid(uuid, value)
    settings.update(cnt.values)

    return ('', 204)            # Return empty response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
