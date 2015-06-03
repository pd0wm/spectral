import logging
from flask import Flask, render_template
from flask.ext.bower import Bower
from element import TextElement, SliderElement, CheckBoxElement, VisualisationElement
from content import Content

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

Bower(app)

gain_slider = SliderElement(key="antenna_gain", title="Antenna gain",
                            value=10, width=1, range=(0, 50))
freq_slider = SliderElement(key="center_freq", title="Center Frequency",
                            value=2400, width=2, range=(2.38e3, 2.42e3))
thresh_slider = SliderElement(key="threshold", title="Detector Threshold",
                              value=0.001, width=2, range=(1e-10, 1), scale='logarithmic', step=1e-10)
bin_slider = SliderElement(key="num_bins", title="Number of Bins",
                           value=20, width=1, range=(1, 100))
win_len_slider = SliderElement(key="window_length", title="Detection windows", value=20, width=1, range=(1, 100))
vis1 = VisualisationElement(key="vis1", title="Test 1")
vis2 = VisualisationElement(key="vis2", title="Test 2")

cnt = Content()
cnt.add(gain_slider, position=(0, 0))
cnt.add(freq_slider, position=(1, 0))
cnt.add(thresh_slider, position=(0, 1))
cnt.add(bin_slider, position=(1, 1))
cnt.add(win_len_slider, position=(2, 1))
cnt.add(vis1, position=(0, 2))
cnt.add(vis2, position=(1, 2))


@app.route('/')
def index():
    return render_template('index.html', content=cnt.html, js_init=cnt.js_init)
