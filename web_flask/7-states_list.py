#!/usr/bin/python3
"""
A simple Flask web application that displays a list of all State objects 
stored in the database.

Routes:
    /states_list: Displays an HTML page with a list of all State objects.
    
Functions:
    states_list: Fetches and renders the list of states.
    closedown: Closes the SQLAlchemy session.
"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.route("/states_list", strict_slashes=False)
def states_list():
    """
    Displays an HTML page with a list of all State objects in DBStorage.

    The states are sorted in ascending order by name.

    Returns:
        The rendered HTML template displaying the list of states.
    """
    states = storage.all(State)
    return render_template("7-states_list.html", states=states)

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
