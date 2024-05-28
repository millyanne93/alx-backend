#!/usr/bin/env python3
"""
A simple Flask app demonstrating localization,
user-based content, and time zone selection.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz
from pytz import UnknownTimeZoneError


class Config(object):
    """
    Configuration class for the Flask application.
    Defines available languages and default locale and timezone.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Configure the Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """
    Retrieves a user dictionary based on the 'login_as' URL parameter.
    Returns None if the user ID is not found or not provided.

    Returns:
        dict or None: The user dictionary or None.
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Function to be executed before each request.
    Sets the current user in the global 'g' object.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    """
    Selects the best locale based on the
    incoming request or user preference.
    Checks the following in order:
    1. 'locale' parameter in the URL.
    2. User's preferred locale.
    3. Best match from the 'Accept-Language' request header.
    4. Default locale.

    Returns:
        str: The selected locale.
    """
    # 1. Check URL parameter
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    # 2. Check user's preferred locale
    if g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    # 3. Check Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Selects the best timezone based on the incoming
    request or user preference.
    Checks the following in order:
    1. 'timezone' parameter in the URL.
    2. User's preferred timezone.
    3. Default to UTC.

    Returns:
        str: The selected timezone.
    """
    # 1. Check URL parameter
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    # 2. Check user's preferred timezone
    if g.user:
        user_timezone = g.user.get('timezone')
        if user_timezone:
            try:
                pytz.timezone(user_timezone)
                return user_timezone
            except UnknownTimeZoneError:
                pass

    # 3. Default to UTC
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index():
    """
    Route handler for the root URL.
    Renders the index template.

    Returns:
        str: Rendered HTML content.
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(port="5000", host="0.0.0.0", debug=True)
