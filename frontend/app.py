from flask import Flask, render_template, flash, request
app = Flask(__name__, template_folder='/templates')
DEBUG = True

@app.route('/')
def homepage():
    return render_template('index.html', title="Launch UI")

if __name__ == '__main__':
    app.run(use_reloader=True)