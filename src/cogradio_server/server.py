from flask import Flask, render_template
import flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

flask.url_for('static', filename='/bootstrap/js/bootstrap-theme.min.css')
flask.url_for('static', filename='/bootstrap/css/bootstrap.min.css')
flask.url_for('static', filename='/bootstrap/js/bootstrap.min.js')
