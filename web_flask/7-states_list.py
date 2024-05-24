#!/usr/bin/python3
"""simple flask application
"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage.

    """
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def closedown(exec):
    """close the SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
