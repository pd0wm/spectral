from flask import Flask, request, render_template, jsonify
from flask.ext.bower import Bower
from element import TextElement, SliderElement, CheckBoxElement, VisualisationElement
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

gain_slider = SliderElement(key="antenna_gain", title="Antenna gain",
                            value=10, width=1, range=(0, 50))
freq_slider = SliderElement(key="center_freq", title="Center Frequency",
                            value=2400, width=2, range=(2.4e3, 2.5e3))
thresh_slider = SliderElement(key="threshold", title="Detector Threshold",
                              value=0.001, width=2, range=(1e-10, 1e-7), scale='logarithmic', step=1e-10)
bin_slider = SliderElement(key="num_bins", title="Number of Bins",
                           value=500, width=1, range=(1, 1000))
vis1 = VisualisationElement(key="vis1", title="Test 1")
vis2 = VisualisationElement(key="vis2", title="Test 2")

cnt = Content()
cnt.add(gain_slider, position=(0, 0))
cnt.add(freq_slider, position=(1, 0))
cnt.add(thresh_slider, position=(2, 0))
cnt.add(bin_slider, position=(3, 0))
cnt.add(vis1, position=(0, 1))
cnt.add(vis2, position=(1, 1))


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
