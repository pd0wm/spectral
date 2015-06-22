import logging
import spectral.supervisor as ss
from flask import Flask, render_template
from flask.ext.bower import Bower
from elements import SliderElement, SweepElement, VisualisationElement, TextElement, CheckboxElement
from content import Content

# Init Flask application.
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
Bower(app)

# Set up logging.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def dashboard_get_content():
    gain_slider = SliderElement(key="antenna_gain", title="Antenna gain",
                                width=1, range=(0, 50))
    freq_slider = SliderElement(key="center_freq", title="Center Frequency",
                                value=2.4, width=2, range=(2.38, 2.42), step=0.001)
    bin_slider = SliderElement(key="num_bins", title="Number of Bins", width=1, range=(100, 200))
    win_len_slider = SliderElement(key="window_length", title="Detection windows", width=1, range=(1, 200))
    vis1 = VisualisationElement(key="vis1", title="", default_type="fft", default_datatype="src_data")
    vis2 = VisualisationElement(key="vis2", title="", default_type="fft", default_datatype="rec_data")

    cnt = Content()
    cnt.add(gain_slider, position=(0, 0))
    cnt.add(freq_slider, position=(1, 0))
    cnt.add(bin_slider, position=(2, 0))
    cnt.add(win_len_slider, position=(3, 0))
    cnt.add(vis1, position=(0, 2))
    cnt.add(vis2, position=(1, 2))

    settings = ss.get_settings_object()

    return cnt


def sweep_get_content():
    sweep = SweepElement(key="sweep", title="Frequency sweep", default_datatype="src_data")

    cnt = Content()
    cnt.add(sweep, position=(0, 0))

    return cnt

dashboard_content = dashboard_get_content()
sweep_content = sweep_get_content()


@app.route('/')
def index():
    cnt = dashboard_content
    return render_template('dashboard.html', content=cnt.html, js_init=cnt.js_init)


# Set up sweep elements
@app.route('/sweep')
def sweep():
    cnt = sweep_content
    return render_template('sweep.html', content=cnt.html, js_init=cnt.js_init)
