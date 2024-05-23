#!/usr/bin/python3
"""simple flask application
"""
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display hello"""
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
