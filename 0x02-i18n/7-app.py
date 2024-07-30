#!/usr/bin/env python3
"""
Flask app with Babel integration,
locale and timezone selection,
forced locale parameter, and user login emulation.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, lazy_gettext as _l
import pytz
from pytz import exceptions


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
    Get the user dictionary based on the login_as parameter.

    Returns:
        user dictionary or None if the user ID is not found or provided.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Function to be executed before each function
    to set the current user in flask.g.user
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Select the best match for supported languages
    using URL parameter, user settings,
    request.accept_languages, or default locale.

    Returns:
    str: The best matched language.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Select the best match for supported timezones
    using URL parameter, user settings, or default to UTC.

    Returns:
    str: The best matched timezone.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except exceptions.UnknownTimeZoneError:
            pass

    if g.user and g.user['timezone']:
        try:
            return pytz.timezone(g.user['timezone']).zone
        except exceptions.UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """
    Route for the index page.

    Returns:
    str: Rendered HTML for the index page.
    """
    return render_template('7-index.html')


if __name__ == "__main__":
    app.run(debug=True)
