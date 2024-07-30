#!/usr/bin/env python3
"""
Basic Flask app demonstrating routes and templates.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    """
    Route for the hello_world page.

    Returns:
    str: HTML rendered for the hello_world page.
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(debug=True)
