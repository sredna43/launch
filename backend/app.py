from flask import Flask, request

app = Flask(__name__)
app.secret_key = "SUPER SECRET KEY"


if __name__ == '__main__':
    app.run(debug=True, port=6000, host='0.0.0.0')