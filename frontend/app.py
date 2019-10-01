from flask import Flask, url_for, render_template, request, Response
from flask_static_compress import FlaskStaticCompress
from flask_bootstrap import Bootstrap

app = Flask(__name__, template_folder='templates', static_folder="static")
Bootstrap(app)

@app.route('/')
def homepage():
    return render_template('index.html', title="Launch UI")

if __name__ == '__main__':
    app.run(use_reloader=True)