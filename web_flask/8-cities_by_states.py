#!/usr/bin/python3
"""
A simple Flask web application that displays a list of all cities by state.

Routes:
    /cities_by_states: Displays an HTML page with a list of all cities grouped by state.

Functions:
    states_cities: Fetches and renders the list of cities grouped by state.
    closedown: Closes the SQLAlchemy session.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
import os

app = Flask(__name__)

@app.route("/cities_by_states", strict_slashes=False)
def states_cities():
    """
    Displays an HTML page with a list of all cities grouped by state.

    Returns:
        The rendered HTML template displaying the list of cities grouped by state.
    """
    states = storage.all(State)
    return render_template("8-cities_by_states.html", states=states)

@app.teardown_appcontext
def closedown(exec):
    """
    Closes the SQLAlchemy session after each request.

    Args:
        exec: The exception that was raised (if any).
    """
    storage.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
