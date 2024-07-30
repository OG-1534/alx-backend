#!/usr/bin/env python3
"""
Babel integration, locale selection, forced locale parameter,
and user login emulation in Flask app.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _


class Config:
    """
    Flask app configuration class.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


# configure the flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Gets the user dictionary based on the login_as parameter.

    Returns:
        User dictionary or None if the ID is not found or not given.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Function to be executed before other functions
    to set the current user in flask.g.user.
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Select the best match for supported languages
    using request.accept_languages or locale parameter.

    Returns:
    str: The best matched language or the forced locale.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """
    Route for the index page.

    Returns:
    str: Rendered HTML for the index page.
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(debug=True)
