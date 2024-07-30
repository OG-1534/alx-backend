#!/usr/bin/env python3
"""
Babel integration and locale selection in Flask app.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """
    Flask app configuration class.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Select the best match for supported languages
    using request.accept_languages.

    Returns:
    str: The best matched language.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Route for the index page.

    Returns:
    str: Rendered HTML for the index page.
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(debug=True)
